#!/usr/bin/env python3
"""count-specific-code-paths.py -- The code paths of the preprocessor and the
migration that exist for one concrete rule set or metamodel (M5.2).

Usage: count-specific-code-paths.py <Vitruv-DSLs checkout>

Reads the main sources of reactions/preprocessor and reactions/migration and
prints, per tool, the lines of code per file or package (blank and
comment-only lines excluded, as count-loc.sh counts them), the imports of
metamodel and case-study packages, the instanceof checks against classes of
those packages, and every line naming a rule set or a metamodel, split into
code and comment lines. For the preprocessor it adds the text patterns of the
reactions language the tool matches. For the migration it lists the hooks of
the adapter interface, which adapter overrides which hook, and every call site
of a hook outside the adapter package, attributed to the hook the registry
method ends in. The test sources add the metamodel packages the test suite
imports with the number of test files each, as the record of which metamodels
ran through the default adapter. The git state of the checkout heads the
output.
"""

import re
import subprocess
import sys
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

PREPROCESSOR = "reactions/preprocessor/src/main/java"
MIGRATION = "reactions/migration/src/main/java"
MIGRATION_TESTS = "reactions/migration/src/test/java"
MIGRATION_ROOT = "tools/vitruv/dsls/reactions/migration"
ADAPTER_PACKAGE = MIGRATION_ROOT + "/adapter"

METAMODEL_IMPORTS = (
    "org.emftext.", "org.eclipse.uml2.", "org.palladiosimulator.",
    "tools.vitruv.applications.umljava.", "tools.vitruv.applications.pcmumlclass.",
    "tools.vitruv.applications.util.", "tools.vitruv.methodologisttemplate.",
    "tools.vitruv.change.testutils.metamodels.", "brakesystem.", "cad.", "simulink.", "autosar.",
    "mir.", "allElementTypes.", "allElementTypes2.", "pcm_mockup.", "uml_mockup.",
)
NAMES = re.compile(
    r"\b(jamopp|emftext|umljava|pcmumlclass|uml|java|pcm|palladio|brake\w*|simulink|autosar|cad"
    r"|config[0-9])\b",
    re.IGNORECASE,
)
JDK_PACKAGE = re.compile(r"\bjava\.(util|io|nio|lang|time|text|net)\b")
COMMENT_START = ("//", "#", "--", "*", "/*", "*/")
INSTANCEOF = re.compile(r"instanceof\s+([A-Za-z_][\w.]*)")
IMPORT = re.compile(r"^\s*import\s+(?:static\s+)?([\w.]+)")
REGISTRY_CALL = re.compile(r"\badapters\.(\w+)\(")
DIRECT_HOOK_CALL = re.compile(r"adapterFor\([^)]*\)\s*\.(\w+)\(")
METHOD = re.compile(r"^\s*(?:default\s+)?[\w<>\[\], ?]+\s+(\w+)\s*\(")
# The registry methods that end in a hook, and the hook they end in.
REGISTRY_METHOD_HOOK = {
    "prepareStandalone": "prepareStandalone",
    "newResourceSet": "loadOptions",
    "combinedLoadOptions": "loadOptions",
    "load": "normalizeLoadedResource",
    "isPlatformLibraryResource": "isPlatformLibraryResource",
    "isMigratedModel": "isPlatformLibraryResource",
    "anyRootRequiresChangeRecording": "requiresChangeRecording",
    "externalIdentityOf": "externalIdentityOf",
}


def java_files(folder):
    return sorted(path for path in folder.rglob("*.java"))


def relative(path, folder):
    return path.relative_to(folder).as_posix()


def lines_of(path):
    return path.read_text(encoding="utf-8").splitlines()


def loc(lines):
    count = 0
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith(COMMENT_START):
            count += 1
    return count


def is_comment(line):
    return line.strip().startswith(("//", "*", "/*", "/**"))


def git_state(checkout):
    def run(*args):
        return subprocess.run(["git", "-C", str(checkout), *args], capture_output=True, text=True,
                              check=True).stdout.strip()

    head = run("rev-parse", "--short", "HEAD")
    dirty = run("status", "--porcelain", "--", PREPROCESSOR, MIGRATION, MIGRATION_TESTS)
    return head, [line for line in dirty.splitlines() if line]


