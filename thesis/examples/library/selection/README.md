# Choosing the source of truth: the three strategies compared

Each run is the library example derived with one configuration's rules and migrated to
another's by a full migration, made once per strategy for choosing the source of truth:

```
migration --model <vsum> --propagations umljava-config<to>.jar \
          --strategy explicit --dominant uml \
          --mode full --source-update none --preserve report --ask never
```

with `--strategy reachability` and `--strategy derivationLoss` (the fewest-changes strategy)
in place of the explicit choice, and once more with `--dominant java` (`explicit-java`) as
the reference for what a migration from the other side changes when nothing ran before it.
A full migration keeps the source of truth as it is and
re-derives every other model from it with the new rules, so the strategy decides which
model survives the migration untouched. The explicit strategy takes the metamodel it is
told; reachability keeps to the metamodels whose propagations reach every other one and
takes the one with the most outgoing propagations; the fewest-changes strategy re-derives
the others from every such candidate into a scratch VSUM first and takes the candidate
whose re-derivation changes them the least.

## What a run records

- the source of truth the strategy chose (`dominant`), the metamodels present in the order
  the strategies iterate them (`present`), and what the reachability ranking looks like
  (`reachabilityRank`: out-degree / reached present metamodels per node, `reachabilityTie`
  when the best rank is not unique);
- `changes`: how many atomic changes the re-derivation made to the derived models, counted
  between their files before the migration and the files the rules derived, with elements
  matched by structure rather than identifier. The fewest-changes strategy computes exactly
  this per candidate in its trials (`trial.<n>.*`), so `predictedChanges` for the chosen
  candidate should equal `changes` (`predictionMatches`);
- `dominanceMillis`: how long the choice took, trial migrations included; `graphMillis`:
  building the propagation graph, which the tool does before every migration;
  `selectionMillis` is what choosing the source costs the strategy - the decision alone
  for the explicit strategy, which needs nothing computed, graph and decision for the
  other two, which read the graph first. `migrationMillis` is the whole migration
  without the time spent counting the changes afterwards (`phase.change-count`), and
  `phase.<name>` holds every phase; a fewest-changes migration adopts the winning trial's
  VSUM (`reuse-trial`) instead of re-deriving the same models again (`re-derive`).

## Over the 81 configuration pairs

| strategy | runs | migrated | source of truth | changes | selection ms | migration ms | selection share |
|---|---|---|---|---|---|---|---|
| explicit | 81 | 81 | `UML` in 81 | 0 / 264 / 908 | 1.176 / 1.528 / 5.584 | 4703 / 5124 / 5386 | 0.03 % |
| explicit-java | 81 | 81 | `java` in 81 | 52 / 275 / 361 | 1.179 / 1.635 / 5.813 | 4505 / 5172 / 5782 | 0.03 % |
| reachability | 81 | 81 | `UML` in 81 | 0 / 264 / 908 | 8.632 / 12.435 / 26.408 | 4506 / 5100 / 5432 | 0.24 % |
| fewest-changes | 81 | 81 | `UML` in 40, `java` in 41 | 0 / 185 / 361 | 4441.990 / 5218.211 / 5996.376 | 8041 / 8630 / 9531 | 60.60 % |

`selection share` is the median over the runs of `selectionMillis / migrationMillis`.

## Changes per configuration pair

Rows are the configuration the example was derived with, columns the one it was migrated
to; a cell is `changes`, marked with the source of truth when it is not the one the strategy
chose in most cells, `fail` when the run did not finish, `?` when it finished but its
changes could not be counted, and `-` when it was not made.

### explicit

Source of truth: `UML` in every cell.

| from \ to | config1 | config2 | config3 | config4 | config5 | config6 | config7 | config8 | config9 |
|---|---|---|---|---|---|---|---|---|---|
| **config1** | 46 | 99 | 86 | 525 | 246 | 70 | 730 | 264 | 750 |
| **config2** | 46 | 46 | 86 | 525 | 246 | 70 | 730 | 264 | 697 |
| **config3** | 46 | 99 | 46 | 525 | 246 | 70 | 762 | 264 | 726 |
| **config4** | 46 | 99 | 86 | 46 | 246 | 70 | 730 | 264 | 359 |
| **config5** | 234 | 287 | 274 | 650 | 234 | 254 | 774 | 452 | 747 |
| **config6** | 76 | 129 | 116 | 555 | 272 | 54 | 734 | 294 | 738 |
| **config7** | 738 | 791 | 774 | 807 | 758 | 742 | 0 | 773 | 908 |
| **config8** | 256 | 309 | 296 | 676 | 456 | 280 | 757 | 46 | 901 |
| **config9** | 260 | 260 | 260 | 260 | 260 | 242 | 810 | 478 | 242 |

### explicit-java

Source of truth: `java` in every cell.

