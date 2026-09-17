#!/usr/bin/env python3
"""compare-migrated-models.py -- Compare every migrated V-SUM of the configuration
matrix with the derivation from scratch of its target configuration (M2.1), and
the registries of the two configurations of every pair (M3.3).

For every ordered pair of different configurations, the migrated cell
thesis/examples/library/runs/config<F>-to-config<T> is compared with
runs/baselines/config<T>, the library example that the rules of config<T> derive
in an empty V-SUM. The UML model (model/library.uml) and the Java files
(src/**/*.java) are compared at four levels, each relaxing the one before:

  exact           after every xmi:id is replaced by a label built from the
                  containment path of its element, the UML trees and all Java
                  files are identical
  body            the body of Member.totalWeight(), the handwritten content that
                  --preserve report never puts back, is left out on both sides
  modifier order  the modifiers of a Java declaration are compared in a fixed order
  member order    the imports and the members of a Java type, and the packaged
                  elements, attributes, operations, generalizations and interface
                  realizations of the UML model are compared as sets; parameters,
                  enumeration literals and the statements of a body keep their order

A cell is equivalent at the first level at which nothing differs. For the cells
that still differ at the last level, the script names the differing classifiers,
paired by name without the I prefix and the Impl suffix, and charges the differing
places, read with classify-inconsistencies.py, to the feature that left them
behind. The result is cross-checked against correspondenceDeviations of
cell.properties.

The registries consistencymetadata/vitruv/rule-hashes.txt (one line
ruleId|hash|trigger per rule) are compared per pair: the source derivation's
against the target derivation's, split into added, removed and shared identifiers
and shared identifiers whose hash or trigger differs, and the migrated cell's
against the target derivation's.

Usage: compare-migrated-models.py <thesis/examples/library>
"""

import importlib.util
import json
import re
import statistics
import sys
import xml.etree.ElementTree as ET
from collections import Counter, OrderedDict
from pathlib import Path

CONFIGURATIONS = range(1, 10)
LEVELS = ("exact", "body", "modifier order", "member order")
XMI_ID = "{http://www.omg.org/spec/XMI/20131001}id"
XMI_TYPE = "{http://www.omg.org/spec/XMI/20131001}type"
UNORDERED_UML = {"packagedElement", "ownedAttribute", "ownedOperation", "generalization", "interfaceRealization"}
MODIFIERS = ["public", "protected", "private", "abstract", "static", "final",
             "synchronized", "native", "strictfp", "default"]