def metamodel_imports(lines):
    found = []
    for line in lines:
        match = IMPORT.match(line)
        if match and match.group(1).startswith(METAMODEL_IMPORTS):
            found.append(match.group(1))
    return found


def metamodel_instanceofs(lines, imports):
    simple_names = {name.rsplit(".", 1)[-1] for name in imports}
    found = []
    for number, line in enumerate(lines, 1):
        for match in INSTANCEOF.finditer(line):
            if match.group(1).rsplit(".", 1)[-1] in simple_names:
                found.append((number, match.group(1)))
    return found


def naming_lines(lines):
    found = []
    for number, line in enumerate(lines, 1):
        if IMPORT.match(line) or line.strip().startswith("package "):
            continue
        cleaned = JDK_PACKAGE.sub("", line)
        if NAMES.search(cleaned):
            found.append((number, "comment" if is_comment(line) else "code", line.strip()))
    return found


def print_file_table(folder, files, label):
    print(f"== {label}: lines of code per file")
    total = 0
    for path in files:
        count = loc(lines_of(path))
        total += count
        print(f"{count:6}  {relative(path, folder)}")
    print(f"{total:6}  total in {len(files)} file(s)")
    print()
    return total


def print_package_table(folder, files, label):
    print(f"== {label}: lines of code per package")
    per_package = OrderedDict()
    for path in files:
        package = relative(path.parent, folder)
        count, number = per_package.get(package, (0, 0))
        per_package[package] = (count + loc(lines_of(path)), number + 1)
    total = 0
    for package, (count, number) in per_package.items():
        total += count
        print(f"{count:6}  {number:3} file(s)  {package}")
    print(f"{total:6}  {len(files):3} file(s)  total")
    print()
    return total


def print_specific_lines(folder, files, label):
    print(f"== {label}: imports of metamodel or case-study packages per file")
    imports_by_file = {}
    any_import = False
    for path in files:
        imports = metamodel_imports(lines_of(path))
        imports_by_file[path] = imports
        if imports:
            any_import = True
            print(relative(path, folder))
            for name in imports:
                print(f"    {name}")
    if not any_import:
        print("(none)")
    print()

    print(f"== {label}: instanceof checks against classes of those packages")
    total_instanceof = 0
    any_check = False
    for path in files:
        lines = lines_of(path)
        total_instanceof += sum(len(INSTANCEOF.findall(line)) for line in lines)
        for number, name in metamodel_instanceofs(lines, imports_by_file[path]):
            any_check = True
            print(f"{relative(path, folder)}:{number}  instanceof {name}")
    if not any_check:
        print("(none)")
    print(f"({total_instanceof} instanceof checks in all)")
    print()

    print(f"== {label}: lines naming a rule set or a metamodel (imports and package lines excluded)")
    kinds = Counter()
    for path in files:
        for number, kind, text in naming_lines(lines_of(path)):
            kinds[kind] += 1
            print(f"{kind:7}  {relative(path, folder)}:{number}  {text}")
    if not kinds:
        print("(none)")
    print(f"({kinds['code']} code line(s), {kinds['comment']} comment line(s))")
    print()


def print_preprocessor_patterns(folder, files):
    print("== preprocessor: text patterns of the reactions language it matches")
    count = 0
    for path in files:
        lines = lines_of(path)
        text = "\n".join(lines)
        for match in re.finditer(r"Pattern\.compile\(", text):
            depth, index, in_string = 1, match.end(), False
            while depth and index < len(text):
                char = text[index]
                if in_string:
                    if char == "\\":
                        index += 1
                    elif char == '"':
                        in_string = False
                elif char == '"':
                    in_string = True
                else:
                    depth += {"(": 1, ")": -1}.get(char, 0)
                index += 1
            literals = re.findall(r'"((?:[^"\\]|\\.)*)"', text[match.end():index - 1])
            number = text.count("\n", 0, match.start()) + 1
            count += 1
            print(f"{relative(path, folder)}:{number}  {''.join(literals)}")
    print(f"({count} pattern(s))")
    print()


def adapter_hooks(adapter_folder):
    hooks = OrderedDict()
    for line in lines_of(adapter_folder / "MetamodelAdapter.java"):
        match = METHOD.match(line)
        if match and not line.strip().startswith(("public interface", "import", "package", "//")):
            hooks[match.group(1)] = "optional" if line.strip().startswith("default") else "required"
    return hooks


