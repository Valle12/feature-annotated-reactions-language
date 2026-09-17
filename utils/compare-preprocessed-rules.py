#!/usr/bin/env python3
"""compare-preprocessed-rules.py -- Check that a preprocessor run kept every
reaction and routine of its input rules (M5.1).

Usage: compare-preprocessed-rules.py <master-reactions-dir> <preprocessed-dir>

Walks the *.reactions files of both folders and compares them per relative
path. From every file the reaction and routine names are read as the words
after the keywords at column zero, order-insensitively, because the
preprocessor rebuilds a file as header, selected reactions and the routines
they reach rather than copying it. Prints one row per file with the
master/output counts, the names behind every difference, the annotation lines
seen in the master as a cross-check, and a totals block. Files missing on
either side, differing reactions or blocks that only exist in the output make
the run a MISMATCH with exit code 1. Routines that only exist in the master
are listed as candidate dead code and left to a check by hand: dropping a
routine no reaction reaches is what the preprocessor is supposed to do.
"""

import re
import sys
from collections import Counter
from pathlib import Path

REACTION = re.compile(r"^reaction (\w+)", re.MULTILINE)
ROUTINE = re.compile(r"^routine (\w+)", re.MULTILINE)
ANNOTATION = re.compile(r"^@feature\(", re.MULTILINE)


def names(pattern, text):
    return Counter(pattern.findall(text))


def fmt_diff(label, counter):
    items = sorted(counter.elements())
    return f"    {label}: {', '.join(items)}"


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    master_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    for path in (master_dir, output_dir):
        if not path.is_dir():
            print(f"no such folder: {path}")
            return 2

    master_files = {
        p.relative_to(master_dir).as_posix(): p for p in master_dir.rglob("*.reactions")
    }
    output_files = {
        p.relative_to(output_dir).as_posix(): p for p in output_dir.rglob("*.reactions")
    }

    mismatch = False
    for only, side in (
        (sorted(master_files.keys() - output_files.keys()), "master"),
        (sorted(output_files.keys() - master_files.keys()), "output"),
    ):
        for name in only:
            print(f"{name}: only in the {side}")
            mismatch = True

    total_reactions = Counter()
    total_routines = Counter()
    total_annotations = 0
    dead = {}
    for name in sorted(master_files.keys() & output_files.keys()):
        master = master_files[name].read_text(encoding="utf-8")
        output = output_files[name].read_text(encoding="utf-8")
        m_reactions, o_reactions = names(REACTION, master), names(REACTION, output)
        m_routines, o_routines = names(ROUTINE, master), names(ROUTINE, output)
        total_annotations += len(ANNOTATION.findall(master))
        total_reactions.update({"master": sum(m_reactions.values())})
        total_reactions.update({"output": sum(o_reactions.values())})
        total_routines.update({"master": sum(m_routines.values())})
        total_routines.update({"output": sum(o_routines.values())})

        master_only_routines = m_routines - o_routines
        problems = [
            ("reactions only in the master", m_reactions - o_reactions),
            ("reactions only in the output", o_reactions - m_reactions),
            ("routines only in the output", o_routines - m_routines),
        ]
        broken = any(counter for _, counter in problems)
        verdict = "MISMATCH" if broken else "OK"
        mismatch = mismatch or broken

        print(
            f"{name:45} reactions {sum(m_reactions.values()):3}/{sum(o_reactions.values()):3}"
            f"  routines {sum(m_routines.values()):3}/{sum(o_routines.values()):3}  {verdict}"
        )
        for label, counter in problems:
            if counter:
                print(fmt_diff(label, counter))
        if master_only_routines:
            dead[name] = master_only_routines

    print()
    print(
        f"files {len(master_files)}/{len(output_files)}"
        f" | reactions {total_reactions['master']}/{total_reactions['output']}"
        f" | routines {total_routines['master']}/{total_routines['output']}"
        f" | annotations in the master {total_annotations}"
    )
    if dead:
        print()
        print("master-only routines (candidate dead code, verify by hand):")
        for name, counter in dead.items():
            print(fmt_diff(name, counter))

    print()
    print("MISMATCH" if mismatch else "OK")
    return 1 if mismatch else 0


if __name__ == "__main__":
    sys.exit(main())
