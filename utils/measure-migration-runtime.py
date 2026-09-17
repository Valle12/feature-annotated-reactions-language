#!/usr/bin/env python3
"""measure-migration-runtime.py -- How long a selective migration of the library
example takes compared with a full one, per configuration pair (M4.2).

Usage: measure-migration-runtime.py <thesis/examples/library>

For every migrated cell runs/config<F>-to-config<T> the total and the phase
times are read from cell.properties, for the full migration of the same pair
from selection/explicit/config<F>-to-config<T>.properties, whose migrationMillis
is the total without the change count taken for M2.5. The phases are grouped
into the load of the VSUM, the identification of the scope (rule diff, roots,
classification, left-out scan, view, selection, preregistration), the snapshot,
the propagation (the two commits of the selective path, the re-derivation of
the full one), the preservation pass and the rest. Prints the per-pair times,
every phase and group over the migrated pairs as median and range, the ratios
and differences per pair, the diagonal cells and the from/to grids of the whole
run and of the migration without the load.

Two further sections put the numbers into context. The propagation time of the
selective path is set against the share of the UML model inside the affected
subtrees, computed as in measure-migration-scope.py. The explicit and the
reachability runs of selection/ keep the same dominant model and therefore do
the same work in two separate batches, so the difference of their
migrationMillis per pair shows how much identical full migrations vary.
"""

import importlib.util
import statistics
import sys
from collections import OrderedDict
from pathlib import Path

CONFIGURATIONS = range(1, 10)
GROUPS = OrderedDict((
    ("load", ("load",)),
    ("identification", ("rule-diff", "roots", "classify", "left-out", "view-open", "selection",
                        "preregister", "view-close", "dominance")),
    ("snapshot", ("snapshot",)),
    ("propagation", ("delete-commit", "reinsert-commit", "re-derive")),
    ("preserve", ("preserve",)),
    ("rest", ("refresh", "source-update")),
    ("change-count", ("change-count",)),
))
SELECTIVE_PHASES = ("rule-diff", "load", "roots", "dominance", "classify", "left-out", "view-open",
                    "selection", "snapshot", "preregister", "delete-commit", "reinsert-commit",
                    "view-close", "preserve", "refresh")
FULL_PHASES = ("load", "roots", "dominance", "snapshot", "re-derive", "change-count",
               "source-update", "preserve", "refresh")