def load_classifier():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location(
        "classify_inconsistencies", Path(__file__).with_name("classify-inconsistencies.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ci = load_classifier()

# ---------------------------------------------------------------- UML

def local(tag):
    return tag.split("}", 1)[-1]


def uml_parts(path, ordered):
    """The canonical tree of every element directly below the catalog package, keyed
    by its name, plus the rest of the model under "(model)" and, when order counts,
    the order of the catalog under "(catalog order)"."""
    root = ET.parse(path).getroot()
    labels = {}

    def assign(element, label):
        if XMI_ID in element.attrib:
            labels[element.get(XMI_ID)] = label
        seen = Counter()
        for child in element:
            key = f"{label}/{local(child.tag)}[{child.get(XMI_TYPE, '')}:{child.get('name', '')}]"
            seen[key] += 1
            assign(child, key if seen[key] == 1 else f"{key}#{seen[key]}")

    assign(root, "")

    def canonical(element):
        attributes = []
        for key, value in sorted(element.attrib.items()):
            if key == XMI_ID:
                continue
            tokens = value.split()
            if tokens and all(token in labels for token in tokens):
                value = " ".join(labels[token] for token in tokens)
            attributes.append((local(key), value))
        children = [(local(child.tag), canonical(child)) for child in element]
        if not ordered:
            children = ([c for c in children if c[0] not in UNORDERED_UML]
                        + sorted(c for c in children if c[0] in UNORDERED_UML))
        return local(element.tag), tuple(attributes), tuple(children)

    parts, rest, order = {}, [], []
    for child in root:
        if local(child.tag) == "packagedElement" and child.get("name") == "catalog":
            for element in child:
                name = element.get("name", local(element.tag))
                parts[name] = canonical(element)
                order.append(name)
        else:
            rest.append(canonical(child))
    parts["(model)"] = tuple(rest if ordered else sorted(rest))
    if ordered:
        parts["(catalog order)"] = tuple(order)
    return parts

# ---------------------------------------------------------------- Java

def java_sources(folder):
    source = folder / "src"
    return {str(path.relative_to(source)).replace("\\", "/"): path.read_text(encoding="utf-8").replace("\r\n", "\n")
            for path in sorted(source.rglob("*.java"))}


def without_hand_written_body(text):
    lines, out, i = text.split("\n"), [], 0
    while i < len(lines):
        out.append(lines[i])
        if "totalWeight(" in lines[i] and lines[i].rstrip().endswith("{"):
            depth, i = 1, i + 1
            while i < len(lines) and depth > 0:
                depth += lines[i].count("{") - lines[i].count("}")
                if depth > 0:
                    i += 1
            continue
        i += 1
    return "\n".join(out)


def with_sorted_modifiers(text):
    def sort(match):
        tokens = " ".join(sorted(match.group(1).split(), key=MODIFIERS.index))
        return match.group(0).replace(match.group(1), tokens + " ")
    return re.sub(r"^\s*((?:(?:" + "|".join(MODIFIERS) + r")\s+){2,})", sort, text, flags=re.M)


def normalized(chars):
    return "\n".join(line.strip() for line in "".join(chars).split("\n") if line.strip())


def java_structure(text):
    """Package, imports as a set, the type header, and the members of the type as a
    set. A member keeps its own text, the enumeration literals are one member."""
    head, _, body = text.partition("{")
    lines = [line.strip() for line in head.split("\n") if line.strip()]
    package = tuple(line for line in lines if line.startswith("package "))
    imports = tuple(sorted(line for line in lines if line.startswith("import ")))
    header = " ".join(line for line in lines if not line.startswith(("package ", "import ")))
    members, current, depth = [], [], 1
    for char in body:
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                break
        current.append(char)
        if depth == 1 and char in ";}":
            member = normalized(current)
            if member:
                members.append(member)
            current = []
    tail = normalized(current)
    if tail:
        members.append(tail)
    return package, imports, header, tuple(sorted(members))


def java_view(sources, level):
    view = {}
    for name, text in sources.items():
        if level >= 1:
            text = without_hand_written_body(text)
        if level >= 2:
            text = with_sorted_modifiers(text)
        view[name] = java_structure(text) if level >= 3 else text
    return view

# ---------------------------------------------------------------- comparison

def differing(cell, baseline, level):
    """The canonical names of the classifiers that differ at a level."""
    names = set()
    uml_a = uml_parts(cell / "model" / "library.uml", ordered=level < 3)
    uml_b = uml_parts(baseline / "model" / "library.uml", ordered=level < 3)
    for key in set(uml_a) | set(uml_b):
        if uml_a.get(key) != uml_b.get(key):
            names.add(key if key.startswith("(") else ci.canonical(key))
    java_a, java_b = java_view(java_sources(cell), level), java_view(java_sources(baseline), level)
    for path in set(java_a) | set(java_b):
        if java_a.get(path) != java_b.get(path):
            stem = Path(path).stem
            names.add("(package-info)" if stem == "package-info" else ci.canonical(stem))
    return names


def lost_body(item):
    return item.cls == "body" and item.element.startswith("totalWeight") and item.detail.startswith("(empty) instead of")


def places(cell, baseline, delta):
    items = (ci.compare("UML", ci.parse_uml(cell / "model" / "library.uml"), ci.parse_uml(baseline / "model" / "library.uml"))
             + ci.compare("Java", ci.parse_java(cell / "src" / "catalog"), ci.parse_java(baseline / "src" / "catalog")))
    uml_visibility = {(ci.canonical(i.classifier), i.element) for i in items if i.side == "UML" and i.cls == "visibility"}
    for item in items:
        item.feature = ci.feature_of(item, delta, uml_visibility)
        # A default constructor that an interface realization or a renamed class turned into
        # an ordinary member named after its classifier is a remain of ConstructorCreation.
        if (item.feature == "?" and item.cls.endswith("member")
                and ci.canonical(item.element.split("(")[0]) == ci.canonical(item.classifier)):
            item.feature = "ConstructorCreation"
    return [item for item in items if not lost_body(item)]


def read_properties(path):
    values = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    return values


def registry(folder):
    rules = {}
    for line in (folder / "consistencymetadata" / "vitruv" / "rule-hashes.txt").read_text(encoding="utf-8").splitlines():
        if line.strip():
            rule, hash_value, trigger = line.split("|", 2)
            rules[rule] = (hash_value, trigger)
    return rules


def median_range(values):
    return f"{statistics.median(values):g} ({min(values)}-{max(values)})"

# ---------------------------------------------------------------- main

def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    library = Path(sys.argv[1])
    runs = library / "runs"
    baselines = runs / "baselines"
    selections = {n: set(json.loads((library / "rules" / f"config{n}.json").read_text())) for n in CONFIGURATIONS}

    results = OrderedDict()
    for f in CONFIGURATIONS:
        for t in CONFIGURATIONS:
            if f == t:
                continue
            cell, baseline = runs / f"config{f}-to-config{t}", baselines / f"config{t}"
            per_level = [differing(cell, baseline, level) for level in range(len(LEVELS))]
            first = next((level for level, names in enumerate(per_level) if not names), None)
            remaining = places(cell, baseline, selections[f] ^ selections[t])
            results[(f, t)] = {
                "levels": per_level,
                "first": first,
                "places": remaining,
                "tool": int(read_properties(cell / "cell.properties")["correspondenceDeviations"]),
            }

    print("== per cell: the classifiers that differ from the derivation from scratch at each level; first level without a difference")
    for (f, t), result in results.items():
        counts = " ".join(f"{len(names):>2}" for names in result["levels"])
        first = LEVELS[result["first"]] if result["first"] is not None else "-"
        last = ", ".join(sorted(result["levels"][-1])) or "none"
        print(f"config{f} -> config{t}: {counts}   equivalent at: {first:<14}  still differing: {last}")

    print()
    print("== equivalent cells over the 72 migrated pairs, cumulative per level")
    for level, name in enumerate(LEVELS):
        cells = [key for key, result in results.items() if result["first"] is not None and result["first"] <= level]
        print(f"  {name:<15} {len(cells):>2}")
    for level, name in enumerate(LEVELS):
        cells = [f"{f}->{t}" for (f, t), result in results.items() if result["first"] == level]
        print(f"  first equivalent at {name:<15} {len(cells):>2}: {' '.join(cells)}")

    print()
    print("== differing classifiers at the last level, from (rows) x to (columns)")
    print("        " + "".join(f"{t:>4}" for t in CONFIGURATIONS))
    for f in CONFIGURATIONS:
        row = []
        for t in CONFIGURATIONS:
            row.append("   =" if f == t else f"{len(results[(f, t)]['levels'][-1]):>4}")
        print(f"config{f}" + "".join(row))

    print()
    print("== deviation classes: the features whose places remain after the migration (the lost totalWeight body excluded)")
    classes = OrderedDict()
    for (f, t), result in results.items():
        by_feature = OrderedDict()
        for item in result["places"]:
            by_feature.setdefault(item.feature, []).append(item)
        for feature, items in by_feature.items():
            entry = classes.setdefault(feature, {"cells": [], "classifiers": [], "classes": Counter(), "details": Counter()})
            entry["cells"].append(f"{f}->{t}")
            entry["classifiers"].append(len({ci.canonical(i.classifier) for i in items}))
            for item in items:
                entry["classes"][f"{item.side} {item.cls}"] += 1
                entry["details"][f"{item.side} {item.classifier}.{item.element}: {item.detail}"] += 1
    for feature, entry in classes.items():
        print(f"-- {feature}: {len(entry['cells'])} cells, classifiers per cell {median_range(entry['classifiers'])}")
        print(f"   cells: {' '.join(entry['cells'])}")
        for name, count in entry["classes"].most_common():
            print(f"   {count:>4}  {name}")
        for detail, count in entry["details"].most_common():
            print(f"   {count:>4}x {detail[:150]}")

    print()
    print("== cross-checks")
    no_places = [f"{f}->{t}" for (f, t), r in results.items() if r["levels"][-1] and not r["places"]]
    no_files = [f"{f}->{t}" for (f, t), r in results.items() if not r["levels"][-1] and r["places"]]
    print(f"  differing at the last level without a differing place: {len(no_places)} {' '.join(no_places)}")
    print(f"  a differing place without a difference at the last level: {len(no_files)} {' '.join(no_files)}")
    disagreements = [(key, r) for key, r in results.items() if len(r["levels"][-1]) != r["tool"]]
    print(f"  correspondenceDeviations of cell.properties differs from the last level in {len(disagreements)} cells")
    for (f, t), r in disagreements:
        print(f"    config{f} -> config{t}: correspondenceDeviations={r['tool']}, last level {len(r['levels'][-1])} "
              f"({', '.join(sorted(r['levels'][-1])) or 'none'}), first equivalent at "
              f"{LEVELS[r['first']] if r['first'] is not None else '-'}")
    tool_equivalent = sum(1 for r in results.values() if r["tool"] == 0)
    print(f"  cells with correspondenceDeviations=0: {tool_equivalent}")

    print()
    print("== registries: source derivation against target derivation, and the migrated cell against the target derivation")
    registries = {n: registry(baselines / f"config{n}") for n in CONFIGURATIONS}
    totals = Counter()
    per_pair_dirty = []
    for (f, t) in results:
        persisted, current = registries[f], registries[t]
        added, removed = set(current) - set(persisted), set(persisted) - set(current)
        shared = set(current) & set(persisted)
        totals["added"] += len(added)
        totals["removed"] += len(removed)
        totals["shared"] += len(shared)
        totals["shared with a differing hash"] += sum(1 for r in shared if current[r][0] != persisted[r][0])
        totals["shared with a differing trigger"] += sum(1 for r in shared if current[r][1] != persisted[r][1])
        totals["cells whose registry equals the target derivation's"] += registry(runs / f"config{f}-to-config{t}") == current
        per_pair_dirty.append(len(added) + len(removed))
    for key, value in totals.items():
        print(f"  {key:<52} {value}")
    print(f"  added plus removed per pair                          {median_range(per_pair_dirty)}")
    union = set().union(*(set(r) for r in registries.values()))
    common = set.intersection(*(set(r) for r in registries.values()))
    print(f"  rules in any of the nine registries                  {len(union)}")
    print(f"  rules in all nine registries                         {len(common)}")
    print(f"  rules in some but not all                            {len(union) - len(common)}")


if __name__ == "__main__":
    main()
