#!/usr/bin/env python3
"""measure-migration-scope.py -- How much of a V-SUM the selective migration
touches: dirty rules relative to all rules, and affected elements and the
elements inside their subtrees relative to all elements, per configuration
pair (M4.1).

Usage: measure-migration-scope.py <thesis/examples/library>

For every migrated cell runs/config<F>-to-config<T> the counts are read from
cell.properties: the persisted registry and the new specifications, the dirty
rules split into added, removed and matching, the affected elements split into
matched and referrers, the elements in the models, the source elements probed
and the elements left out. The dirty-rule list of RUN.md adds the direction
each rule belongs to. The dirty share is put against the persisted registry,
the new specifications and the union of both, which is the one set every dirty
rule belongs to; the affected share against the elements in the models and the
source elements probed, which are the elements of the UML model. A repropagation
tears down and reinserts an affected element with everything it contains, so
the affected elements of RUN.md are also resolved in the UML model of
runs/baselines/config<F>, the state the migration started from, and the
elements with an xmi:id inside their subtrees are counted against all elements
of that model. Prints the per-pair table, the denominators per source
configuration, the from/to grid of the raw counts, the totals, medians and
ranges over the pairs, the dirty rules by direction and the unordered pairs
whose two directions disagree.
"""

import re
import statistics
import sys
import xml.etree.ElementTree as ET
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

CONFIGURATIONS = range(1, 10)
DIRTY_LINE = re.compile(r"^([+\-~]) (\S+)  matches (\d+) source element\(s\)$")
AFFECTED_KEY = re.compile(r"^library\.uml#/(\d+)((?:/[^/\s]+)*)\s")
XMI_ID = "{http://www.omg.org/spec/XMI/20131001}id"
COUNTS = ("rulesPersisted", "rulesCurrent", "dirtyRules", "dirtyRulesAdded", "dirtyRulesRemoved",
          "dirtyRulesMatching", "affectedElements", "matchedElements", "referrerElements",
          "sourceElements", "modelElements", "leftOutElements")


def read_properties(path):
    properties = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        properties[key.strip()] = value.strip()
    return properties


def fenced_blocks(text):
    """The fenced code block under each '### heading' of the selection section."""
    blocks = {}
    heading = None
    lines = None
    for line in text.splitlines():
        if line.startswith("### "):
            heading = line[4:].strip()
            blocks[heading] = []
            lines = None
        elif line.startswith("```"):
            if heading is None:
                continue
            if lines is None:
                lines = blocks[heading]
            else:
                heading = None
                lines = None
        elif lines is not None:
            lines.append(line)
    return blocks


def read_dirty(cell):
    """The dirty rules of a cell's RUN.md as (name, marker, matches), or None without the section."""
    text = (cell / "RUN.md").read_text(encoding="utf-8")
    start = text.find("## What the rule diff and the trigger mechanism found")
    if start < 0:
        return None
    blocks = fenced_blocks(text[start:text.find("\n## ", start + 1)])
    dirty = []
    for line in blocks.get("Dirty rules", []):
        match = DIRTY_LINE.match(line)
        if match is None:
            raise SystemExit(f"{cell.name}: cannot read the dirty rule line {line!r}")
        dirty.append((match.group(2), match.group(1), int(match.group(3))))
    return dirty


def read_affected(cell):
    """The affected elements of a cell's RUN.md as (root index, names on the path), or None without the section."""
    text = (cell / "RUN.md").read_text(encoding="utf-8")
    start = text.find("## What the rule diff and the trigger mechanism found")
    if start < 0:
        return None
    blocks = fenced_blocks(text[start:text.find("\n## ", start + 1)])
    affected = []
    for line in blocks.get("Affected elements", []):
        match = AFFECTED_KEY.match(line)
        if match is None:
            raise SystemExit(f"{cell.name}: cannot read the affected element line {line!r}")
        affected.append((int(match.group(1)), [name for name in match.group(2).split("/") if name]))
    return affected


def subtrees(model, affected):
    """(elements inside the subtrees of the affected elements, all elements, paths not found), counted by xmi:id."""
    root = ET.parse(model).getroot()
    roots = list(root) if root.tag.endswith("XMI") else [root]
    everything = {element.get(XMI_ID) for top in roots for element in top.iter() if XMI_ID in element.attrib}
    covered, missing = set(), []
    for index, names in affected:
        node = roots[index] if index < len(roots) else None
        for name in names:
            if node is None:
                break
            node = next((child for child in node if child.get("name") == name), None)
        if node is None:
            missing.append("/".join(names))
            continue
        covered.update(element.get(XMI_ID) for element in node.iter() if XMI_ID in element.attrib)
    return len(covered), len(everything), missing


