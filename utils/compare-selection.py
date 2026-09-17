#!/usr/bin/env python3
"""compare-selection.py -- Compare what the selective migration reports as dirty
rules and affected elements with the places that actually differ from a
derivation from scratch (M3.2).

Usage: compare-selection.py <thesis/examples/library>

For every migrated cell runs/config<F>-to-config<T> the reported side is read
from the cell's RUN.md (the dirty rules with the number of source elements each
trigger matched, the affected elements with the rules that matched them or the
selected element they reference, the elements left out) and cell.properties.
The actual side is the M3.1 comparison of classify-inconsistencies.py: every
place in which baselines/config<F> differs from baselines/config<T>, with its
class. The same comparison between the migrated cell and baselines/config<T>
says which of these places the migration resolved; the hand-written body of
Member.totalWeight, which the report policy of the cells never puts back, is
left out of that comparison.

Every place belongs to a classifier and, below it, to the element that owns it:
the classifier itself for its name, kind, modifiers and literals, a
generalization, interface realization or import for a reference, the attribute
for attribute places and for the accessors derived from it, the operation for
operation places, the classifier for a constructor the source configuration has
no operation for. A place counts as selected by the classifier when the whole
classifier is an affected element, by its owner when the owning element is, and
by a sibling when another element of the same classifier is. An affected
element is justified when a place lies in what it stands for, and it lies in a
differing classifier when the classifier holds places elsewhere. Prints the
coverage per inconsistency class, the per-pair table, recall and precision over
the pairs, the affected elements no place justifies, the dirty rules that never
match anything, the places no selection reaches and the selected places that
still differ after the migration.
"""

import importlib.util
import re
import statistics
import sys
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

CONFIGURATIONS = range(1, 10)
CLASSIFIER_CLASSES = {"classifier name", "classifier kind", "classifier modifier", "missing classifier",
                      "surplus classifier", "literal"}
REFERENCE_ELEMENTS = {"supertype", "realization", "import"}
# The place a sub-element of a classifier stands for, by the metaclass the report names.
SUB_ELEMENTS = {"uml::InterfaceRealization": "realization", "uml::Generalization": "supertype"}
CLASSIFIERS = {"uml::Class", "uml::Interface", "uml::Enumeration", "uml::DataType", "uml::PrimitiveType"}
MEMBERS = {"uml::Property", "uml::Operation", "uml::EnumerationLiteral", "uml::Parameter"}
CATEGORIES = ("classifier", "owner", "sibling")
DIRTY_LINE = re.compile(r"^([+\-~]) (\S+)  matches (\d+) source element\(s\)$")
AFFECTED_LINE = re.compile(r"^(\S+)  (\S+)  (matched by (.+)|refers to (\S+))$")
LEFT_OUT_LINE = re.compile(r"^(\S+)  (\S+)  (.+)$")
FRAGMENT = re.compile(r"^library\.uml#/0((?:/[^/]+)*)$")