def overrides(path):
    names = []
    lines = lines_of(path)
    for index, line in enumerate(lines):
        if line.strip() == "@Override":
            for following in lines[index + 1:index + 4]:
                match = re.search(r"\b(\w+)\s*\(", following)
                if match:
                    names.append(match.group(1))
                    break
    return names


def print_hooks(folder, adapter_folder):
    hooks = adapter_hooks(adapter_folder)
    adapters = [path for path in java_files(adapter_folder)
                if "implements MetamodelAdapter" in path.read_text(encoding="utf-8")]
    overridden = {path.stem: set(overrides(path)) for path in adapters}
    print("== migration: hooks of MetamodelAdapter and the adapters overriding them")
    header = "hook".ljust(28) + "kind      " + "  ".join(name.ljust(18) for name in overridden)
    print(header)
    for hook, kind in hooks.items():
        marks = "  ".join(("yes" if hook in names else "-").ljust(18) for names in overridden.values())
        print(f"{hook.ljust(28)}{kind.ljust(10)}{marks}")
    counts = "  ".join(str(len(names)).ljust(18) for names in overridden.values())
    print(f"{'overridden'.ljust(28)}{''.ljust(10)}{counts}")
    print(f"({len(hooks)} hooks, {sum(1 for k in hooks.values() if k == 'optional')} optional)")
    print()
    return hooks


def print_call_sites(folder, files, hooks):
    print("== migration: call sites of the hooks outside the adapter package")
    sites = defaultdict(list)
    files_hit = set()
    unattributed = []
    for path in files:
        name = relative(path, folder)
        for number, line in enumerate(lines_of(path), 1):
            for match in DIRECT_HOOK_CALL.finditer(line):
                sites[match.group(1)].append((name, number, "adapterFor(...)." + match.group(1)))
                files_hit.add(name)
            for match in REGISTRY_CALL.finditer(line):
                method = match.group(1)
                if method == "adapterFor":
                    continue
                hook = REGISTRY_METHOD_HOOK.get(method)
                if hook is None:
                    unattributed.append((name, number, method))
                    continue
                sites[hook].append((name, number, "adapters." + method))
                files_hit.add(name)
    total = 0
    for hook in hooks:
        entries = sites.get(hook, [])
        total += len(entries)
        print(f"{hook}: {len(entries)} site(s)")
        for name, number, call in entries:
            print(f"    {name}:{number}  {call}")
    for name, number, method in unattributed:
        print(f"UNATTRIBUTED  {name}:{number}  adapters.{method}", file=sys.stderr)
    print(f"({total} call site(s) in {len(files_hit)} file(s))")
    print()


def print_test_metamodels(folder, files):
    print("== migration tests: metamodel packages imported, with the number of test files")
    by_prefix = defaultdict(set)
    for path in files:
        for name in metamodel_imports(lines_of(path)):
            prefix = next(p for p in METAMODEL_IMPORTS if name.startswith(p))
            by_prefix[prefix.rstrip(".")].add(relative(path, folder))
    for prefix, names in sorted(by_prefix.items(), key=lambda item: (-len(item[1]), item[0])):
        print(f"{len(names):4}  {prefix}")
    print(f"({len(files)} test source file(s))")
    print()


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(2)
    checkout = Path(sys.argv[1])
    head, dirty = git_state(checkout)
    print(f"Vitruv-DSLs at {head}, {len(dirty)} modified source file(s) under the counted folders")
    for entry in dirty:
        print(f"    {entry}")
    print()

    preprocessor = checkout / PREPROCESSOR
    preprocessor_files = java_files(preprocessor)
    print_file_table(preprocessor, preprocessor_files, "preprocessor")
    print_specific_lines(preprocessor, preprocessor_files, "preprocessor")
    print_preprocessor_patterns(preprocessor, preprocessor_files)

    migration = checkout / MIGRATION
    migration_files = java_files(migration)
    adapter_folder = migration / ADAPTER_PACKAGE
    print_package_table(migration, migration_files, "migration")
    print_file_table(migration, java_files(adapter_folder), "migration adapter package")
    outside = [path for path in migration_files if adapter_folder not in path.parents]
    print_specific_lines(migration, migration_files, "migration")
    hooks = print_hooks(migration, adapter_folder)
    print_call_sites(migration, outside, hooks)

    tests = checkout / MIGRATION_TESTS
    print_test_metamodels(tests, java_files(tests))


if __name__ == "__main__":
    main()
