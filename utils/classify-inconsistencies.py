#!/usr/bin/env python3
"""classify-inconsistencies.py -- Classify what a configuration switch leaves
inconsistent in the library example (M3.1).

For every ordered pair of configurations the artifacts derived with the source
configuration (thesis/examples/library/runs/baselines/config<F>) are compared
with the artifacts the target configuration derives from scratch
(baselines/config<T>). Every place where the two disagree is an inconsistency
that switching from F to T leaves behind when the existing artifacts are kept:
the target rules would have derived something else there. Each place is
assigned to exactly one class and to the feature of the switch that causes it,
and the classes are counted over the 72 pairs.

Usage: classify-inconsistencies.py <thesis/examples/library>

Both models are read per classifier of the catalog package: the UML from
model/library.uml (kind, abstractness, finality, generalizations, interface
realizations, attributes with type, visibility, multiplicity and staticness,
operations with parameters, return type, staticness and leafness), the Java from
src/catalog/*.java (kind, modifiers, extends, implements, imports, fields with
modifiers, type and initializer, methods and constructors with modifiers,
signature and body). Classifiers are paired by name after stripping the "I"
prefix of InterfacePrefix and the "Impl" suffix of RealizationSuffix, so a
renamed classifier is one renamed classifier and not one missing plus one
unexpected. References are compared the same way, so a reference that only
follows a rename is told apart from a reference to something else. The feature
selections are read from rules/config<n>.json; the feature an item is charged
to follows from its class, its detail and the features the two selections
differ in (see feature_of).
"""

import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, OrderedDict
from pathlib import Path

XMI = "{http://www.omg.org/spec/XMI/20131001}"
CONFIGURATIONS = range(1, 10)

# ---------------------------------------------------------------- naming

def canonical(name):
    """The name a classifier has without the prefix or suffix a feature added."""
    if name.endswith("Impl") and len(name) > 4:
        name = name[:-4]
    if len(name) > 1 and name[0] == "I" and name[1].isupper():
        name = name[1:]
    return name


def simple(type_text):
    """Qualified Java type text reduced to simple names: ArrayList<Media>."""
    if type_text is None:
        return None
    return re.sub(r"(?:\w+\.)+(\w+)", r"\1", type_text).replace(" ", "")


def canonical_text(text):
    if text is None:
        return None
    return re.sub(r"\w+", lambda m: canonical(m.group(0)), text)


def is_accessor(method_name, field_names):
    for prefix in ("get", "set"):
        if method_name.startswith(prefix) and len(method_name) > 3:
            field = method_name[3].lower() + method_name[4:]
            if field in field_names:
                return True
    return False

# ---------------------------------------------------------------- UML

def parse_uml(path):
    root = ET.parse(path).getroot()
    names = {}
    for element in root.iter():
        if XMI + "id" in element.attrib and "name" in element.attrib:
            names[element.attrib[XMI + "id"]] = element.attrib["name"]

    def type_of(element):
        if "type" in element.attrib:
            return names.get(element.attrib["type"], "?")
        child = element.find("type")
        if child is not None:
            return child.attrib.get("href", "?").split("#")[-1]
        return None

    catalog = next(p for p in root.findall("packagedElement") if p.attrib.get("name") == "catalog")
    classifiers = OrderedDict()
    for element in catalog.findall("packagedElement"):
        name = element.attrib["name"]
        classifier = {
            "kind": element.attrib[XMI + "type"].split(":")[1],
            "abstract": element.attrib.get("isAbstract") == "true",
            "final": element.attrib.get("isFinalSpecialization") == "true",
            "supertypes": [names[g.attrib["general"]] for g in element.findall("generalization")],
            "realizations": [names[r.attrib["contract"]] for r in element.findall("interfaceRealization")],
            "attributes": OrderedDict(),
            "operations": OrderedDict(),
            "literals": [l.attrib["name"] for l in element.findall("ownedLiteral")],
            "imports": [],
        }
        for attribute in element.findall("ownedAttribute"):
            upper = attribute.find("upperValue")
            classifier["attributes"][attribute.attrib["name"]] = {
                "type": type_of(attribute),
                "visibility": attribute.attrib.get("visibility", "public"),
                "static": attribute.attrib.get("isStatic") == "true",
                "final": False,
                "many": upper is not None and upper.attrib.get("value") == "*",
                "initializer": None,
            }
        for operation in element.findall("ownedOperation"):
            parameters = [p for p in operation.findall("ownedParameter") if p.attrib.get("direction") != "return"]
            returns = [type_of(p) for p in operation.findall("ownedParameter") if p.attrib.get("direction") == "return"]
            signature = operation.attrib["name"] + "(" + ",".join(type_of(p) or "?" for p in parameters) + ")"
            classifier["operations"][signature] = {
                "name": operation.attrib["name"],
                "visibility": operation.attrib.get("visibility", "public"),
                "static": operation.attrib.get("isStatic") == "true",
                "final": operation.attrib.get("isLeaf") == "true",
                "abstract": False,
                "return": returns[0] if returns else None,
                "constructor": operation.attrib["name"] == name,
                "bodyless": None,
                "body": None,
            }
        classifiers[name] = classifier
    return classifiers