| from \ to | config1 | config2 | config3 | config4 | config5 | config6 | config7 | config8 | config9 |
|---|---|---|---|---|---|---|---|---|---|
| **config1** | 271 | 273 | 62 | 272 | 286 | 276 | 345 | 345 | 81 |
| **config2** | 272 | 272 | 63 | 273 | 287 | 277 | 345 | 345 | 80 |
| **config3** | 271 | 273 | 52 | 272 | 286 | 276 | 345 | 345 | 71 |
| **config4** | 281 | 283 | 72 | 281 | 296 | 286 | 348 | 348 | 90 |
| **config5** | 273 | 275 | 68 | 274 | 276 | 278 | 355 | 355 | 76 |
| **config6** | 273 | 275 | 62 | 274 | 288 | 275 | 347 | 347 | 80 |
| **config7** | 184 | 185 | 166 | 184 | 187 | 184 | 184 | 184 | 170 |
| **config8** | 350 | 351 | 141 | 350 | 353 | 355 | 350 | 350 | 146 |
| **config9** | 286 | 286 | 69 | 286 | 289 | 288 | 361 | 361 | 72 |

### reachability

Source of truth: `UML` in every cell.

| from \ to | config1 | config2 | config3 | config4 | config5 | config6 | config7 | config8 | config9 |
|---|---|---|---|---|---|---|---|---|---|
| **config1** | 46 | 99 | 86 | 525 | 246 | 70 | 730 | 264 | 750 |
| **config2** | 46 | 46 | 86 | 525 | 246 | 70 | 730 | 264 | 697 |
| **config3** | 46 | 99 | 46 | 525 | 246 | 70 | 762 | 264 | 726 |
| **config4** | 46 | 99 | 86 | 46 | 246 | 70 | 730 | 264 | 359 |
| **config5** | 234 | 287 | 274 | 650 | 234 | 254 | 774 | 452 | 747 |
| **config6** | 76 | 129 | 116 | 555 | 272 | 54 | 734 | 294 | 738 |
| **config7** | 738 | 791 | 774 | 807 | 758 | 742 | 0 | 773 | 908 |
| **config8** | 256 | 309 | 296 | 676 | 456 | 280 | 757 | 46 | 901 |
| **config9** | 260 | 260 | 260 | 260 | 260 | 242 | 810 | 478 | 242 |

### fewest-changes

Source of truth: `java` in all but 40 cell(s); those are marked with the one they took.

| from \ to | config1 | config2 | config3 | config4 | config5 | config6 | config7 | config8 | config9 |
|---|---|---|---|---|---|---|---|---|---|
| **config1** | 46 (UML) | 99 (UML) | 62 | 272 | 246 (UML) | 70 (UML) | 345 | 264 (UML) | 81 |
| **config2** | 46 (UML) | 46 (UML) | 63 | 273 | 246 (UML) | 70 (UML) | 345 | 264 (UML) | 80 |
| **config3** | 46 (UML) | 99 (UML) | 46 (UML) | 272 | 246 (UML) | 70 (UML) | 345 | 264 (UML) | 71 |
| **config4** | 46 (UML) | 99 (UML) | 72 | 46 (UML) | 246 (UML) | 70 (UML) | 348 | 264 (UML) | 90 |
| **config5** | 234 (UML) | 275 | 68 | 274 | 234 (UML) | 254 (UML) | 355 | 355 | 76 |
| **config6** | 76 (UML) | 129 (UML) | 62 | 274 | 272 (UML) | 54 (UML) | 347 | 294 (UML) | 80 |
| **config7** | 184 | 185 | 166 | 184 | 187 | 184 | 0 (UML) | 184 | 170 |
| **config8** | 256 (UML) | 309 (UML) | 141 | 350 | 353 | 280 (UML) | 350 | 46 (UML) | 146 |
| **config9** | 260 (UML) | 260 (UML) | 69 | 260 (UML) | 260 (UML) | 242 (UML) | 361 | 361 | 72 |

## What the fewest-changes strategy tried

Per configuration pair, the changes each candidate's trial re-derivation proposed, in the
order the trials ran; `-` marks a trial that did not complete.

| from \ to | config1 | config2 | config3 | config4 | config5 | config6 | config7 | config8 | config9 |
|---|---|---|---|---|---|---|---|---|---|
| **config1** | UML 46 / java 271 | UML 99 / java 273 | UML 86 / java 62 | UML 525 / java 272 | UML 246 / java 286 | UML 70 / java 276 | UML 717 / java 345 | UML 237 / java 345 | UML 750 / java 81 |
| **config2** | UML 46 / java 272 | UML 46 / java 272 | UML 86 / java 63 | UML 525 / java 273 | UML 246 / java 287 | UML 70 / java 277 | UML 717 / java 345 | UML 237 / java 345 | UML 697 / java 80 |
| **config3** | UML 46 / java 271 | UML 99 / java 273 | UML 46 / java 52 | UML 525 / java 272 | UML 246 / java 286 | UML 70 / java 276 | UML 749 / java 345 | UML 237 / java 345 | UML 726 / java 71 |
| **config4** | UML 46 / java 281 | UML 99 / java 283 | UML 86 / java 72 | UML 46 / java 281 | UML 246 / java 296 | UML 70 / java 286 | UML 717 / java 348 | UML 237 / java 348 | UML 359 / java 90 |
| **config5** | UML 234 / java 273 | UML 287 / java 275 | UML 274 / java 68 | UML 650 / java 274 | UML 234 / java 276 | UML 254 / java 278 | UML 761 / java 355 | UML 425 / java 355 | UML 747 / java 76 |
| **config6** | UML 76 / java 273 | UML 129 / java 275 | UML 116 / java 62 | UML 555 / java 274 | UML 272 / java 288 | UML 54 / java 275 | UML 721 / java 347 | UML 267 / java 347 | UML 738 / java 80 |
| **config7** | UML 725 / java 184 | UML 778 / java 185 | UML 761 / java 166 | UML 800 / java 184 | UML 745 / java 187 | UML 729 / java 184 | UML 0 / java 184 | UML 760 / java 184 | UML 901 / java 170 |
| **config8** | UML 231 / java 350 | UML 284 / java 351 | UML 271 / java 141 | UML 669 / java 350 | UML 431 / java 353 | UML 255 / java 355 | UML 744 / java 350 | UML 46 / java 350 | UML 894 / java 146 |
| **config9** | UML 260 / java 286 | UML 260 / java 286 | UML 260 / java 69 | UML 260 / java 286 | UML 260 / java 289 | UML 242 / java 288 | UML 797 / java 361 | UML 451 / java 361 | UML 242 / java 72 |

