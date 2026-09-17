#!/usr/bin/env python3
"""summarize-migration-reports.py -- Sum up what the 81 cells of the library
matrix report about the VSUM bookkeeping a configuration switch disturbs.

Usage: summarize-migration-reports.py <thesis/examples/library>

Reads runs/config<F>-to-config<T>/cell.properties (the numbers the generator
recorded: dirty rules, affected elements, deviations from the from-scratch
derivation, preservation counts, compiler errors) and the cell's
preservation-report.md (every item the preservation pass listed, by section and
by what it says about the item). Prints the per-cell table and, over the
migrated cells, the totals per section, per metaclass of the listed content and
per reason the pass gives for content it could not keep.

The last sections follow the handwritten body of Member.totalWeight. The
compiler errors of each cell's RUN.md are grouped by message and by the member
they point at. The body gets a situation per cell, from the body in the source
baseline, the body in the migrated Member.java and the report items for its
statements. Everything else the reports list is counted once per item, an open
decision together with the Not kept item it concerns, and grouped by cause.
"""

import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

KEYS = ["dirtyRules", "affectedElements", "umlDeviations", "javaDeviations", "correspondenceDeviations",
        "umlOrderings", "javaOrderings", "kept", "lost", "undecided", "manualItems", "compilerErrors", "fellBackToFull"]
SECTION = re.compile(r"^## (Would be kept|Not kept|Open decisions|Notes) \((\d+)\)")
BODY_STATEMENT = re.compile(r"^statements::(\w+) in Member\.totalWeight at ")
BODY_PART = re.compile(r" in Member\.totalWeight\.")
COMPILER_ERROR = re.compile(r"^(\w+\.java):(\d+) (.+)$")
DECLARATION = re.compile(r"^\s*(?:(?:public|protected|private|static|final|abstract)\s+)*(?:[\w.<>\[\],]+\s+)?(\w+)\s*\(")
NOT_A_MEMBER = {"for", "if", "while", "switch", "catch", "synchronized", "return", "super", "this"}
TYPE = re.compile(r"^\s*(?:(?:public|protected|private|static|final|abstract)\s+)*(class|interface|enum)\s+(\w+)", re.M)
MISSING_VALUE = re.compile(r"the value (\w+::\w+ '[^']*')")
NAMED = re.compile(r"^\w+::\w+ '([^']*)'")
INTO_FEATURE = re.compile(r"\((\w+)\)\s*$")


def read_properties(path):
    properties = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        properties[key.strip()] = value.strip()
    return properties


def read_report(path):
    """Items per section: (subject line, detail line) pairs."""
    sections = OrderedDict()
    current = None
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        header = SECTION.match(line)
        if header:
            current = header.group(1)
            sections[current] = items = []
            continue
        if current is None:
            continue
        if line.startswith("- "):
            items.append([line[2:], ""])
        elif line.startswith("  ") and items:
            items[-1][1] += line.strip() + " "
    return sections


def read_compiler_errors(path):
    """(file, line, message) per error that RUN.md lists under 'Does the Java compile'."""
    errors = []
    inside = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            inside = line == "## Does the Java compile"
        elif inside:
            match = COMPILER_ERROR.match(line)
            if match:
                errors.append((match.group(1), int(match.group(2)), match.group(3)))
    return errors


def located(folder, file, line, message):
    """The error with the type and member it points at, without the line number."""
    text = (folder / "src" / "catalog" / file).read_text(encoding="utf-8")
    member = "?"
    for candidate in reversed(text.splitlines()[:line]):
        match = DECLARATION.match(candidate)
        if match and match.group(1) not in NOT_A_MEMBER:
            member = match.group(1)
            break
    kind = TYPE.search(text)
    where = f"{kind.group(1)} {kind.group(2)}" if kind else file
    return f"{message} ({where}, member {member})"


def metaclass_of(subject):
    match = re.match(r"([\w]+::[\w]+)", subject)
    return match.group(1) if match else subject.split(" ")[0]


def reason_of(detail):
    detail = detail.strip()
    for separator in (" (", ": ", "; "):
        if separator in detail:
            detail = detail.split(separator, 1)[0]
    return detail