# ---------------------------------------------------------------- Java

HEADER = re.compile(
    r"^public\s+((?:(?:abstract|final|static)\s+)*)(class|interface|enum|record)\s+(\w+)"
    r"(?:\s+extends\s+([\w.,\s]+?))?(?:\s+implements\s+([\w.,\s]+?))?\s*\{;?",
    re.M,
)
MODIFIERS = r"((?:(?:public|private|protected|static|final|abstract)\s+)*)"
# JaMoPP prints no blank between a generic type and the name it types
# (ArrayList<catalog.Media>borrowed), everywhere else there is one.
TYPE = r"([\w.]+(?:<[\w.]+>)?(?:\[\])?)(?:(?<=>)\s*|\s+)"
FIELD = re.compile(r"^\t" + MODIFIERS + TYPE + r"(\w+)\s*(?:=\s*([^;]+))?;$")
METHOD = re.compile(r"^\t" + MODIFIERS + TYPE + r"(\w+)\((.*?)\)\s*(\{|;)")
CONSTRUCTOR = re.compile(r"^\t" + MODIFIERS + r"(\w+)\((.*?)\)\s*\{")
CONSTANT = re.compile(r"^\t(\w+)\s*[,}]?\s*$")


def split_list(text):
    return [simple(t.strip()) for t in text.split(",") if t.strip()] if text else []


def visibility_in(modifiers):
    return next((m for m in modifiers if m in ("public", "private", "protected")), "package")


def parameter_types(params):
    return [simple(p.strip().rsplit(" ", 1)[0]) for p in params.split(",") if p.strip()]


def parse_java(folder):
    classifiers = OrderedDict()
    for file in sorted(folder.glob("*.java")):
        if file.name == "package-info.java":
            continue
        text = file.read_text(encoding="utf-8")
        header = HEADER.search(text)
        if header is None:
            raise SystemExit(f"{file}: no classifier header found")
        modifiers, kind, name, extends, implements = header.groups()
        modifiers = modifiers.split()
        classifier = {
            "kind": kind,
            "abstract": "abstract" in modifiers,
            "final": "final" in modifiers,
            "supertypes": split_list(extends),
            "realizations": split_list(implements),
            "attributes": OrderedDict(),
            "operations": OrderedDict(),
            "literals": [],
            "imports": [simple(m) for m in re.findall(r"^import\s+([\w.]+);", text, re.M)],
            "file": file.name,
        }
        lines = text[header.end():].splitlines()
        index = 0
        while index < len(lines):
            line = lines[index].rstrip()
            index += 1
            constructor = CONSTRUCTOR.match(line)
            if constructor and constructor.group(2) == name:
                mods, _, params = constructor.groups()
                body, index = read_body(lines, index)
                signature = name + "(" + ",".join(parameter_types(params)) + ")"
                classifier["operations"][signature] = {
                    "name": name,
                    "visibility": visibility_in(mods.split()),
                    "static": False,
                    "final": False,
                    "abstract": False,
                    "return": None,
                    "constructor": True,
                    "bodyless": False,
                    "body": " ".join(body),
                }
                continue
            field = FIELD.match(line)
            if field:
                mods, type_text, field_name, initializer = field.groups()
                mods = mods.split()
                classifier["attributes"][field_name] = {
                    "type": simple(type_text),
                    "visibility": visibility_in(mods),
                    "static": "static" in mods,
                    "final": "final" in mods,
                    "many": "<" in type_text,
                    "initializer": initializer.strip() if initializer else None,
                }
                continue
            method = METHOD.match(line)
            if method:
                mods, return_type, method_name, params, opener = method.groups()
                mods = mods.split()
                body, index = read_body(lines, index) if opener == "{" else ([], index)
                signature = method_name + "(" + ",".join(parameter_types(params)) + ")"
                classifier["operations"][signature] = {
                    "name": method_name,
                    "visibility": visibility_in(mods),
                    "static": "static" in mods,
                    "final": "final" in mods,
                    "abstract": "abstract" in mods,
                    "return": simple(return_type),
                    "constructor": False,
                    "bodyless": opener == ";",
                    "body": " ".join(body),
                }
                continue
            constant = CONSTANT.match(line)
            if constant and kind == "enum":
                classifier["literals"].append(constant.group(1))
        classifiers[name] = classifier
    return classifiers