- Cells where the chosen candidate's trial count differs from `changes`: config1-to-config8, config2-to-config8, config3-to-config8, config4-to-config8, config6-to-config8, config8-to-config1, config8-to-config2, config8-to-config6.
- Trials that did not complete: none.

## The brake system

The brake-system chain, four metamodels with a propagation each way between neighbours,
seeded with one front axle and migrated with its own rules. Here the strategies can
disagree: the explicit strategy is told the brake system (`explicit`) and, for reference,
each of the other three (`explicit-<metamodel>`), reachability ranks by out-degree and the
two middle metamodels have the higher one, and the fewest-changes strategy tries all four.

| strategy | source of truth | re-derived | changes | trials | selection ms | migration ms |
|---|---|---|---|---|---|---|
| explicit | `brakesystem` | `cad`, `simulink`, `autosar` | 0 | - | 1.208 | 181 |
| explicit-autosar | `autosar` | `brakesystem`, `cad`, `simulink` | 42 | - | 1.296 | 179 |
| explicit-cad | `cad` | `brakesystem`, `simulink`, `autosar` | fail | fail | - | - |
| explicit-simulink | `simulink` | `brakesystem`, `cad`, `autosar` | 34 | - | 1.486 | 190 |
| reachability | `cad` | `brakesystem`, `simulink`, `autosar` | fail | fail | - | - |
| fewest-changes | `brakesystem` | `cad`, `simulink`, `autosar` | 0 | brakesystem 0 / cad - / simulink 34 / autosar 42 | 349.549 | 546 |

Runs that did not finish:

- explicit-cad, brake system, re-deriving from `cad`: `There were (2) corresponding elements of type Parameter for: simulink.impl.ParameterImpl@55d6b2dc (name: Diameter, type: double, value: 320.0, readOnly: false), which are: [edu.kit.ipd.sdq.metamodels.cad.impl.NumericParameterImpl@17a72c07 (id: null, name: Diameter, description: null) (value: 320.0, unit: mm), edu.kit.ipd.sdq.metamodels.cad.impl.NumericParameterImpl@49f535ac (id: null, name: Diameter, description: null) (value: 320.0, unit: mm)]`
- reachability, brake system, re-deriving from `cad`: `There were (2) corresponding elements of type Parameter for: simulink.impl.ParameterImpl@1e896a96 (name: Diameter, type: double, value: 320.0, readOnly: false), which are: [edu.kit.ipd.sdq.metamodels.cad.impl.NumericParameterImpl@2e68299b (id: null, name: Diameter, description: null) (value: 320.0, unit: mm), edu.kit.ipd.sdq.metamodels.cad.impl.NumericParameterImpl@604efdc0 (id: null, name: Diameter, description: null) (value: 320.0, unit: mm)]`

## Ties and the order of the models

The library VSUM lists its models as `UML`, `java`, which is the order every strategy iterates the metamodels in. The reachability ranking is `UML` 1/1, `java` 1/1 (out-degree / reached present metamodels), a tie in 324 of 324 runs: with one propagation each way, both metamodels reach each other and neither has the higher out-degree, so the strategy keeps the first one listed.
The brake-system VSUM lists `brakesystem`, `cad`, `simulink`, `autosar`; the reachability ranking is `brakesystem` 1/3, `cad` 2/3, `simulink` 2/3, `autosar` 1/3, so the best rank is shared and the first of its holders wins.

## Regenerating

Written by `SourceSelectionArtifactGenerator` in the `reactions/migration` module, which
owns this folder. `reactions/migration/generate-selection-matrix` runs it - one JVM per
run, one run after the other, because the runs are timed and because JaMoPP's classpath
registry is global and a VSUM lifecycle leaves it changed. It skips runs whose properties
file is already there, so an interrupted sweep continues rather than starting over. The
runs start from the baselines `generate-config-matrix` derives, and use the same
propagation jars.

Last written 2026-09-17.
