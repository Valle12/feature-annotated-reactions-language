#!/usr/bin/env bash
#
# check-reversibility.sh -- Is a migration reversible? (Q2.4 / M2.4)
#
# For every ordered pair of the nine library feature configurations, the V-SUM
# derived with config A is migrated to config B and straight back to config A,
# and the result is compared with the V-SUM it started from:
#
#   baselines/configA --[configB rules]--> intermediate --[configA rules]--> returned
#                                                                              vs
#                                                       the baselines/configA it started from
#
# M2.4 is the number of the 72 ordered pairs (the nine diagonal ones are trivial)
# for which the returned V-SUM is the original one again. A pair counts only when
# all three of these hold:
#
#   1. the Java is byte-identical (line endings normalised),
#   2. the UML is identical after mapping every xmi:id to a content-derived label
#      -- a round trip never reproduces ids, so a raw comparison would always fail,
#   3. consistencymetadata/vitruv/rule-hashes.txt is config A's again, i.e. the
#      returned V-SUM claims to be config A.
#
# Below the headline the same runs are counted again with the comparison relaxed
# one step at a time. That is what separates the three reasons a round trip does
# not close: content no rule derives being dropped, the serialisation reordering
# things, and the source model itself having changed in a way the way back cannot
# undo. Only the third is a statement about the reactions.
#
# Both legs run the migration CLI with the settings of the committed configuration
# matrix, one JVM each:
#
#   --strategy explicit --dominant uml --mode ids --source-update none
#   --preserve report --ask never
#
# --preserve report is deliberate: the preservation pass writes down what the old
# models hold that no rule of the target configuration produces and puts none of
# it back, so what a leg leaves behind is what the rules derive. The other
# policies are not run here.
#
# Running it takes about 70 seconds per pair -- roughly 35 minutes for all 81 with
# three workers. Pairs that already have a result are skipped, so an interrupted
# run continues rather than starting over, and running it again once everything is
# there only re-does the comparison and prints the numbers within seconds.
#
# Usage:
#   ./check-reversibility.sh
#
# Environment (all optional):
#   VITRUV_DSLS   the Vitruv-DSLs checkout       (default: E:/projects/Vitruv-DSLs)
#   WORKERS       pairs migrated in parallel     (default: 3)
#   FRESH=1       throw previous results away and run everything again
#
# Needs Git Bash, a JDK 21 in JAVA_HOME, and the nine umljava-config<n>.jar in
# reactions/migration/src/test/resources/propagations (they are committed). The
# nine from-scratch baselines are derived on the first run if they are not cached
# yet, which adds about ten minutes.
#
set -euo pipefail

REPOSITORY="${VITRUV_DSLS:-E:/projects/Vitruv-DSLs}"
WORKERS="${WORKERS:-3}"
FRESH="${FRESH:-0}"

fail() { echo "$*" >&2; exit 1; }

# ---------------------------------------------------------------- preconditions
[ -d "$REPOSITORY" ] || fail "No Vitruv-DSLs checkout at '$REPOSITORY'. Set VITRUV_DSLS."
REPOSITORY="$(cd "$REPOSITORY" && pwd)"
MIGRATION="$REPOSITORY/reactions/migration"
SWEEP="$MIGRATION/reversibility/sweep.sh"
[ -f "$SWEEP" ] || fail "The reversibility harness is missing: $SWEEP"

[ -n "${JAVA_HOME:-}" ] || fail "JAVA_HOME is not set; it has to point at a JDK 21."
[ -x "$JAVA_HOME/bin/javac" ] || [ -x "$JAVA_HOME/bin/javac.exe" ] \
  || fail "No javac in '$JAVA_HOME/bin'; JAVA_HOME has to point at a JDK, not a JRE."

PYTHON=""
for candidate in python python3 py; do
  if command -v "$candidate" > /dev/null 2>&1 && "$candidate" -c "import sys" > /dev/null 2>&1; then
    PYTHON="$candidate"
    break
  fi
done
[ -n "$PYTHON" ] || fail "No usable Python on PATH; the comparison needs one."

JARS="$MIGRATION/src/test/resources/propagations"
for n in 1 2 3 4 5 6 7 8 9; do
  [ -f "$JARS/umljava-config$n.jar" ] \
    || fail "umljava-config$n.jar is missing in $JARS. Build them: reactions/migration/build-propagation-jars"
done