def load_scope():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location(
        "measure_migration_scope", Path(__file__).with_name("measure-migration-scope.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scope = load_scope()


def ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    result = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            result[order[k]] = (i + j) / 2
        i = j + 1
    return result


def spearman(xs, ys):
    rx, ry = ranks(xs), ranks(ys)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    covariance = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    return covariance / (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5


def read_properties(path):
    properties = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        properties[key.strip()] = value.strip()
    return properties


def phases_of(properties):
    return {key[6:]: float(value) for key, value in properties.items() if key.startswith("phase.")}


def group_of(phase):
    for group, members in GROUPS.items():
        if phase in members:
            return group
    return None


def median_range(values, digits=0):
    fmt = f"{{:.{digits}f}}"
    return (f"{fmt.format(statistics.median(values))} "
            f"({fmt.format(min(values))}-{fmt.format(max(values))})")


def seconds(millis):
    return f"{millis / 1000:.2f}"


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    root = Path(sys.argv[1])

    warnings = []
    pairs = OrderedDict()
    diagonal = OrderedDict()
    for f in CONFIGURATIONS:
        for t in CONFIGURATIONS:
            cell = root / "runs" / f"config{f}-to-config{t}" / "cell.properties"
            full = root / "selection" / "explicit" / f"config{f}-to-config{t}.properties"
            if not cell.is_file() or not full.is_file():
                warnings.append(f"config{f} -> config{t}: cell or full run missing, skipped")
                continue
            selective = read_properties(cell)
            explicit = read_properties(full)
            if explicit.get("outcome") != "migrated" or explicit.get("mode") != "FULL":
                warnings.append(f"config{f} -> config{t}: the full run is {explicit.get('outcome')} "
                                f"in mode {explicit.get('mode')}, skipped")
                continue
            pair = {
                "selective": phases_of(selective), "full": phases_of(explicit),
                "selectiveTotal": float(selective["totalMillis"]),
                "fullMigration": float(explicit["migrationMillis"]),
                "fullTotal": float(explicit["totalMillis"]),
            }
            if selective.get("outcome") == "diagonal":
                diagonal[(f, t)] = pair
                continue
            if selective.get("outcome") != "migrated":
                warnings.append(f"config{f} -> config{t}: outcome {selective.get('outcome')}, skipped")
                continue
            if selective.get("fellBackToFull") == "true":
                warnings.append(f"config{f} -> config{t}: fell back to a full migration")
            for path, expected in (("selective", SELECTIVE_PHASES), ("full", FULL_PHASES)):
                unknown = sorted(set(pair[path]) - set(expected))
                missing = sorted(set(expected) - set(pair[path]))
                if unknown or missing:
                    warnings.append(f"config{f} -> config{t}: {path} phases unknown {unknown}, "
                                    f"missing {missing}")
                for phase in pair[path]:
                    if group_of(phase) is None:
                        warnings.append(f"config{f} -> config{t}: {path} phase {phase} in no group")
            for path, total in (("selective", pair["selectiveTotal"]), ("full", pair["fullTotal"])):
                if sum(pair[path].values()) > total + 1:
                    warnings.append(f"config{f} -> config{t}: {path} phases exceed the total")
            affected = scope.read_affected(root / "runs" / f"config{f}-to-config{t}")
            if affected is None:
                warnings.append(f"config{f} -> config{t}: RUN.md has no selection section")
            else:
                inside, everything, missing = scope.subtrees(
                    root / "runs" / "baselines" / f"config{f}" / "model" / "library.uml", affected)
                pair["subtreeShare"] = inside / everything
                for path in missing:
                    warnings.append(f"config{f} -> config{t}: the affected element {path} is not in the baseline")
            pairs[(f, t)] = pair

    def grouped(pair, path):
        sums = OrderedDict((group, 0.0) for group in GROUPS)
        for phase, millis in pair[path].items():
            group = group_of(phase)
            if group is not None:
                sums[group] += millis
        sums["rest"] += (pair["selectiveTotal"] if path == "selective" else pair["fullTotal"]) \
            - sum(pair[path].values())
        return sums

    def migration_without_load(pair, path):
        sums = grouped(pair, path)
        return sum(millis for group, millis in sums.items() if group not in ("load", "change-count"))

    print(f"{len(pairs)} migrated pairs, {len(diagonal)} diagonal cells")

    # -- per pair
    print()
    print("== per pair: selective total (identification, propagation, preserve) vs full without the"
          " change count (re-derive, preserve); ratio of the whole run and of the migration without"
          " the load")
    for (f, t), pair in pairs.items():
        s, u = grouped(pair, "selective"), grouped(pair, "full")
        print(f"config{f} -> config{t}: selective {pair['selectiveTotal']:6.0f} ms "
              f"(identification {s['identification']:4.0f}, propagation {s['propagation']:5.0f}, "
              f"preserve {s['preserve']:5.0f})  full {pair['fullMigration']:6.0f} ms "
              f"(re-derive {u['propagation']:5.0f}, preserve {u['preserve']:5.0f})  "
              f"ratio {pair['selectiveTotal'] / pair['fullMigration']:.2f} / "
              f"{migration_without_load(pair, 'selective') / migration_without_load(pair, 'full'):.2f}")

    # -- phases and groups
    print()
    print(f"== phases over the {len(pairs)} migrated pairs, median (range) in ms, selective | full")
    for phase in SELECTIVE_PHASES + tuple(p for p in FULL_PHASES if p not in SELECTIVE_PHASES):
        left = [pair["selective"][phase] for pair in pairs.values() if phase in pair["selective"]]
        right = [pair["full"][phase] for pair in pairs.values() if phase in pair["full"]]
        print(f"  {phase:16} {median_range(left) if left else '-':>22} | "
              f"{median_range(right) if right else '-'}")
    print()
    print("== groups, median (range) in ms, selective | full")
    for group in GROUPS:
        left = [grouped(pair, "selective")[group] for pair in pairs.values()]
        right = [grouped(pair, "full")[group] for pair in pairs.values()]
        print(f"  {group:16} {median_range(left):>22} | {median_range(right)}")
    left = [migration_without_load(pair, "selective") for pair in pairs.values()]
    right = [migration_without_load(pair, "full") for pair in pairs.values()]
    print(f"  {'without load':16} {median_range(left):>22} | {median_range(right)}")
    left = [pair["selectiveTotal"] for pair in pairs.values()]
    right = [pair["fullMigration"] for pair in pairs.values()]
    print(f"  {'whole run':16} {median_range(left):>22} | {median_range(right)}   "
          f"(full with the change count {median_range([p['fullTotal'] for p in pairs.values()])})")

    # -- ratios
    print()
    print("== selective / full per pair")
    for label, values in (
            ("whole run", [p["selectiveTotal"] / p["fullMigration"] for p in pairs.values()]),
            ("without load", [migration_without_load(p, "selective") / migration_without_load(p, "full")
                              for p in pairs.values()]),
            ("propagation", [grouped(p, "selective")["propagation"] / grouped(p, "full")["propagation"]
                             for p in pairs.values()]),
            ("preserve", [grouped(p, "selective")["preserve"] / grouped(p, "full")["preserve"]
                          for p in pairs.values()])):
        print(f"  {label:14} {median_range(values, 2)}, selective smaller in "
              f"{sum(1 for v in values if v < 1)} of {len(values)} pairs")
    total_selective = sum(p["selectiveTotal"] for p in pairs.values())
    total_full = sum(p["fullMigration"] for p in pairs.values())
    print(f"  pooled whole run {total_selective:.0f} / {total_full:.0f} = {total_selective / total_full:.2f}")
    ratios = [p["selectiveTotal"] / p["fullMigration"] for p in pairs.values()]
    gains = [p["fullMigration"] - p["selectiveTotal"] for p in pairs.values()]
    print(f"  whole run, full minus selective: {median_range(gains)} ms; selective slower in "
          f"{sum(1 for r in ratios if r > 1)} pairs, by at most {max(ratios) - 1:.1%}")

    # -- propagation against the affected subtrees
    shared = [p for p in pairs.values() if "subtreeShare" in p]
    if shared:
        print()
        print("== propagation of the selective path against the share of the UML model inside the affected subtrees")
        propagation = [grouped(p, "selective")["propagation"] for p in shared]
        shares = [p["subtreeShare"] for p in shared]
        print(f"  Spearman rank correlation over {len(shared)} pairs: {spearman(shares, propagation):.2f}")
        for label, keep in (("at most 10%", lambda s: s <= 0.10), ("at least 50%", lambda s: s >= 0.5)):
            chosen = [millis for millis, share in zip(propagation, shares) if keep(share)]
            if chosen:
                print(f"  {label:13} {len(chosen):>2} pairs, propagation {median_range(chosen)} ms")

    # -- identical full migrations in two batches
    print()
    print("== identical full migrations in two batches: reachability minus explicit per pair, migrationMillis")
    differences, same = [], 0
    for f in CONFIGURATIONS:
        for t in CONFIGURATIONS:
            explicit_file = root / "selection" / "explicit" / f"config{f}-to-config{t}.properties"
            reachability_file = root / "selection" / "reachability" / f"config{f}-to-config{t}.properties"
            if not explicit_file.is_file() or not reachability_file.is_file():
                continue
            explicit, reachability = read_properties(explicit_file), read_properties(reachability_file)
            if explicit.get("outcome") != "migrated" or reachability.get("outcome") != "migrated":
                continue
            if explicit.get("dominant") != reachability.get("dominant"):
                warnings.append(f"config{f} -> config{t}: explicit and reachability keep different dominant models")
                continue
            same += 1
            differences.append(float(reachability["migrationMillis"]) - float(explicit["migrationMillis"]))
    if differences:
        print(f"  {same} pairs with the same dominant model; difference {median_range(differences)} ms, "
              f"absolute {median_range([abs(d) for d in differences])} ms, reachability slower in "
              f"{sum(1 for d in differences if d > 0)} pairs")

    # -- diagonal
    print()
    print("== diagonal cells: selective total | full without the change count | full with it")
    for (n, _), pair in diagonal.items():
        print(f"  config{n}: {pair['selectiveTotal']:5.0f} ms, phases {sorted(pair['selective'])} | "
              f"{pair['fullMigration']:5.0f} ms | {pair['fullTotal']:5.0f} ms")
    if diagonal:
        print(f"  median: {median_range([p['selectiveTotal'] for p in diagonal.values()])} | "
              f"{median_range([p['fullMigration'] for p in diagonal.values()])} | "
              f"{median_range([p['fullTotal'] for p in diagonal.values()])}")

    # -- grids
    for title, selective_of, full_of in (
            ("whole run in seconds, selective total / full without the change count",
             lambda p: p["selectiveTotal"], lambda p: p["fullMigration"]),
            ("migration without the load in seconds, selective / full",
             lambda p: migration_without_load(p, "selective"),
             lambda p: migration_without_load(p, "full"))):
        print()
        print(f"== {title}, from (rows) x to (columns)")
        print("        " + "".join(f"{t:>14}" for t in CONFIGURATIONS))
        for f in CONFIGURATIONS:
            cells = []
            for t in CONFIGURATIONS:
                pair = pairs.get((f, t)) or diagonal.get((f, t))
                if pair is None:
                    cells.append("?")
                elif (f, t) in diagonal:
                    cells.append(f"{seconds(pair['selectiveTotal'])}/{seconds(full_of(pair))}")
                else:
                    cells.append(f"{seconds(selective_of(pair))}/{seconds(full_of(pair))}")
            print(f"config{f} " + "".join(f"{cell:>14}" for cell in cells))

    if warnings:
        print()
        print("== warnings")
        for warning in warnings:
            print("  " + warning, file=sys.stderr)


if __name__ == "__main__":
    main()