def load_classifier():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location(
        "classify_inconsistencies", Path(__file__).with_name("classify-inconsistencies.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ci = load_classifier()

# ---------------------------------------------------------------- the reported side

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


class Affected:
    def __init__(self, key, metaclass, matched_by, refers_to):
        self.key = key
        self.metaclass = metaclass
        self.matched_by = matched_by
        self.refers_to = refers_to
        match = FRAGMENT.match(key)
        if match is None:
            raise SystemExit(f"cannot place the affected element {key}")
        segments = match.group(1).split("/")[1:]
        self.package = segments[0] if segments else None
        self.classifier = segments[1] if len(segments) > 1 else None
        self.member = None
        self.sub = None
        if metaclass in CLASSIFIERS:
            pass
        elif metaclass in SUB_ELEMENTS:
            self.sub = SUB_ELEMENTS[metaclass]
        elif metaclass in MEMBERS and len(segments) > 2:
            self.member = segments[2]
        elif metaclass == "uml::Package" and len(segments) == 1:
            self.classifier = None
        else:
            raise SystemExit(f"cannot place the affected element {key} of metaclass {metaclass}")
        self.places = defaultdict(list)

    def is_referrer(self):
        return self.refers_to is not None

    def short(self):
        return self.key.split("#", 1)[1].replace("/0/catalog/", "")

    def selected_by(self):
        return "refers to " + self.refers_to.split("#", 1)[1].replace("/0/catalog/", "") if self.refers_to else "matched by " + ", ".join(self.matched_by)

    def category_for(self, place):
        """How this element's repropagation reaches the place, or None if it does not lie in its classifier."""
        if self.package != "catalog":
            return None
        if self.classifier is None:
            return "classifier"
        if self.classifier != place.classifier:
            return None
        if self.member is None and self.sub is None:
            return "classifier"
        if place.level == "sub" and self.sub == place.owner:
            return "owner"
        if place.level == "member" and self.member == place.owner:
            return "owner"
        return "sibling"

    def justified(self):
        return bool(self.places["classifier"] or self.places["owner"])

    def in_differing_classifier(self):
        return not self.justified() and bool(self.places["sibling"])


def read_selection(cell):
    """Dirty rules, affected elements and left-out elements of a cell's RUN.md, or None without the section."""
    text = (cell / "RUN.md").read_text(encoding="utf-8")
    start = text.find("## What the rule diff and the trigger mechanism found")
    if start < 0:
        return None
    end = text.find("\n## ", start + 1)
    blocks = fenced_blocks(text[start:end])
    dirty = []
    for line in blocks.get("Dirty rules", []):
        match = DIRTY_LINE.match(line)
        if match is None:
            raise SystemExit(f"{cell.name}: cannot read the dirty rule line {line!r}")
        dirty.append((match.group(2), match.group(1), int(match.group(3))))
    affected = []
    for line in blocks.get("Affected elements", []):
        match = AFFECTED_LINE.match(line)
        if match is None:
            raise SystemExit(f"{cell.name}: cannot read the affected element line {line!r}")
        matched_by = [rule.strip() for rule in match.group(4).split(",")] if match.group(4) else []
        affected.append(Affected(match.group(1), match.group(2), matched_by, match.group(5)))
    left_out = []
    for line in blocks.get("Left out", []):
        match = LEFT_OUT_LINE.match(line)
        if match is None:
            raise SystemExit(f"{cell.name}: cannot read the left-out line {line!r}")
        left_out.append(match.groups())
    return dirty, affected, left_out

# ---------------------------------------------------------------- the actual side

def compare_models(uml_a, java_a, uml_b, java_b, delta):
    items = ci.compare("UML", uml_a, uml_b) + ci.compare("Java", java_a, java_b)
    uml_visibility = {(ci.canonical(i.classifier), i.element) for i in items if i.side == "UML" and i.cls == "visibility"}
    for item in items:
        item.feature = ci.feature_of(item, delta, uml_visibility)
    return items


def merged_class(cls):
    return re.sub(r"^(surplus|missing) ", "", cls)


def lost_body(item):
    """The hand-written body the report policy of the cells never puts back."""
    return item.cls == "body" and item.element.startswith("totalWeight") and item.detail.startswith("(empty) instead of")


def canonical_key(item):
    """A place's key with the prefix and suffix a feature adds stripped from every name, so a
    place survives the rename of its classifier between the ground truth and the residual."""
    return f"{item.side} {ci.canonical(item.classifier)}.{ci.canonical_text(item.element)}: {ci.canonical_text(item.detail)}"


def place_owner(item, uml_source):
    """(level, owner) of a place: the classifier, a sub-element named by what it references, or a member."""
    if item.cls in CLASSIFIER_CLASSES:
        return "classifier", None
    if item.element in REFERENCE_ELEMENTS:
        return "sub", item.element
    element = item.element
    if "(" not in element:
        return "member", element
    name = element.split("(")[0]
    classifier = uml_source.get(item.classifier)
    attributes = set(classifier["attributes"]) if classifier else set()
    for prefix in ("get", "set"):
        if name.startswith(prefix) and len(name) > 3:
            field = name[3].lower() + name[4:]
            if field in attributes:
                return "member", field
    if name in (ci.canonical(item.classifier), item.classifier):
        operations = classifier["operations"] if classifier else {}
        if any(op["name"] == name for op in operations.values()):
            return "member", name
        return "classifier", None
    return "member", name


def trigger_types(library):
    """The metaclass each rule's trigger reacts to, from the persisted registries of the baselines."""
    types = {}
    for n in CONFIGURATIONS:
        registry = library / "runs" / "baselines" / f"config{n}" / "consistencymetadata" / "vitruv" / "rule-hashes.txt"
        for line in registry.read_text(encoding="utf-8").splitlines():
            rule, _, trigger = line.split("|", 2)
            parts = trigger.split(";")
            types[rule] = (parts[0] + " " + parts[1].split("#")[-1]) if len(parts) > 1 else "?"
    return types

# ---------------------------------------------------------------- main

def median_range(values, digits=0):
    if not values:
        return "-"
    fmt = f"{{:.{digits}f}}"
    return f"{fmt.format(statistics.median(values))} ({fmt.format(min(values))}-{fmt.format(max(values))})"


def percent_summary(values):
    return f"median {statistics.median(values):.1%}, range {min(values):.1%}-{max(values):.1%}"


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    library = Path(sys.argv[1])
    runs = library / "runs"
    baselines = runs / "baselines"
    uml = {n: ci.parse_uml(baselines / f"config{n}" / "model" / "library.uml") for n in CONFIGURATIONS}
    java = {n: ci.parse_java(baselines / f"config{n}" / "src" / "catalog") for n in CONFIGURATIONS}
    selections = {n: set(ci.json.loads((library / "rules" / f"config{n}.json").read_text())) for n in CONFIGURATIONS}
    triggers = trigger_types(library)

    warnings = []
    pairs = OrderedDict()
    for f in CONFIGURATIONS:
        for t in CONFIGURATIONS:
            if f == t:
                continue
            cell = runs / f"config{f}-to-config{t}"
            if not (cell / "cell.properties").is_file():
                warnings.append(f"config{f} -> config{t}: not generated, skipped")
                continue
            properties = read_properties(cell / "cell.properties")
            if properties.get("outcome") != "migrated":
                warnings.append(f"config{f} -> config{t}: outcome {properties.get('outcome')}, skipped")
                continue
            selection = read_selection(cell)
            if selection is None:
                warnings.append(f"config{f} -> config{t}: RUN.md has no selection section, skipped")
                continue
            dirty, affected, left_out = selection
            delta = selections[f] ^ selections[t]
            places = compare_models(uml[f], java[f], uml[t], java[t], delta)
            cell_uml = ci.parse_uml(cell / "model" / "library.uml")
            cell_java = ci.parse_java(cell / "src" / "catalog")
            residual = {canonical_key(i) for i in compare_models(cell_uml, cell_java, uml[t], java[t], delta) if not lost_body(i)}
            introduced = residual - {canonical_key(i) for i in places}

            for place in places:
                place.level, place.owner = place_owner(place, uml[f])
                place.resolved = canonical_key(place) not in residual
                categories = set()
                for a in affected:
                    category = a.category_for(place)
                    if category:
                        categories.add(category)
                        a.places[category].append(place)
                place.category = next((c for c in CATEGORIES if c in categories), None)

            if int(properties["dirtyRules"]) != len(dirty) or int(properties["dirtyRules"]) != int(properties["dirtyRulesAdded"]) + int(properties["dirtyRulesRemoved"]):
                warnings.append(f"config{f} -> config{t}: dirtyRules={properties['dirtyRules']} but {len(dirty)} listed, {properties['dirtyRulesAdded']} added + {properties['dirtyRulesRemoved']} removed")
            if int(properties["affectedElements"]) != len(affected):
                warnings.append(f"config{f} -> config{t}: affectedElements={properties['affectedElements']} but {len(affected)} listed")
            if int(properties["leftOutElements"]) != len(left_out):
                warnings.append(f"config{f} -> config{t}: leftOutElements={properties['leftOutElements']} but {len(left_out)} listed")
            if bool(residual) != (int(properties["correspondenceDeviations"]) > 0):
                warnings.append(f"config{f} -> config{t}: {len(residual)} place(s) still differ but correspondenceDeviations={properties['correspondenceDeviations']}")
            if introduced:
                warnings.append(f"config{f} -> config{t}: {len(introduced)} place(s) differ after the migration that did not differ before: {sorted(introduced)[:3]}")

            pairs[(f, t)] = {
                "properties": properties, "dirty": dirty, "affected": affected, "left_out": left_out,
                "places": places, "delta": delta, "introduced": introduced,
            }

    # -- per class over the pairs
    classes = OrderedDict()
    totals = Counter()
    for (f, t), pair in pairs.items():
        for place in pair["places"]:
            entry = classes.setdefault(merged_class(place.cls), Counter())
            entry["pairs:" + f"{f}>{t}"] = 1
            keys = ["places", place.category or "not selected", "resolved" if place.resolved else "remaining",
                    ("selected" if place.category else "not selected") + ("/resolved" if place.resolved else "/remaining")]
            for key in keys:
                entry[key] += 1
                totals[key] += 1

    columns = ["places", "classifier", "owner", "sibling", "not selected", "resolved", "remaining",
               "selected/resolved", "selected/remaining", "not selected/resolved", "not selected/remaining"]
    print("== coverage per inconsistency class over the migrated pairs (selected by the whole classifier, by the owning element, by a sibling element of the classifier, or not at all; resolved after the migration or remaining; the selected x resolved cross-tab)")
    print(f"{'class':<32} {'pairs':>5} {'places':>6} {'classif':>7} {'owner':>5} {'siblng':>6} {'notsel':>6} {'resolv':>6} {'remain':>6}  sel/res sel/rem nsel/res nsel/rem")
    for cls, entry in sorted(classes.items(), key=lambda e: -e[1]["places"]):
        npairs = sum(1 for k in entry if k.startswith("pairs:"))
        values = [entry[c] for c in columns]
        print(f"{cls:<32} {npairs:>5} {values[0]:>6} {values[1]:>7} {values[2]:>5} {values[3]:>6} {values[4]:>6} {values[5]:>6} {values[6]:>6}  {values[7]:>7} {values[8]:>7} {values[9]:>8} {values[10]:>8}")
    values = [totals[c] for c in columns]
    print(f"{'all':<32} {len(pairs):>5} {values[0]:>6} {values[1]:>7} {values[2]:>5} {values[3]:>6} {values[4]:>6} {values[5]:>6} {values[6]:>6}  {values[7]:>7} {values[8]:>7} {values[9]:>8} {values[10]:>8}")

    # -- per pair
    print()
    print("== per pair: dirty rules added/removed/matching; affected matched/referrers; places selected/all = recall; affected justified/in a differing classifier/without any difference; resolved/remaining; differing classifiers")
    recalls, precisions, affected_counts, classifier_counts = [], [], [], []
    full_recall = full_precision = 0
    for (f, t), pair in pairs.items():
        p = pair["properties"]
        places = pair["places"]
        selected = sum(1 for place in places if place.category)
        justified = sum(1 for a in pair["affected"] if a.justified())
        differing = sum(1 for a in pair["affected"] if a.in_differing_classifier())
        resolved = sum(1 for place in places if place.resolved)
        classifiers = {place.classifier for place in places}
        recall = selected / len(places) if places else 1.0
        precision = justified / len(pair["affected"]) if pair["affected"] else 1.0
        recalls.append(recall)
        precisions.append(precision)
        affected_counts.append(len(pair["affected"]))
        classifier_counts.append(len(classifiers))
        full_recall += recall == 1.0
        full_precision += precision == 1.0
        matched = sum(1 for a in pair["affected"] if not a.is_referrer())
        print(f"config{f} -> config{t}: dirty {p['dirtyRulesAdded']:>2}/{p['dirtyRulesRemoved']:>2}/{p['dirtyRulesMatching']:>2}  affected {matched:>2}/{len(pair['affected']) - matched:>2}  places {selected:>3}/{len(places):>3} = {recall:6.1%}  justified {justified:>2}/{differing:>2}/{len(pair['affected']) - justified - differing:>2} of {len(pair['affected']):>2}  resolved {resolved:>3}/{len(places) - resolved:>3}  classifiers {len(classifiers):>2}")

    print()
    print("== over the pairs")
    print(f"recall (places selected / places):                {percent_summary(recalls)}, {full_recall} of {len(pairs)} pairs complete")
    print(f"precision (justified / affected elements):         {percent_summary(precisions)}, {full_precision} of {len(pairs)} pairs without an unjustified selection")
    print(f"affected elements per pair:                        {median_range(affected_counts)}")
    print(f"classifiers with a differing place per pair:       {median_range(classifier_counts)}")
    all_affected = [a for pair in pairs.values() for a in pair["affected"]]
    print(f"affected elements over the pairs:                  {len(all_affected)}, {sum(1 for a in all_affected if a.justified())} justified, {sum(1 for a in all_affected if a.in_differing_classifier())} in a classifier that differs elsewhere, {sum(1 for a in all_affected if not a.justified() and not a.in_differing_classifier())} without any difference; {sum(1 for a in all_affected if a.is_referrer())} referrers")
    by_direction = Counter()
    for pair in pairs.values():
        for rule, _, matched in pair["dirty"]:
            direction = "javaToUml" if rule.startswith("javaToUml") else "umlToJava"
            by_direction[direction, "dirty"] += 1
            by_direction[direction, "matching"] += matched > 0
    print("dirty rules over the pairs by direction:           " + ", ".join(f"{d} {by_direction[d, 'dirty']} ({by_direction[d, 'matching']} matching a source element)" for d in ("umlToJava", "javaToUml")) + f"; all {sum(v for (d, k), v in by_direction.items() if k == 'dirty')} ({sum(v for (d, k), v in by_direction.items() if k == 'matching')} matching)")

    # -- unjustified selections
    print()
    print("== affected elements no place justifies (times seen over the pairs; * = the classifier differs elsewhere)")
    unjustified = Counter()
    for pair in pairs.values():
        for a in pair["affected"]:
            if not a.justified():
                unjustified[(a.metaclass, a.short(), a.selected_by(), "*" if a.in_differing_classifier() else "")] += 1
    for (metaclass, key, by, star), count in sorted(unjustified.items(), key=lambda e: (-e[1], e[0])):
        print(f"  {count:>3}x {star:1}{metaclass} {key} {by}")
    if not unjustified:
        print("  none")

    # -- dirty rules
    print()
    print("== dirty rules whose trigger never matches a source element (times dirty over the pairs; trigger)")
    never = Counter()
    ever = set()
    matches = defaultdict(lambda: [0, 0])
    for pair in pairs.values():
        for rule, _, matched in pair["dirty"]:
            if matched > 0:
                ever.add(rule)
                matches[rule][0] += 1
                matches[rule][1] += matched
            else:
                never[rule] += 1
    for rule, count in sorted(never.items(), key=lambda e: (e[0].split("::")[0], -e[1], e[0])):
        note = "" if rule not in ever else "  (matches in other pairs)"
        print(f"  {count:>3}x {rule}  {triggers.get(rule, '?')}{note}")
    print()
    print("== dirty rules whose trigger matches (times dirty over the pairs; trigger; elements matched in total)")
    for rule, (count, elements) in sorted(matches.items(), key=lambda e: (e[0].split("::")[0], -e[1][0], e[0])):
        print(f"  {count:>3}x {rule}  {triggers.get(rule, '?')}  {elements} element(s)")

    # -- places no selection reaches
    print()
    print("== places not selected, by class (times seen over the pairs)")
    missed = defaultdict(Counter)
    for pair in pairs.values():
        for place in pair["places"]:
            if not place.category:
                missed[merged_class(place.cls)][f"{place.key()} [{'resolved' if place.resolved else 'remaining'}]"] += 1
    for cls, examples in sorted(missed.items(), key=lambda e: -sum(e[1].values())):
        print(f"-- {cls}: {sum(examples.values())}")
        for example, count in sorted(examples.items(), key=lambda e: (-e[1], e[0])):
            print(f"  {count:>3}x {example}")

    # -- places selected but remaining
    print()
    print("== places selected but still differing after the migration, by class (times seen over the pairs)")
    kept = defaultdict(Counter)
    for pair in pairs.values():
        for place in pair["places"]:
            if place.category and not place.resolved:
                kept[merged_class(place.cls)][f"{place.key()} [{place.category}]"] += 1
    for cls, examples in sorted(kept.items(), key=lambda e: -sum(e[1].values())):
        print(f"-- {cls}: {sum(examples.values())}")
        for example, count in sorted(examples.items(), key=lambda e: (-e[1], e[0])):
            print(f"  {count:>3}x {example}")

    # -- left out
    print()
    print("== elements left out of every selection (times seen over the pairs)")
    left = Counter()
    for pair in pairs.values():
        for key, metaclass, reason in pair["left_out"]:
            left[(metaclass, key.split("#", 1)[1], reason)] += 1
    for (metaclass, key, reason), count in sorted(left.items(), key=lambda e: (-e[1], e[0])):
        print(f"  {count:>3}x {metaclass} {key}: {reason}")

    if warnings:
        print()
        print("== warnings")
        for warning in warnings:
            print("  " + warning, file=sys.stderr)


if __name__ == "__main__":
    main()