RESULTS="$MIGRATION/target/matrix-reversibility"
SNAPSHOTS="$MIGRATION/target/matrix-baselines"

if [ "$FRESH" = 1 ]; then
  echo "FRESH=1: throwing away $RESULTS/report"
  rm -rf "$RESULTS/report"
fi
# The folder has to exist for the counting below: find on a missing folder fails, and with
# pipefail that would end the script without a word right after FRESH=1 emptied it.
mkdir -p "$RESULTS/report"

# ------------------------------------------------------------------- baselines
# Each pair starts from the library example as one configuration's rules derive it
# into an empty V-SUM. The generator caches those nine snapshots; deriving one that
# is not cached yet writes it, plus a note into a scratch folder we do not keep.
MISSING=()
for n in 1 2 3 4 5 6 7 8 9; do
  [ -d "$SNAPSHOTS/config$n" ] || MISSING+=("$n")
done
if [ ${#MISSING[@]} -gt 0 ]; then
  echo "=== deriving ${#MISSING[@]} missing baseline(s): ${MISSING[*]}"
  SCRATCH="$MIGRATION/target/matrix-reversibility-bootstrap"
  mkdir -p "$SCRATCH"
  SCRATCH_ARGUMENT="$SCRATCH"
  command -v cygpath > /dev/null 2>&1 && SCRATCH_ARGUMENT="$(cygpath -m "$SCRATCH")"
  (
    cd "$REPOSITORY"
    ./mvnw -q -B -pl reactions/migration test-compile
    for n in "${MISSING[@]}"; do
      echo "=== baseline $n"
      ./mvnw -q -B -pl reactions/migration org.codehaus.mojo:exec-maven-plugin:3.6.3:java \
        -Dexec.mainClass=tools.vitruv.dsls.reactions.migration.migration.ConfigMatrixArtifactGenerator \
        -Dexec.classpathScope=test \
        -Dexec.args="\"$SCRATCH_ARGUMENT\" reactions/preprocessor/src/main/resources/configs baseline $n"
    done
  ) || fail "A baseline could not be derived. Run reactions/migration/generate-config-matrix by hand to see why."
  for n in 1 2 3 4 5 6 7 8 9; do
    [ -d "$SNAPSHOTS/config$n" ] || fail "The config$n baseline is still missing after the bootstrap."
  done
fi

# ----------------------------------------------------------------- the sweep
DONE=$(find "$RESULTS/report" -name cell.properties 2>/dev/null | wc -l | tr -d ' ')
TODO=$((81 - DONE))
if [ "$TODO" -gt 0 ]; then
  echo "=== migrating $TODO of 81 pairs, $WORKERS at a time (about $(( (TODO * 70 + WORKERS * 59) / (WORKERS * 60) )) minutes)"
  mkdir -p "$RESULTS"
  PROGRESS="$RESULTS/sweep-report.log"
  touch "$PROGRESS"
  tail -n 0 -f "$PROGRESS" &
  FOLLOWER=$!
  trap 'kill "$FOLLOWER" 2> /dev/null || true' EXIT
  # A pair whose migration aborts is a result too, so a non-zero status here is
  # not a reason to stop; the census below reports what is actually on disk.
  "$SWEEP" report "$WORKERS" || true
  sleep 2 # let the follower catch up with the last pair before it is taken away
  kill "$FOLLOWER" 2> /dev/null || true
  trap - EXIT
else
  echo "=== all 81 pairs are already there, comparing them again"
fi

FOUND=$(find "$RESULTS/report" -name cell.properties 2>/dev/null | wc -l | tr -d ' ')
[ "$FOUND" -gt 0 ] || fail "No pair produced a result; look at $RESULTS/sweep-report.log"
[ "$FOUND" = 81 ] && echo "=== all 81 pairs ran" \
  || echo "=== warning: only $FOUND of 81 pairs produced a result; the counts below are over those"

# ------------------------------------------------------------- the comparison
RESULTS_ARGUMENT="$RESULTS"
MATRIX="$(cd "$(dirname "$0")/.." && pwd)/thesis/examples/library/runs/README.md"
if command -v cygpath > /dev/null 2>&1; then
  RESULTS_ARGUMENT="$(cygpath -w "$RESULTS")"
  MATRIX="$(cygpath -w "$MATRIX")"
fi

PYTHONIOENCODING=utf-8 "$PYTHON" - "$RESULTS_ARGUMENT" "$MATRIX" <<'PYTHON'
"""Reads the round trips on disk and reports M2.4. Self-contained on purpose: the
count must not depend on the harness that produced the runs."""
import re
import sys
from collections import Counter
from pathlib import Path

RESULTS = Path(sys.argv[1]) / "report"
MATRIX = Path(sys.argv[2])
MODIFIERS = ["public", "protected", "private", "abstract", "static", "final",
             "synchronized", "native", "strictfp", "default"]


def read(path):
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")


def properties(path):
    values = {}
    for line in (read(path) or "").splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    return values


def java_files(folder):
    source = folder / "src"
    if not source.is_dir():
        return None
    return {str(f.relative_to(source)).replace("\\", "/"): read(f)
            for f in sorted(source.rglob("*.java"))}


# --- the UML comparison ------------------------------------------------------
# Every run gives the elements fresh xmi:ids, so the ids are replaced by a label
# derived from the element itself before comparing. References then follow the
# element they point at rather than the number it happened to get.
ID_DEFINITION = re.compile(r'<([A-Za-z:]+)([^>]*?)\bxmi:id="([^"]+)"([^>]*)>?')
TOKEN = re.compile(r'(?<![A-Za-z0-9_\-])[A-Za-z0-9_\-]{6,}(?![A-Za-z0-9_\-])')


def canonical_uml(text):
    if text is None:
        return None
    labels, seen = {}, {}
    for match in ID_DEFINITION.finditer(text):
        tag, before, identifier, after = match.groups()
        attributes = before + after
        kind = re.search(r'xmi:type="([^"]+)"', attributes)
        name = re.search(r'\bname="([^"]*)"', attributes)
        label = (kind.group(1) if kind else tag) + (":" + name.group(1) if name else "")
        seen[label] = seen.get(label, 0) + 1
        labels[identifier] = label if seen[label] == 1 else "%s~%d" % (label, seen[label])
    return TOKEN.sub(lambda m: labels.get(m.group(0), m.group(0)), text)


# --- the relaxations ---------------------------------------------------------
def without_hand_written_body(text):
    """Drops the body of Member.totalWeight, the one thing in the example no rule
    derives. --preserve report records it and puts it back nowhere, so it is gone
    after the first leg; ignoring it separates that from the migration itself."""
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
    """`public static final` comes back as `public final static`: a serialisation
    instability, not a difference in what the models hold."""
    def sort(match):
        tokens = " ".join(sorted(match.group(1).split(), key=MODIFIERS.index))
        return match.group(0).replace(match.group(1), tokens)
    return re.sub(r"^\s*((?:(?:" + "|".join(MODIFIERS) + r")\s+){2,})", sort, text, flags=re.M)


def normalized(chars):
    return "\n".join(line.strip() for line in "".join(chars).split("\n") if line.strip())


def java_structure(text):
    """Package, imports as a set, the type header, and the members of the type as a
    set, as compare-migrated-models.py compares them at its member order level. A
    member keeps its own text, so the statements of a body keep their order, and the
    enumeration literals are one member."""
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


def compare_java(left, right, body=False, modifiers=False, members=False):
    if left is None or right is None or set(left) != set(right):
        return False
    for name in left:
        a, b = left[name] or "", right[name] or ""
        if body:
            a, b = without_hand_written_body(a), without_hand_written_body(b)
        if modifiers:
            a, b = with_sorted_modifiers(a), with_sorted_modifiers(b)
        if members:
            a, b = java_structure(a), java_structure(b)
        if a != b:
            return False
    return True


# --- the pairs ---------------------------------------------------------------
pairs = {}
for a in range(1, 10):
    for b in range(1, 10):
        if a == b:
            continue
        folder = RESULTS / ("config%d-config%d" % (a, b))
        cell = properties(folder / "cell.properties")
        if not cell:
            continue
        original, returned = folder / "original", folder / "returned"
        originalJava, returnedJava = java_files(original), java_files(returned)
        originalUml = canonical_uml(read(original / "model" / "library.uml"))
        returnedUml = canonical_uml(read(returned / "model" / "library.uml"))
        pairs[(a, b)] = {
            "java": compare_java(originalJava, returnedJava),
            "javaNoBody": compare_java(originalJava, returnedJava, body=True),
            "javaNoModifiers": compare_java(originalJava, returnedJava, body=True, modifiers=True),
            "javaNoMemberOrder": compare_java(originalJava, returnedJava, body=True, modifiers=True, members=True),
            "uml": originalUml is not None and originalUml == returnedUml,
            "registry": cell.get("ruleHashesEqual") == "true",
            "crashed": cell.get("exitForward") != "0" or cell.get("exitBack") != "0",
            "compilesBefore": cell.get("javacOriginal") == "0",
            "compilesAfter": cell.get("javacReturned") == "0",
        }

total = len(pairs)
if not total:
    sys.exit("No round trip could be read under %s" % RESULTS)


def count(predicate):
    return sum(1 for pair in pairs.values() if predicate(pair))


def reversible(pair, java="java"):
    return pair[java] and pair["uml"] and pair["registry"]


successful = [key for key, pair in sorted(pairs.items()) if reversible(pair)]

print("")
print("=" * 72)
print("M2.4   %d of %d configuration pairs are reversible" % (len(successful), total))
print("=" * 72)
for a, b in successful:
    print("       config%d -> config%d -> config%d" % (a, b, a))
if not successful:
    print("       (none)")

print("")
print("Per pair: UML, the first Java level that matches (strict, body, modifiers, members), registry, legs, javac after")
for (a, b), pair in sorted(pairs.items()):
    level = next((name for name, key in (("strict", "java"), ("body", "javaNoBody"),
                                         ("modifiers", "javaNoModifiers"), ("members", "javaNoMemberOrder")) if pair[key]), "differs")
    print("   config%d -> config%d -> config%d  uml %-8s java %-9s registry %-5s %-8s javac %s"
          % (a, b, a, "same" if pair["uml"] else "differs", level, "same" if pair["registry"] else "other",
             "aborted" if pair["crashed"] else "ran", "0" if pair["compilesAfter"] else "errors"))

print("")
print("Each criterion on its own, over the %d pairs:" % total)
print("   Java byte-identical .................................. %d" % count(lambda p: p["java"]))
print("   UML identical (after canonicalising xmi:id) .......... %d" % count(lambda p: p["uml"]))
print("   rule registry back to config A ....................... %d" % count(lambda p: p["registry"]))
print("   a migration leg aborted .............................. %d" % count(lambda p: p["crashed"]))
print("   the V-SUM compiles before / after the round trip ...... %d / %d"
      % (count(lambda p: p["compilesBefore"]), count(lambda p: p["compilesAfter"])))

print("")
print("The same runs with the comparison relaxed one step at a time:")
print("   as measured (M2.4) ................................... %d" % len(successful))
print("   ignoring the hand-written totalWeight body ........... %d"
      % count(lambda p: reversible(p, "javaNoBody")))
print("   + ignoring modifier order (public final static) ...... %d"
      % count(lambda p: reversible(p, "javaNoModifiers")))
print("   + ignoring member and import order ................... %d"
      % count(lambda p: reversible(p, "javaNoMemberOrder")))
print("")
print("   What the last line leaves is the pairs whose source model changed on the")
print("   way out in a way the way back does not undo. That is a property of the")
print("   reactions, not of the migration: the model each leg produces is the one")
print("   the target rules derive from scratch.")

# --- against the configuration matrix, when it is there ----------------------
try:
    verdict = {}
    for line in read(MATRIX).splitlines():
        row = re.match(r"\| \*\*config(\d)\*\* \|(.*)\|$", line.strip())
        if row:
            for column, cell in enumerate([c.strip() for c in row.group(2).split("|")], start=1):
                verdict[(int(row.group(1)), column)] = cell.split("/")[0].strip()
    if len(verdict) == 81:
        clean = lambda key: verdict[key].startswith("ok")
        offDiagonal = [key for key in verdict if key[0] != key[1]]
        both = [key for key in offDiagonal if clean(key) and clean((key[1], key[0]))]
        print("")
        print("Against the committed configuration matrix, which reads one migration at a time:")
        print("   single migrations it calls clean (ok or ok (order)) .. %d of %d"
              % (sum(1 for key in offDiagonal if clean(key)), len(offDiagonal)))
        print("   pairs whose BOTH directions it calls clean ........... %d" % len(both))
        print("   of those, reversible here ............................ %d"
              % sum(1 for key in both if key in pairs and reversible(pairs[key])))
        print("")
        print("   A cell being clean means the migrated models hold what the target rules")
        print("   derive; it does not mean they are the byte-identical file, and it says")
        print("   nothing about the other direction. Both is what a round trip needs.")
except Exception:
    pass

print("")
print("Full runs, logs and per-pair models: %s" % RESULTS)
PYTHON
