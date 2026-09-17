#!/usr/bin/env python3
"""count-adaptation-effort.py -- Count the files that adding or changing a feature or
a configuration touches in the umljava 150% model, against nine separately
maintained rule sets (M1.2), and the size of such rule sets with a shared core (M1.1).

Reads the annotated reactions of Vitruv-CaseStudies
(umljava/src/main/reactions/tools/vitruv/applications/umljava), the feature gates of
its tests (umljava/src/test), and the nine configurations of Vitruv-DSLs
(reactions/preprocessor/src/main/resources/configs/config<n>.json) together with the
rule sets the preprocessor derived from them (config<n>-reactions) and the feature
model (reactions/preprocessor/src/main/resources/feature-model.uvl).

Per feature it prints the reactions and rule files that carry its annotation, the
configurations that select it and the test files that gate on it. From these follow
the files a change touches: a feature is renamed in every rule file, configuration,
the feature model and every gated test file that names it, and an added optional
feature touches the rule files of its reactions, the configurations that select it
and the feature model. The nine rule sets instead hold copies of the rule files.

The derived rule sets are split into reaction and routine blocks. A block that all
nine hold identically could be kept once in a shared core, so the size of nine rule
sets with such a core is the lines of the shared blocks once plus the rest of every
rule set. Lines are counted like count-loc.sh.

Finally every commit that changed the annotated rules after the annotations were
complete (after 5dc0221ff) is replayed against the derived rule sets: per edited rule
file, the configurations whose derived file contains one of the edited blocks, or
all nine where the edit lies outside any block. The sum over the files is the number
of (configuration, file) edits the same change costs with nine separate rule sets.

Usage: count-adaptation-effort.py <Vitruv-CaseStudies> <Vitruv-DSLs>
"""

import json
import re
import subprocess
import sys
from collections import Counter, OrderedDict
from pathlib import Path

CONFIGURATIONS = range(1, 10)
RULES = "umljava/src/main/reactions/tools/vitruv/applications/umljava"
TESTS = "umljava/src/test"
RESOURCES = "reactions/preprocessor/src/main/resources"
ANNOTATIONS_COMPLETE = "5dc0221ff"
ANNOTATION = re.compile(r'^\s*@feature\(type\s*=\s*"([^"]+)"\)')
HEADER = re.compile(r"^\s*(reaction|routine)\s+(\w+)")
GATE = re.compile(r"@(RequiresFeatures|IncompatibleFeatures)\((.*)\)")
COMMENT = re.compile(r"^(//|#|--|\*|/\*|\*/)")
HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def is_code(line):
    stripped = line.strip()
    return bool(stripped) and not COMMENT.match(stripped)


def blocks(text):
    """(kind, name, first line, last line, lines of code) of every reaction and routine,
    lines numbered from 1; braces inside strings and line comments are ignored."""
    result, lines, i = [], text.split("\n"), 0
    while i < len(lines):
        match = HEADER.match(lines[i])
        if not match:
            i += 1
            continue
        depth, seen, j = 0, False, i
        while j < len(lines):
            code = re.sub(r'"(?:\\.|[^"\\])*"', '""', lines[j].split("//")[0])
            depth += code.count("{") - code.count("}")
            seen = seen or "{" in code
            if seen and depth <= 0:
                break
            j += 1
        body = lines[i:j + 1]
        result.append((match.group(1), match.group(2), i + 1, j + 1, sum(1 for line in body if is_code(line)),
                       "\n".join(line.strip() for line in body if is_code(line))))
        i = j + 1
    return result


