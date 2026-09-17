#!/usr/bin/env python3
"""measure-selection-strategies.py -- How the strategies for choosing the
source of a full migration compare on the library example and the brake
system (M2.5).

Usage: measure-selection-strategies.py <thesis/examples/library>

For every library strategy (explicit with UML, explicit with Java,
reachability, fewest changes) the 81 runs selection/<strategy>/config<F>-to-
config<T>.properties give the selected source, the changes the re-derivation
makes, the time of the selection and of the whole migration without the change
count. Prints these per strategy as median and range, the selection share, the
pairs in which the fewest-changes strategy takes Java, the trial times, the
time of the propagation graph over all runs, and the brake-system runs of every
strategy folder.
"""

import statistics
import sys
from collections import Counter
from pathlib import Path

CONFIGURATIONS = range(1, 10)
LIBRARY_STRATEGIES = ("explicit", "explicit-java", "reachability", "fewest-changes")
BRAKE_STRATEGIES = ("explicit", "explicit-cad", "explicit-simulink", "explicit-autosar",
                    "reachability", "fewest-changes")


def read_properties(path):
    properties = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        properties[key.strip()] = value.strip().replace("\\:", ":")
    return properties


def short_name(uri):
    lowered = uri.lower()
    if "java" in lowered:
        return "Java"
    if "uml" in lowered:
        return "UML"
    return uri.rsplit("/", 1)[-1]


def median_range(values, fmt):
    return f"{fmt(statistics.median(values))} ({fmt(min(values))}-{fmt(max(values))})"


def milliseconds(value):
    return f"{value:.1f}ms"


def seconds(value):
    return f"{value / 1000:.1f}s"


def count(value):
    return f"{value:.0f}"


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    selection = Path(sys.argv[1]) / "selection"

    warnings = []
    graph = []
    explicit_migration = None
    print("== library, per strategy over the migrated pairs: selected source, changes, selection"
          " time and migration time as median (range), selection share (median of selection /"
          " migration)")
    for strategy in LIBRARY_STRATEGIES:
        runs = {}
        for f in CONFIGURATIONS:
            for t in CONFIGURATIONS:
                path = selection / strategy / f"config{f}-to-config{t}.properties"
                if not path.is_file():
                    warnings.append(f"{strategy}: config{f} -> config{t} missing")
                    continue
                runs[(f, t)] = read_properties(path)
        migrated = {pair: run for pair, run in runs.items() if run.get("migrated") == "true"}
        for pair, run in runs.items():
            if run.get("migrated") != "true":
                warnings.append(f"{strategy}: config{pair[0]} -> config{pair[1]} {run.get('outcome')}"
                                f" ({run.get('failure', 'no failure recorded')[:80]})")
            if run.get("mode") != "FULL":
                warnings.append(f"{strategy}: config{pair[0]} -> config{pair[1]} in mode {run.get('mode')}")
            if "graphMillis" in run:
                graph.append(float(run["graphMillis"]))
        if not migrated:
            warnings.append(f"{strategy}: no migrated run")
            continue
        sources = Counter(short_name(run["dominant"]) for run in migrated.values())
        changes = [int(run["changes"]) for run in migrated.values()]
        selection_ms = [float(run["selectionMillis"]) for run in migrated.values()]
        migration_ms = [float(run["migrationMillis"]) for run in migrated.values()]
        shares = [float(run["selectionMillis"]) / float(run["migrationMillis"]) for run in migrated.values()]
        selection_fmt = seconds if statistics.median(selection_ms) >= 1000 else milliseconds
        print(f"{strategy + ':':16} {len(migrated)} of {len(runs)} migrated, source "
              + ", ".join(f"{name} in {n}" for name, n in sources.most_common())
              + f"; changes {median_range(changes, count)}; selection {median_range(selection_ms, selection_fmt)}"
              f" (median {statistics.median(selection_ms):.1f} ms); migration {median_range(migration_ms, seconds)}"
              f" (median {statistics.median(migration_ms):.0f} ms); share {statistics.median(shares):.2%}")
        if strategy == "explicit":
            explicit_migration = statistics.median(migration_ms)
        if strategy == "fewest-changes":
            java_pairs = sorted(pair for pair, run in migrated.items() if short_name(run["dominant"]) == "Java")
            print(f"{'':16} Java in " + ", ".join(f"{f}->{t}" for f, t in java_pairs))
            trials = [float(value) for run in migrated.values()
                      for key, value in run.items() if key.startswith("trial.") and key.endswith(".millis")]
            failed_trials = sum(1 for run in migrated.values()
                                for key in run if key.startswith("trial.") and key.endswith(".failure"))
            against = (f" against {explicit_migration:.0f} ms of the explicit strategy"
                       if explicit_migration is not None else "")
            print(f"{'':16} {len(trials)} trials, {failed_trials} failed, {median_range(trials, count)} ms each;"
                  f" migration {statistics.median(migration_ms):.0f} ms{against}")
    if graph:
        print(f"propagation graph: mean {statistics.mean(graph):.1f} ms, median {statistics.median(graph):.1f} ms,"
              f" range {min(graph):.1f}-{max(graph):.1f} ms over {len(graph)} runs")

    print()
    print("== brake system, per strategy: selected source, changes, selection time, migration time")
    for strategy in BRAKE_STRATEGIES:
        path = selection / strategy / "brake-system.properties"
        if not path.is_file():
            warnings.append(f"{strategy}: brake-system.properties missing")
            continue
        run = read_properties(path)
        source = short_name(run.get("dominant", "?"))
        if run.get("migrated") != "true":
            print(f"{strategy + ':':18} {source}, failed: {run.get('failure', 'no failure recorded')[:90]}")
            continue
        trials = ""
        if run.get("trials", "0") != "0":
            candidates = []
            for i in range(int(run["trials"])):
                candidate = short_name(run.get(f"trial.{i}.candidate", "?"))
                changes = run.get(f"trial.{i}.changes", "-1")
                failed = f"trial.{i}.failure" in run or changes == "-1"
                candidates.append(f"{candidate} {'failed' if failed else changes}")
            trials = "; trials " + ", ".join(candidates)
        print(f"{strategy + ':':18} {source}, {run['changes']} changes, selection {float(run['selectionMillis']):.1f} ms,"
              f" migration {float(run['migrationMillis']):.0f} ms{trials}")

    if warnings:
        print()
        print("== warnings")
        for warning in warnings:
            print("  " + warning, file=sys.stderr)


if __name__ == "__main__":
    main()