def direction_of(rule):
    prefix = rule.split("::", 1)[0]
    if prefix.startswith("umlToJava"):
        return "uml2java"
    if prefix.startswith("javaToUml"):
        return "java2uml"
    return None


def num(value):
    return f"{value:g}"


def median_range(values):
    return f"{num(statistics.median(values))} ({num(min(values))}-{num(max(values))})"


def percent_summary(shares, digits=1):
    fmt = f"{{:.{digits}%}}"
    return (f"median {fmt.format(statistics.median(shares))}, "
            f"range {fmt.format(min(shares))}-{fmt.format(max(shares))}")


def pooled(numerator, denominator, digits=1):
    return f"pooled {numerator}/{denominator} = {numerator / denominator:.{digits}%}"


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    runs = Path(sys.argv[1]) / "runs"

    warnings = []
    pairs = OrderedDict()
    diagonals = 0
    rules_of = defaultdict(set)
    for f in CONFIGURATIONS:
        for t in CONFIGURATIONS:
            cell = runs / f"config{f}-to-config{t}"
            if not (cell / "cell.properties").is_file():
                warnings.append(f"config{f} -> config{t}: not generated, skipped")
                continue
            properties = read_properties(cell / "cell.properties")
            if properties.get("outcome") == "diagonal":
                diagonals += 1
                continue
            if properties.get("outcome") != "migrated":
                warnings.append(f"config{f} -> config{t}: outcome {properties.get('outcome')}, skipped")
                continue
            pair = {key: int(properties[key]) for key in COUNTS}
            pair["fellBack"] = properties.get("fellBackToFull") == "true"
            if pair["fellBack"]:
                warnings.append(f"config{f} -> config{t}: fell back to a full migration")
            pair["union"] = pair["rulesPersisted"] + pair["dirtyRulesAdded"]
            if pair["union"] != pair["rulesCurrent"] + pair["dirtyRulesRemoved"]:
                warnings.append(f"config{f} -> config{t}: persisted {pair['rulesPersisted']} + added "
                                f"{pair['dirtyRulesAdded']} != current {pair['rulesCurrent']} + removed "
                                f"{pair['dirtyRulesRemoved']}, the union is ill-defined")
            if pair["dirtyRules"] != pair["dirtyRulesAdded"] + pair["dirtyRulesRemoved"]:
                warnings.append(f"config{f} -> config{t}: dirtyRules={pair['dirtyRules']} but "
                                f"{pair['dirtyRulesAdded']} added + {pair['dirtyRulesRemoved']} removed")
            if pair["affectedElements"] != pair["matchedElements"] + pair["referrerElements"]:
                warnings.append(f"config{f} -> config{t}: affectedElements={pair['affectedElements']} but "
                                f"{pair['matchedElements']} matched + {pair['referrerElements']} referrers")
            for key in ("rulesPersisted", "rulesCurrent", "union", "modelElements", "sourceElements"):
                if pair[key] == 0:
                    warnings.append(f"config{f} -> config{t}: {key} is zero")
            pair["dirty"] = read_dirty(cell)
            if pair["dirty"] is None:
                warnings.append(f"config{f} -> config{t}: RUN.md has no selection section")
            else:
                if len(pair["dirty"]) != pair["dirtyRules"]:
                    warnings.append(f"config{f} -> config{t}: dirtyRules={pair['dirtyRules']} but "
                                    f"{len(pair['dirty'])} listed in RUN.md")
                if sum(1 for _, _, matches in pair["dirty"] if matches > 0) != pair["dirtyRulesMatching"]:
                    warnings.append(f"config{f} -> config{t}: dirtyRulesMatching={pair['dirtyRulesMatching']} "
                                    f"does not match the RUN.md list")
                for rule, marker, _ in pair["dirty"]:
                    if direction_of(rule) is None:
                        warnings.append(f"config{f} -> config{t}: no direction for the rule {rule}")
                    if marker == "~":
                        warnings.append(f"config{f} -> config{t}: {rule} is dirty by hash, not counted "
                                        f"as added or removed")
            affected = read_affected(cell)
            if affected is not None:
                pair["subtree"], pair["umlElements"], missing = subtrees(
                    runs / "baselines" / f"config{f}" / "model" / "library.uml", affected)
                for path in missing:
                    warnings.append(f"config{f} -> config{t}: the affected element {path} is not in the baseline")
                if len(affected) != pair["affectedElements"]:
                    warnings.append(f"config{f} -> config{t}: affectedElements={pair['affectedElements']} but "
                                    f"{len(affected)} listed in RUN.md")
                if pair["umlElements"] != pair["sourceElements"]:
                    warnings.append(f"config{f} -> config{t}: the baseline UML model holds {pair['umlElements']} "
                                    f"elements, sourceElements={pair['sourceElements']}")
            rules_of[f].add(pair["rulesPersisted"])
            rules_of[t].add(pair["rulesCurrent"])
            pairs[(f, t)] = pair

    for n in CONFIGURATIONS:
        if len(rules_of[n]) > 1:
            warnings.append(f"config{n}: seen with the rule counts {sorted(rules_of[n])}")
        for key in ("modelElements", "sourceElements", "leftOutElements"):
            values = {pair[key] for (f, _), pair in pairs.items() if f == n}
            if len(values) > 1:
                warnings.append(f"config{n}: {key} varies over its row, {sorted(values)}")

    print(f"{len(pairs)} migrated pairs; {diagonals} diagonal cells with identical rules, "
          f"where the migration stops before selecting anything")

    # -- per pair
    print()
    print("== per pair: rules persisted -> current (union); dirty (added/removed, matching); dirty share of"
          " persisted/current/union; affected (matched + referrers) with the share of the elements in the"
          " models and of the source elements probed; elements inside the affected subtrees; left out")
    for (f, t), p in pairs.items():
        tag = "  [fell back]" if p["fellBack"] else ""
        subtree = (f"subtrees {p['subtree']:>2} of {p['umlElements']} UML elements "
                   f"({p['subtree'] / p['umlElements']:>5.1%})  ") if "subtree" in p else ""
        print(f"config{f} -> config{t}: rules {p['rulesPersisted']:>3} -> {p['rulesCurrent']:>3} "
              f"(union {p['union']:>3})  dirty {p['dirtyRules']:>2} (+{p['dirtyRulesAdded']:>2}"
              f"/-{p['dirtyRulesRemoved']:>2}, {p['dirtyRulesMatching']:>2} matching)  "
              f"share {p['dirtyRules'] / p['rulesPersisted']:>5.1%}/{p['dirtyRules'] / p['rulesCurrent']:>5.1%}"
              f"/{p['dirtyRules'] / p['union']:>5.1%}  "
              f"affected {p['affectedElements']:>2} ({p['matchedElements']:>2} matched + "
              f"{p['referrerElements']} referrer(s))  "
              f"{p['affectedElements'] / p['modelElements']:>5.2%} of {p['modelElements']:>3} elements, "
              f"{p['affectedElements'] / p['sourceElements']:>5.1%} of {p['sourceElements']} probed  "
              f"{subtree}left out {p['leftOutElements']}{tag}")

    # -- per source configuration
    print()
    print("== per source configuration: the denominators, constant over its row")
    for n in CONFIGURATIONS:
        row = [pair for (f, _), pair in pairs.items() if f == n]
        if not row:
            continue
        print(f"config{n}: rules {sorted(rules_of[n])[0]:>3}  "
              f"model elements {row[0]['modelElements']:>3}  "
              f"source elements {row[0]['sourceElements']:>2}  "
              f"left out {row[0]['leftOutElements']:>2}")

    # -- the from/to grid
    print()
    print("== dirty rules / affected elements, from (rows) x to (columns)")
    print("         " + "".join(f"{t:>8}" for t in CONFIGURATIONS))
    for f in CONFIGURATIONS:
        cells = []
        for t in CONFIGURATIONS:
            pair = pairs.get((f, t))
            cells.append("=" if f == t else
                         f"{pair['dirtyRules']}/{pair['affectedElements']}" if pair else "?")
        print(f"config{f:<2} " + "".join(f"{cell:>8}" for cell in cells))

    # -- aggregates
    values = {key: [p[key] for p in pairs.values()] for key in COUNTS + ("union",)}
    dirty_total = sum(values["dirtyRules"])
    matching_total = sum(values["dirtyRulesMatching"])
    affected_total = sum(values["affectedElements"])
    print()
    print(f"== over the {len(pairs)} migrated pairs")
    print(f"dirty rules:                           {dirty_total} in total, per pair "
          f"{median_range(values['dirtyRules'])}; {sum(values['dirtyRulesAdded'])} added, "
          f"{sum(values['dirtyRulesRemoved'])} removed, {matching_total} matching a source element "
          f"({matching_total / dirty_total:.1%} of the dirty)")
    for label, key in (("persisted registry", "rulesPersisted"), ("new specifications", "rulesCurrent"),
                       ("union of both", "union")):
        shares = [p["dirtyRules"] / p[key] for p in pairs.values()]
        print(f"  share of the {label + ':':<21} {percent_summary(shares)} "
              f"({pooled(dirty_total, sum(values[key]))})")
    print(f"  matching a source element per pair:  {median_range(values['dirtyRulesMatching'])}")
    matching_shares = [p["dirtyRulesMatching"] / p["union"] for p in pairs.values()]
    print(f"  matching share of the union:         {percent_summary(matching_shares)} "
          f"({pooled(matching_total, sum(values['union']))})")
    print(f"affected elements:                     {affected_total} in total, per pair "
          f"{median_range(values['affectedElements'])}; {sum(values['matchedElements'])} matched, "
          f"{sum(values['referrerElements'])} referrers")
    model_shares = [p["affectedElements"] / p["modelElements"] for p in pairs.values()]
    print(f"  share of the elements in the models: {percent_summary(model_shares, 2)} "
          f"({pooled(affected_total, sum(values['modelElements']), 2)})")
    source_shares = [p["affectedElements"] / p["sourceElements"] for p in pairs.values()]
    print(f"  share of the source elements probed: {percent_summary(source_shares)} "
          f"({pooled(affected_total, sum(values['sourceElements']))})")
    resolved = [p for p in pairs.values() if "subtree" in p]
    if resolved:
        subtree_counts = [p["subtree"] for p in resolved]
        subtree_shares = [p["subtree"] / p["umlElements"] for p in resolved]
        print(f"elements inside the affected subtrees: {sum(subtree_counts)} in total, per pair "
              f"{median_range(subtree_counts)}")
        print(f"  share of the UML model:              {percent_summary(subtree_shares)} "
              f"({pooled(sum(subtree_counts), sum(p['umlElements'] for p in resolved))})")
        small = [f"config{f}->config{t}" for (f, t), p in pairs.items()
                 if "subtree" in p and p["subtree"] / p["umlElements"] <= 0.10]
        print(f"  pairs with at least half of the UML model: "
              f"{sum(1 for share in subtree_shares if share >= 0.5)} of {len(resolved)}")
        print(f"  pairs with at most 10% of the UML model:   {len(small)}: {' '.join(small)}")
    print(f"elements left out:                     {sum(values['leftOutElements'])} in total, per pair "
          f"{median_range(values['leftOutElements'])}")
    print(f"registries per pair:                   persisted {median_range(values['rulesPersisted'])}, "
          f"current {median_range(values['rulesCurrent'])}, union {median_range(values['union'])}")
    print(f"model elements per pair:               {median_range(values['modelElements'])}")

    # -- dirty rules by direction
    print()
    listed = [p for p in pairs.values() if p["dirty"] is not None]
    header = "== dirty rules by direction over the pairs"
    if len(listed) < len(pairs):
        header += f" (only {len(listed)} pairs have the RUN.md list)"
    print(header)
    tallies = defaultdict(Counter)
    names = defaultdict(set)
    for p in listed:
        for rule, marker, matches in p["dirty"]:
            direction = direction_of(rule) or "unknown"
            names[direction].add(rule)
            tallies[direction]["dirty"] += 1
            tallies[direction]["added" if marker == "+" else "removed" if marker == "-" else "changed"] += 1
            tallies[direction]["matching" if matches > 0 else "matching none"] += 1
    for direction in sorted(tallies) + ["all"]:
        tally = (Counter() if direction == "all" else tallies[direction])
        if direction == "all":
            for counter in tallies.values():
                tally.update(counter)
        distinct = len(set().union(*names.values())) if direction == "all" else len(names[direction])
        print(f"{direction + ':':<10} {distinct:>2} distinct rules, {tally['dirty']:>3} dirty "
              f"({tally['added']} added, {tally['removed']} removed), {tally['matching']:>3} matching a "
              f"source element, {tally['matching none']:>3} matching none")

    # -- symmetry of the unordered pairs
    print()
    print("== the two directions of each unordered pair")
    quantities = (("dirty rules", "dirtyRules"), ("union of the registries", "union"),
                  ("affected elements", "affectedElements"),
                  ("dirty rules matching a source element", "dirtyRulesMatching"))
    unordered = [(f, t) for f in CONFIGURATIONS for t in CONFIGURATIONS
                 if f < t and (f, t) in pairs and (t, f) in pairs]
    for label, key in quantities:
        differing = [(f, t) for f, t in unordered if pairs[(f, t)][key] != pairs[(t, f)][key]]
        if not differing:
            print(f"{label}: identical in all {len(unordered)} pairs")
        else:
            print(f"{label}: identical in {len(unordered) - len(differing)} pairs, "
                  f"{len(differing)} differ")
            for f, t in differing:
                print(f"  config{f} <-> config{t}: {pairs[(f, t)][key]} vs {pairs[(t, f)][key]}")

    if warnings:
        print()
        print("== warnings")
        for warning in warnings:
            print("  " + warning, file=sys.stderr)


if __name__ == "__main__":
    main()
