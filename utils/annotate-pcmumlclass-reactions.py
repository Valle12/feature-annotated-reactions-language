#!/usr/bin/env python3
"""annotate-pcmumlclass-reactions.py -- Put the uniform feature annotation on
every reaction of the pcmumlclass case study (M5.1).

Usage: annotate-pcmumlclass-reactions.py <Vitruv-CaseStudies checkout>

Inserts the line @feature(type = "PcmUmlClass") directly above every reaction
of the rule files under pcmumlclass/src/main/reactions/tools/vitruv/
applications/pcmumlclass/{pcm2uml,uml2pcm}. The two aggregator files at the
top level of that folder hold no reactions and stay untouched. The insert
works on the raw bytes and reuses the CRLF line endings of the files; a
reaction keyword always sits at column zero with header content above it, so
the anchor is the line break before the keyword. Refuses to run when any file
already carries an annotation, checks that no file mixes in LF-only reaction
lines, prints the inserted count per file and fails unless the total is the
126 reactions the case study holds.
"""

import sys
from pathlib import Path

ANNOTATION = b'@feature(type = "PcmUmlClass")'
EXPECTED_TOTAL = 126


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    checkout = Path(sys.argv[1])
    rules = (
        checkout
        / "pcmumlclass/src/main/reactions/tools/vitruv/applications/pcmumlclass"
    )
    if not rules.is_dir():
        print(f"no such rules folder: {rules}")
        return 2

    files = sorted(
        [*rules.glob("pcm2uml/*.reactions"), *rules.glob("uml2pcm/*.reactions")]
    )
    if not files:
        print(f"no rule files under {rules}")
        return 2

    contents = {}
    for file in files:
        data = file.read_bytes()
        if b"@feature" in data:
            print(f"{file.relative_to(rules)} already carries an annotation, aborting")
            return 1
        if data.count(b"\nreaction ") != data.count(b"\r\nreaction "):
            print(f"{file.relative_to(rules)} has an LF-only reaction line, aborting")
            return 1
        contents[file] = data

    total = 0
    for file, data in contents.items():
        count = data.count(b"\r\nreaction ")
        replaced = data.replace(
            b"\r\nreaction ", b"\r\n" + ANNOTATION + b"\r\nreaction "
        )
        file.write_bytes(replaced)
        total += count
        print(f"{str(file.relative_to(rules)):55} {count:3} reactions annotated")

    print(f"{'total':55} {total:3}")
    if total != EXPECTED_TOTAL:
        print(f"expected {EXPECTED_TOTAL} annotated reactions, files are left annotated")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