def read_body(lines, index):
    """Statements of a member body opened on the previous line; returns (lines, next index)."""
    body = []
    depth = 1
    while index < len(lines) and depth > 0:
        line = lines[index]
        index += 1
        depth += line.count("{") - line.count("}")
        stripped = line.strip()
        if depth > 0 and stripped and stripped != "}":
            body.append(stripped)
        elif depth == 0 and stripped not in ("}", "}}"):
            body.append(stripped.rstrip("}").strip())
    return [b for b in body if b], index

# ---------------------------------------------------------------- comparison

class Item:
    def __init__(self, cls, side, classifier, element, detail):
        self.cls = cls
        self.side = side
        self.classifier = classifier
        self.element = element
        self.detail = detail
        self.feature = None

    def key(self):
        return f"{self.side} {self.classifier}.{self.element}: {self.detail}"


def pair_by_canonical(source, target):
    by_canonical_source = {canonical(n): n for n in source}
    by_canonical_target = {canonical(n): n for n in target}
    for key in list(by_canonical_source) + [k for k in by_canonical_target if k not in by_canonical_source]:
        yield key, by_canonical_source.get(key), by_canonical_target.get(key)


def compare(side, source, target):
    items = []
    for key, old_name, new_name in pair_by_canonical(source, target):
        if old_name is None:
            items.append(Item("missing classifier", side, new_name, "", f"the target rules derive {target[new_name]['kind']} {new_name}"))
            continue
        if new_name is None:
            items.append(Item("surplus classifier", side, old_name, "", f"no target rule derives {source[old_name]['kind']} {old_name}"))
            continue
        old, new = source[old_name], target[new_name]
        c = old_name
        if old_name != new_name:
            detail = f"{old_name} instead of {new_name}"
            if side == "Java":
                detail += f" (file {old['file']})"
            items.append(Item("classifier name", side, c, "name", detail))
        if old["kind"] != new["kind"]:
            items.append(Item("classifier kind", side, c, "kind", f"{old['kind']} instead of {new['kind']}"))
        else:
            for flag in ("abstract", "final"):
                if old[flag] != new[flag]:
                    items.append(Item("classifier modifier", side, c, flag, f"{flag}={old[flag]} instead of {new[flag]}"))
        compare_references(items, side, c, "supertype", old["supertypes"], new["supertypes"])
        compare_references(items, side, c, "realization", old["realizations"], new["realizations"])
        compare_references(items, side, c, "import", old["imports"], new["imports"])
        if old["literals"] != new["literals"]:
            items.append(Item("literal", side, c, "literals", f"{old['literals']} instead of {new['literals']}"))
        compare_attributes(items, side, c, old, new)
        compare_operations(items, side, c, old, new)
    return items


def compare_references(items, side, classifier, what, old_refs, new_refs):
    old_by_canonical = {canonical_text(r): r for r in old_refs}
    new_by_canonical = {canonical_text(r): r for r in new_refs}
    for key in old_by_canonical.keys() | new_by_canonical.keys():
        old_ref, new_ref = old_by_canonical.get(key), new_by_canonical.get(key)
        if old_ref is None:
            items.append(Item("missing reference", side, classifier, what, f"no {what} {new_ref}"))
        elif new_ref is None:
            items.append(Item("surplus reference", side, classifier, what, f"{what} {old_ref} not derived"))
        elif old_ref != new_ref:
            items.append(Item("reference to renamed classifier", side, classifier, what, f"{what} {old_ref} instead of {new_ref}"))


