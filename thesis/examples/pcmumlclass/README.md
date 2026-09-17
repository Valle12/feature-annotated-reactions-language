# pcmumlclass transfer (M5.1)

The generalizability measurement transfers the annotation mechanism and the
preprocessor to the umlpcm case study (`pcmumlclass` in Vitruv-CaseStudies,
checked out at `67fc9a843`), a rule set the mechanism was not developed on:
126 reactions and 251 routines in 30 rule files across `pcm2uml/` and
`uml2pcm/`, plus the two aggregator files `CombinedPcmToUmlClass.reactions`
and `CombinedUmlClassToPcm.reactions` that only bundle the segments of a
direction.

Every reaction received the same annotation `@feature(type = "PcmUmlClass")`
(inserted by `utils/annotate-pcmumlclass-reactions.py`, 126 lines, no rule
body changed), so the feature model degenerates to a single root feature and
the identity configuration selects everything.

## What is here

- `rules/pcmumlclass.json` — the identity configuration, the flat feature
  list format of the umljava `config<n>.json` files.
- `rules/pcmumlclass-reactions/` — the preprocessor output for that
  configuration, the folder the case study build compiles via
  `-Dpcmumlclass.reactions.dir`. With everything selected only the annotation
  lines disappear; `utils/compare-preprocessed-rules.py` confirms 32/32
  files, 126/126 reactions and 251/251 routines against the annotated
  master, with no candidate dead code.

## Regenerating

In the Vitruv-DSLs checkout, with the annotated rules in place in
Vitruv-CaseStudies:

    reactions/preprocessor/preprocess-pcmumlclass

writes `pcmumlclass-reactions` next to the `pcmumlclass.json` under
`reactions/preprocessor/src/main/resources/configs`. The test runs behind
`thesis/figures/pcmumlclass-tests.txt` are one

    ./pcmumlclass-tests <label> [reactions-dir]

each in the Vitruv-CaseStudies checkout: `baseline` without a reactions
directory on the untouched rules, `preprocessed` with the generated folder.
Both states run the unchanged 53-test suite of the case study; 52 tests pass
in both, the one skipped test is disabled by the case study itself. The
annotated sources alone do not compile: the compile guard of the language
rejects `@feature` in compiler input for all 30 annotated rule files and
forces the preprocessor step, exactly as for the umljava master.