def git(repository, *arguments):
    return subprocess.run(["git", "-C", str(repository), *arguments], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=True).stdout


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    cases, dsls = Path(sys.argv[1]), Path(sys.argv[2])
    rules = cases / RULES
    configs = dsls / RESOURCES / "configs"
    selections = {n: json.loads((configs / f"config{n}.json").read_text(encoding="utf-8")) for n in CONFIGURATIONS}
    model_text = (dsls / RESOURCES / "feature-model.uvl").read_text(encoding="utf-8")

    reactions_of, files_of = Counter(), {}
    for path in sorted(rules.rglob("*.reactions")):
        relative = path.relative_to(rules).as_posix()
        for line in path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n"):
            match = ANNOTATION.match(line)
            if match:
                reactions_of[match.group(1)] += 1
                files_of.setdefault(match.group(1), set()).add(relative)

    gated_files, gates = {}, Counter()
    for path in sorted((cases / TESTS).rglob("*")):
        if not path.is_file() or path.suffix not in (".xtend", ".java"):
            continue
        for match in GATE.finditer(path.read_text(encoding="utf-8")):
            for feature in re.findall(r'"([^"]+)"', match.group(2)):
                gated_files.setdefault(feature, set()).add(path.relative_to(cases).as_posix())
                gates[feature] += 1

    selected_by = {feature: [n for n in CONFIGURATIONS if feature in selections[n]] for feature in reactions_of}
    print("== per feature: reactions and rule files with its annotation, configurations selecting it, test files and gates naming it")
    print(f"{'feature':<26} {'reactions':>9} {'files':>5} {'configs':>7} {'tests':>5} {'gates':>5}  in the feature model  varying")
    for feature in sorted(reactions_of, key=lambda f: (len(selected_by[f]) == 9, f)):
        in_model = feature in re.findall(r"[\w.]+", model_text)
        varying = 0 < len(selected_by[feature]) < 9
        print(f"{feature:<26} {reactions_of[feature]:>9} {len(files_of[feature]):>5} {len(selected_by[feature]):>7} "
              f"{len(gated_files.get(feature, ())):>5} {gates[feature]:>5}  {'yes' if in_model else 'NO':<20}  {'yes' if varying else ''}")
    spans = Counter(len(files) for files in files_of.values())
    print(f"features: {len(reactions_of)}, annotated reactions: {sum(reactions_of.values())}, "
          f"rule files per feature: {', '.join(f'{count} feature(s) in {files}' for files, count in sorted(spans.items()))}")

    print()
    print("== files touched per change, 150% model against nine separately maintained rule sets")
    rule_files = sorted(p.relative_to(rules).as_posix() for p in rules.rglob("*.reactions"))
    print(f"add a configuration:          1 configuration file  |  {len(rule_files)} rule files copied, then edited")
    for feature in sorted(f for f in reactions_of if 0 < len(selected_by[f]) < 9):
        k, files = len(selected_by[feature]), len(files_of[feature])
        renamed = files + k + 1 + len(gated_files.get(feature, ()))
        print(f"{feature:<26}  add: {files} rule file(s) + {k} configuration(s) + feature model = {files + k + 1}"
              f"  |  {files} rule file(s) in {k} rule sets = {files * k};"
              f"  rename: {files} rule + {k} configuration + 1 model + {len(gated_files.get(feature, ()))} test files = {renamed}")
    for feature in ("Naming", "ClassCreation.Class"):
        k, files = len(selected_by[feature]), len(files_of[feature])
        print(f"{feature:<26}  rename: {files} rule + {k} configuration + 1 model + {len(gated_files.get(feature, ()))} test files"
              f" = {files + k + 1 + len(gated_files.get(feature, ()))}")
    print("fix a block that all nine rule sets hold: 1 rule file  |  9 rule files")

    print()
    print("== nine rule sets with a shared core")
    per_config, versions, loc = {}, {}, {}
    for n in CONFIGURATIONS:
        folder = configs / f"config{n}-reactions"
        total, found = 0, set()
        for path in sorted(folder.rglob("*.reactions")):
            text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
            total += sum(1 for line in text.split("\n") if is_code(line))
            for kind, name, _, _, lines, body in blocks(text):
                key = (path.relative_to(folder).as_posix(), kind, name, body)
                found.add(key)
                versions[key] = lines
        per_config[n], loc[n] = found, total
    shared = set.intersection(*per_config.values())
    shared_loc = sum(versions[key] for key in shared)
    total_loc = sum(loc.values())
    print(f"lines per configuration:              {', '.join(str(loc[n]) for n in CONFIGURATIONS)} (sum {total_loc})")
    print(f"distinct block versions:              {len(versions)} with {sum(versions.values())} lines")
    print(f"blocks all nine hold identically:     {len(shared)} with {shared_loc} lines")
    print(f"nine rule sets with a shared core:    {shared_loc} + {total_loc} - 9 x {shared_loc} = {total_loc - 8 * shared_loc}")

    print()
    print(f"== commits that changed the annotated rules after {ANNOTATIONS_COMPLETE}, replayed against the derived rule sets")
    history = git(cases, "log", "--reverse", "--format=%h %ad %s", "--date=short",
                  f"{ANNOTATIONS_COMPLETE}..HEAD", "--", RULES).strip().split("\n")
    sum_files = sum_pairs = 0
    for entry in filter(None, history):
        commit = entry.split()[0]
        diff = git(cases, "diff", "-U0", f"{commit}^", commit, "--", RULES)
        edited = OrderedDict()
        current = None
        for line in diff.split("\n"):
            if line.startswith("+++ "):
                current = None if line.endswith("/dev/null") else line[6:]
                if current:
                    edited[current] = []
            match = HUNK.match(line)
            if match and current:
                start, count = int(match.group(3)), int(match.group(4) if match.group(4) is not None else 1)
                edited[current].append((start, max(start + count - 1, start)))
        files = pairs = 0
        details = []
        for path, ranges in edited.items():
            text = git(cases, "show", f"{commit}:{path}").replace("\r\n", "\n")
            touched, outside = set(), False
            for first, last in ranges:
                hit = [name for kind, name, start, end, _, _ in blocks(text) if start <= last and first <= end]
                touched.update(hit)
                outside = outside or not hit
            relative = path.split("applications/umljava/", 1)[1]
            holding = []
            for n in CONFIGURATIONS:
                derived = configs / f"config{n}-reactions" / relative
                names = {name for _, name, _, _, _, _ in blocks(derived.read_text(encoding="utf-8").replace("\r\n", "\n"))} \
                    if derived.is_file() else set()
                if outside or touched & names:
                    holding.append(n)
            files += 1
            pairs += len(holding)
            details.append(f"    {relative}: blocks {', '.join(sorted(touched)) or '-'}{' + lines outside blocks' if outside else ''}"
                           f"; held by config {', '.join(map(str, holding)) or 'none'}")
        sum_files += files
        sum_pairs += pairs
        print(f"{entry}: {files} rule file(s) | {pairs} (configuration, file) edit(s)")
        print("\n".join(details))
    print(f"total: {sum_files} rule file edits | {sum_pairs} (configuration, file) edits")


if __name__ == "__main__":
    main()