def compare_attributes(items, side, classifier, old, new):
    for name in old["attributes"].keys() | new["attributes"].keys():
        a, b = old["attributes"].get(name), new["attributes"].get(name)
        if a is None:
            items.append(Item("missing member", side, classifier, name, "attribute the target rules derive"))
            continue
        if b is None:
            items.append(Item("surplus member", side, classifier, name, "attribute no target rule derives"))
            continue
        if a["visibility"] != b["visibility"]:
            items.append(Item("visibility", side, classifier, name, f"{a['visibility']} instead of {b['visibility']}"))
        for flag in ("static", "final"):
            if a[flag] != b[flag]:
                items.append(Item("member modifier", side, classifier, name, f"{flag}={a[flag]} instead of {b[flag]}"))
        if a["type"] != b["type"]:
            if canonical_text(a["type"]) == canonical_text(b["type"]):
                items.append(Item("reference to renamed classifier", side, classifier, name, f"type {a['type']} instead of {b['type']}"))
            else:
                items.append(Item("type", side, classifier, name, f"type {a['type']} instead of {b['type']}"))
        if a["initializer"] != b["initializer"]:
            items.append(Item("initial value", side, classifier, name, f"{a['initializer']} instead of {b['initializer']}"))


def compare_operations(items, side, classifier, old, new):
    field_names = set(old["attributes"]) | set(new["attributes"])
    old_ops = {canonical_text(k): (k, v) for k, v in old["operations"].items()}
    new_ops = {canonical_text(k): (k, v) for k, v in new["operations"].items()}
    for key in old_ops.keys() | new_ops.keys():
        a, b = old_ops.get(key), new_ops.get(key)
        if a is None:
            signature, op = b
            items.append(Item(member_class(op, field_names, "missing"), side, classifier, signature, "the target rules derive it"))
            continue
        if b is None:
            signature, op = a
            items.append(Item(member_class(op, field_names, "surplus"), side, classifier, signature, "no target rule derives it"))
            continue
        (old_signature, a), (new_signature, b) = a, b
        name = old_signature
        if old_signature != new_signature:
            items.append(Item("reference to renamed classifier", side, classifier, name, f"signature {old_signature} instead of {new_signature}"))
        if a["return"] != b["return"]:
            cls = "reference to renamed classifier" if canonical_text(a["return"]) == canonical_text(b["return"]) else "type"
            items.append(Item(cls, side, classifier, name, f"returns {a['return']} instead of {b['return']}"))
        if a["visibility"] != b["visibility"]:
            items.append(Item("visibility", side, classifier, name, f"{a['visibility']} instead of {b['visibility']}"))
        for flag in ("static", "final", "abstract"):
            if a[flag] != b[flag]:
                items.append(Item("member modifier", side, classifier, name, f"{flag}={a[flag]} instead of {b[flag]}"))
        if a["bodyless"] != b["bodyless"]:
            items.append(Item("member kind", side, classifier, name, "class method instead of interface method" if b["bodyless"] else "interface method instead of class method"))
        elif a["body"] != b["body"]:
            if canonical_text(a["body"]) == canonical_text(b["body"]):
                items.append(Item("reference to renamed classifier", side, classifier, name, f"in the hand-written body: {a['body']} instead of {b['body']}"))
            else:
                items.append(Item("body", side, classifier, name, f"{a['body'] or '(empty)'} instead of {b['body'] or '(empty)'}"))


def member_class(op, field_names, direction):
    if op["constructor"]:
        return f"{direction} constructor"
    if is_accessor(op["name"], field_names):
        return f"{direction} accessor"
    return f"{direction} member"

# ---------------------------------------------------------------- features

CLASS_CREATION = {"classifier kind", "member kind", "initial value", "surplus accessor", "missing accessor",
                  "surplus reference", "missing reference"}


def feature_of(item, delta, uml_visibility):
    """The feature of the switch an item is charged to. `delta` holds the
    features the two selections differ in, `uml_visibility` the (classifier,
    element) pairs whose UML visibility differs as well. Charged by class first,
    then by the detail where one class has more than one cause: a Java
    visibility that differs together with its UML visibility is
    AccessorGeneration's, one that differs alone is the interface's."""
    # The alternative that replaces the default realization names the switch:
    # ClassCreation.Interface for config1 <-> config7, both for config7 <-> config8.
    creation = sorted(f for f in delta if f.startswith("ClassCreation.") and f != "ClassCreation.Class")
    if item.cls in CLASS_CREATION:
        return " / ".join(creation)
    if item.cls == "classifier modifier":
        return "DataTypeCreation.Record"
    if item.cls in ("classifier name", "reference to renamed classifier"):
        if "IBorrowable" in item.detail:
            return "InterfacePrefix"
        if "MediaImpl" in item.detail:
            return "RealizationSuffix"
        return "?"
    if item.cls in ("surplus constructor", "missing constructor"):
        return "ConstructorCreation"
    if item.cls == "visibility":
        if item.side == "UML" or (canonical(item.classifier), item.element) in uml_visibility or not creation:
            return "AccessorGeneration"
        return " / ".join(creation)
    if item.cls == "member modifier":
        if "final" in item.detail and item.element.startswith("register"):
            return "MethodStaticCall"
        if "static" in item.detail and item.element.startswith(("getCardNumber", "setCardNumber")):
            return "AttributeStaticCall"
        return " / ".join(creation)
    if item.cls == "body":
        return "AttributeStaticCall"
    return "?"