def body_situation(root, folder, cell):
    """Where the handwritten body of Member.totalWeight ends up in one cell."""
    source = (root / "baselines" / f"config{cell['from']}" / "src" / "catalog" / "Member.java").read_text(encoding="utf-8")
    migrated = (folder / "src" / "catalog" / "Member.java").read_text(encoding="utf-8")
    kind = TYPE.search(migrated)
    if "return total;" not in source:
        situation = "Member holds no body in the source"
    elif "return total;" in migrated:
        situation = "Member is not re-derived, the body stays"
    elif kind and kind.group(1) == "interface":
        situation = "Member becomes an interface"
    else:
        situation = "Member is re-derived"
    report = cell["report"]
    kept = [BODY_STATEMENT.match(s).group(1) for s, _ in report.get("Would be kept", []) if BODY_STATEMENT.match(s)]
    lost = [f"{BODY_STATEMENT.match(s).group(1)} ({reason_of(d)})"
            for s, d in report.get("Not kept", []) if BODY_STATEMENT.match(s)]
    return f"{situation}; would be kept: {', '.join(kept) or '-'}; not kept: {', '.join(lost) or '-'}"


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    runs = Path(sys.argv[1]) / "runs"
    cells = []
    for folder in sorted(runs.glob("config*-to-config*")):
        properties_file = folder / "cell.properties"
        if not properties_file.is_file():
            continue
        cell = read_properties(properties_file)
        report_file = folder / "preservation-report.md"
        cell["report"] = read_report(report_file) if report_file.is_file() else {}
        cell["folder"] = folder
        cells.append(cell)

    print("== per cell")
    print(f"{'cell':<6} " + " ".join(f"{k[:8]:>8}" for k in KEYS))
    for cell in cells:
        print(f"{cell['from']}->{cell['to']:<3} " + " ".join(f"{cell.get(k, '-'):>8}" for k in KEYS))

    migrated = [c for c in cells if c.get("outcome") == "migrated"]
    print()
    print(f"== over the {len(migrated)} migrated cells ({len(cells)} cells present)")
    print(f"fell back to a full migration: {sum(c['fellBackToFull'] == 'true' for c in migrated)}")
    print(f"equivalent to the from-scratch derivation: {sum(c['correspondenceDeviations'] == '0' for c in migrated)}"
          f" (of which ordering-only: {sum(c['correspondenceDeviations'] == '0' and (c['umlOrderings'] != '0' or c['javaOrderings'] != '0') for c in migrated)})")
    for key in ("dirtyRules", "affectedElements", "correspondenceDeviations", "kept", "lost", "undecided", "manualItems", "compilerErrors"):
        values = sorted(int(c[key]) for c in migrated)
        print(f"{key}: total {sum(values)}, median {values[len(values) // 2]}, range {values[0]}-{values[-1]}, cells > 0: {sum(v > 0 for v in values)}")

    print()
    print("== preservation report items per section (items, cells with at least one)")
    per_section = Counter()
    cells_per_section = Counter()
    per_metaclass = OrderedDict()
    per_reason = OrderedDict()
    per_note = OrderedDict()
    for cell in migrated:
        for section, items in cell["report"].items():
            per_section[section] += len(items)
            if items:
                cells_per_section[section] += 1
            for subject, detail in items:
                if section == "Would be kept":
                    bucket = per_metaclass.setdefault(metaclass_of(subject), [0, set()])
                elif section == "Not kept":
                    bucket = per_reason.setdefault(reason_of(detail), [0, set()])
                elif section == "Notes":
                    bucket = per_note.setdefault(reason_of(detail), [0, set()])
                else:
                    bucket = per_reason.setdefault("open decision: " + reason_of(detail), [0, set()])
                bucket[0] += 1
                bucket[1].add((cell["from"], cell["to"]))
    for section in ("Would be kept", "Not kept", "Open decisions", "Notes"):
        print(f"{section}: {per_section[section]} items in {cells_per_section[section]} cells")

    def print_buckets(title, buckets):
        print()
        print(f"== {title}")
        for name, (count, cells_with) in sorted(buckets.items(), key=lambda b: -b[1][0]):
            print(f"{count:>5} items in {len(cells_with):>2} cells  {name}")

    print_buckets("would be kept, by metaclass", per_metaclass)
    print_buckets("not kept and open decisions, by reason", per_reason)
    print_buckets("notes, by kind", per_note)

    def name(cell):
        return f"{cell['from']}->{cell['to']}"

    def print_groups(groups):
        for key, members in sorted(groups.items(), key=lambda g: -len(g[1])):
            print(f"{len(members):>4} cells  {key}")
            print(f"            {' '.join(name(c) for c in members)}")

    warnings = []

    # -- compiler errors
    print()
    print("== compiler errors per migrated cell, grouped by message, type and member (line numbers dropped)")
    compile_groups = OrderedDict()
    for cell in migrated:
        errors = read_compiler_errors(cell["folder"] / "RUN.md")
        if len(errors) != int(cell["compilerErrors"]):
            warnings.append(f"{name(cell)}: RUN.md lists {len(errors)} errors, cell.properties {cell['compilerErrors']}")
        described = sorted(located(cell["folder"], *error) for error in errors)
        cell["compileResult"] = ", ".join(f"{n}x {message}" for message, n in
                                          sorted(Counter(message for _, _, message in errors).items())) or "compiles"
        compile_groups.setdefault(" | ".join(described) or "compiles", []).append(cell)
    print_groups(compile_groups)

    # -- the handwritten body
    print()
    print("== handwritten body of Member.totalWeight per migrated cell")
    body_groups = OrderedDict()
    for cell in migrated:
        cell["body"] = body_situation(runs, cell["folder"], cell)
        body_groups.setdefault(cell["body"], []).append(cell)
    print_groups(body_groups)

    print()
    print("== compile result against the body situation")
    crossed = OrderedDict()
    for cell in migrated:
        crossed.setdefault(f"{cell['compileResult']} | {cell['body'].split(';')[0]}", []).append(cell)
    print_groups(crossed)

    print()
    print("== parts of the body listed without its statements (Not kept or Would be kept), with the loop the migrated Member.java holds")
    false_parts = 0
    for cell in migrated:
        report = cell["report"]
        parts = [(s, d) for section in ("Would be kept", "Not kept") for s, d in report.get(section, []) if BODY_PART.search(s)]
        if not parts:
            continue
        if any(BODY_STATEMENT.match(s) for section in ("Would be kept", "Not kept") for s, _ in report.get(section, [])):
            warnings.append(f"{name(cell)}: parts of the body listed next to its statements")
            continue
        false_parts += len(parts)
        loop = next((line.strip() for line in (cell["folder"] / "src" / "catalog" / "Member.java")
                     .read_text(encoding="utf-8").splitlines() if line.strip().startswith("for (")), "no loop")
        print(f"  {name(cell)}  {loop}")
        for subject, detail in parts:
            value = MISSING_VALUE.search(detail)
            print(f"      {subject.split(' at ')[0]}: {reason_of(detail)}{' (' + value.group(1) + ')' if value else ''}")
    print(f"  {false_parts} parts in total")

    # -- everything else, counted once
    print()
    print("== items outside the handwritten body, each counted once")
    body_items = Counter()
    would_be_kept = OrderedDict()
    not_kept = OrderedDict()
    open_decisions, matched_decisions = 0, 0
    for cell in migrated:
        report = cell["report"]
        for subject, detail in report.get("Would be kept", []):
            if BODY_STATEMENT.match(subject) or BODY_PART.search(subject):
                body_items["Would be kept"] += 1
                continue
            package = subject.split("::")[0]
            bucket = would_be_kept.setdefault(package, [0, set(), Counter(), set()])
            bucket[0] += 1
            bucket[1].add(name(cell))
            feature = INTO_FEATURE.search(detail.strip())
            bucket[2][f"{metaclass_of(subject)} into {feature.group(1) if feature else '?'}"] += 1
            named = NAMED.match(subject)
            if named:
                bucket[3].add(named.group(1))
        for subject, detail in report.get("Not kept", []):
            if BODY_STATEMENT.match(subject) or BODY_PART.search(subject):
                body_items["Not kept"] += 1
                continue
            bucket = not_kept.setdefault(reason_of(detail), [0, set(), Counter(), Counter()])
            bucket[0] += 1
            bucket[1].add(name(cell))
            bucket[2][f"config{cell['to']}"] += 1
            value = MISSING_VALUE.search(detail) or NAMED.match(subject)
            bucket[3][value.group(1) if value else metaclass_of(subject)] += 1
        not_kept_subjects = [s for s, _ in report.get("Not kept", [])]
        for question, _ in report.get("Open decisions", []):
            open_decisions += 1
            if any(subject in question for subject in not_kept_subjects):
                matched_decisions += 1
            else:
                warnings.append(f"{name(cell)}: open decision without a Not kept item: {question}")

    total_kept = sum(b[0] for b in would_be_kept.values())
    total_lost = sum(b[0] for b in not_kept.values())
    print(f"body statements and parts: Would be kept {body_items['Would be kept']}, Not kept {body_items['Not kept']}")
    print(f"open decisions: {open_decisions}, each the same item as a Not kept entry of its cell: {matched_decisions}")
    print(f"distinct items outside the body: Would be kept {total_kept} + Not kept {total_lost} = {total_kept + total_lost}")
    print()
    print("-- Would be kept, by package")
    for package, (count, cells_with, kinds, names) in sorted(would_be_kept.items(), key=lambda b: -b[1][0]):
        print(f"{count:>5} items in {len(cells_with):>2} cells  {package}")
        for kind, n in kinds.most_common():
            print(f"            {n:>4}  {kind}")
        if names:
            print(f"            names: {', '.join(sorted(names))}")
    print()
    print("-- Not kept, by reason, with the target configurations and what the item is or references")
    for reason, (count, cells_with, targets, values) in sorted(not_kept.items(), key=lambda b: -b[1][0]):
        print(f"{count:>5} items in {len(cells_with):>2} cells  {reason}")
        print(f"            into {', '.join(f'{t} {n}' for t, n in sorted(targets.items()))}")
        print(f"            {', '.join(f'{v} {n}' for v, n in values.most_common())}")

    print()
    print("== warnings")
    for warning in warnings or ["none"]:
        print(f"  {warning}")


if __name__ == "__main__":
    main()