# ---------------------------------------------------------------- main

def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    library = Path(sys.argv[1])
    baselines = library / "runs" / "baselines"
    uml = {n: parse_uml(baselines / f"config{n}" / "model" / "library.uml") for n in CONFIGURATIONS}
    java = {n: parse_java(baselines / f"config{n}" / "src" / "catalog") for n in CONFIGURATIONS}
    selections = {n: set(json.loads((library / "rules" / f"config{n}.json").read_text())) for n in CONFIGURATIONS}

    per_pair = OrderedDict()
    for f in CONFIGURATIONS:
        for t in CONFIGURATIONS:
            if f == t:
                continue
            delta = selections[f] ^ selections[t]
            items = compare("UML", uml[f], uml[t]) + compare("Java", java[f], java[t])
            uml_visibility = {(canonical(i.classifier), i.element) for i in items if i.side == "UML" and i.cls == "visibility"}
            for item in items:
                item.feature = feature_of(item, delta, uml_visibility)
            per_pair[(f, t)] = (delta, items)

    classes = OrderedDict()
    for (f, t), (_, items) in per_pair.items():
        for item in items:
            entry = classes.setdefault(item.cls, {"items": 0, "UML": 0, "Java": 0, "pairs": set(), "features": Counter(), "examples": Counter()})
            entry["items"] += 1
            entry[item.side] += 1
            entry["pairs"].add((f, t))
            entry["features"][item.feature] += 1
            entry["examples"][item.key()] += 1

    def print_summary(title, table):
        print(f"== {title}")
        print(f"{'class':<32} {'pairs':>5} {'items':>5} {'UML':>5} {'Java':>5}  features (items)")
        for cls, entry in sorted(table.items(), key=lambda e: (-len(e[1]['pairs']), -e[1]['items'])):
            features = ", ".join(f"{name} ({count})" for name, count in entry["features"].most_common())
            print(f"{cls:<32} {len(entry['pairs']):>5} {entry['items']:>5} {entry['UML']:>5} {entry['Java']:>5}  {features}")
        print(f"{'classes':<32} {len(table):>5}")
        print(f"{'all':<32} {len({p for e in table.values() for p in e['pairs']}):>5} {sum(e['items'] for e in table.values()):>5}")

    print_summary("inconsistency classes over the 72 configuration pairs", classes)

    merged = OrderedDict()
    for cls, entry in classes.items():
        name = re.sub(r"^(surplus|missing) ", "", cls)
        target = merged.setdefault(name, {"items": 0, "UML": 0, "Java": 0, "pairs": set(), "features": Counter()})
        target["items"] += entry["items"]
        target["UML"] += entry["UML"]
        target["Java"] += entry["Java"]
        target["pairs"] |= entry["pairs"]
        target["features"] += entry["features"]
    print()
    print_summary("the same with surplus and missing folded into one class each", merged)

    print()
    print("== items per pair (from -> to: items, UML items, Java items; features the selections differ in | classes)")
    for (f, t), (delta, items) in per_pair.items():
        sides = Counter(i.side for i in items)
        print(f"config{f} -> config{t}: {len(items):>3} {sides['UML']:>3} {sides['Java']:>3}  {', '.join(sorted(delta))}  |  {', '.join(sorted({i.cls for i in items}))}")

    print()
    print("== pairs per class")
    for cls, entry in classes.items():
        cells = " ".join(f"{f}>{t}" for f, t in sorted(entry["pairs"]))
        print(f"{cls}: {cells}")

    print()
    print("== distinct items per class (times seen over the pairs)")
    for cls, entry in classes.items():
        print(f"-- {cls}")
        for example, count in sorted(entry["examples"].items()):
            print(f"  {count:>3}x {example}")


if __name__ == "__main__":
    main()
