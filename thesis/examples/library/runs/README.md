# The library example across every pair of configurations

Each cell is the library example derived with one configuration's rules and then migrated to
another's, with

```
migration --model <vsum> --propagations umljava-config<to>.jar \
          --strategy explicit --dominant uml \
          --mode ids --source-update none --preserve report --ask never
```

and read against `baselines/config<to>`, the same example derived with the target rules into
an empty VSUM. `--mode ids` is the selective migration: it works out which rules changed by
their ids and repropagates only the elements those rules affect, tearing them down before
the new rules build them up again. What that came to in a cell - the dirty rules, the
source elements their triggers selected and the ones left out - is in the cell's `RUN.md`
under *What the rule diff and the trigger mechanism found*.

## The matrix

Rows are the configuration the example was derived with, columns the one it was migrated to.

| from \ to | config1 | config2 | config3 | config4 | config5 | config6 | config7 | config8 | config9 |
|---|---|---|---|---|---|---|---|---|---|
| **config1** | = | ok / 3 manual | ok (order) / 10 manual | ok / 8 manual | ok / 3 manual | ok (order) / 3 manual | ok / 36 manual | ok / 14 manual | ok / 19 manual |
| **config2** | 3 dev | = | 3 dev / 10 manual | 3 dev / 8 manual | 3 dev / 3 manual | 3 dev / 3 manual | 3 dev / 36 manual | 3 dev / 14 manual | ok / 18 manual |
| **config3** | 5 dev | 5 dev / 3 manual | = | 5 dev / 8 manual | 5 dev / 3 manual | 5 dev / 3 manual | 5 dev / 44 manual | 5 dev / 14 manual | ok / 13 manual |
| **config4** | 4 dev | 4 dev / 3 manual | 4 dev / 10 manual | = | 4 dev / 3 manual | 4 dev / 3 manual | 4 dev / 36 manual | 4 dev / 14 manual | ok / 19 manual |
| **config5** | 4 dev / 3 manual | 4 dev / 6 manual | 4 dev / 13 manual | 4 dev / 9 manual | = | 4 dev / 6 manual | 4 dev / 36 manual | 4 dev / 14 manual | ok (order) / 18 manual |
| **config6** | 1 dev / 6 manual | 1 dev / 9 manual | 1 dev / 16 manual | 1 dev / 14 manual | 1 dev / 9 manual | = | ok / 37 manual | 1 dev / 20 manual | 1 dev / 16 manual |
| **config7** | ok / 33 manual | ok / 34 manual | ok / 42 manual | ok / 22 manual | ok / 33 manual | ok / 33 manual | = | ok / 35 manual | ok / 29 manual |
| **config8** | ok / 12 manual | ok / 13 manual | ok / 22 manual | ok / 14 manual | ok / 12 manual | ok / 15 manual | ok / 35 manual | = | ok / 24 manual |
| **config9** | 8 dev / 9 manual | 6 dev / 9 manual | 7 dev / 9 manual | 7 dev / 9 manual | 8 dev / 6 manual | 8 dev / 3 manual | 8 dev / 45 manual | 8 dev / 20 manual | = |

- `=` - source and target rules are the same. Nothing is dirty, the migration returns
  without opening a view, and the models are the ones the row's baseline holds. This is the
  cell that would show a selective migration doing work it has no reason to do.
- `ok` - the migrated models describe exactly what the target configuration derives from
  scratch.
- `ok (order)` - they hold exactly the same content, listed in a different order. Nothing is
  missing, added or derived differently: a classifier's members came back in the order the
  repropagation rebuilt them in rather than the order a derivation from scratch produces.
  The cell's `RUN.md` lists these apart from real differences.
- `N dev` - the migrated models and the baseline disagree about N classifiers, ordering
  aside. A classifier is counted once however many of the two models it is wrong in, since
  the UML and the Java derived beside it are one thing to go and look at. The cell's
  `RUN.md` names each one, per model.
- `/ M manual` - M items of the old models are left to be dealt with by hand: content no
  rule of the target configuration derives (the report's `Would be kept`), content the
  pass could not place at all (`Not kept`), and decisions nobody made (`Open decisions`).
  These runs use `--preserve report`, so none of it is put back; M is the sum of those
  three section headers, stated in the report's own `Left to deal with by hand` line. The
  report's `Notes` section - moves, replaced values, carriers - is informational and not
  counted.

## What a migration does not undo

Leaving a feature behind does not take back what it put into the dominant model. The rules
of the target configuration know nothing about the elements an earlier one added, and the
tear-down works from rule ids, so a UML construct the source rules introduced simply stays.
`config5-to-config8` keeps `Member()` and its siblings, the default constructors
`ConstructorCreation` derives, in classifiers config8 realizes as Java enums - where a
public constructor is not legal Java. `config4-to-config1` keeps the `Impl` suffix
`RealizationSuffix` appended. Both are counted as deviations above; neither is a defect of
the migration, and undoing them would mean tearing down dominant-model elements on the
strength of rules that are no longer there.

## Why a cell is comparable to a from-scratch derivation at all

Because these runs use `--preserve report`. The preservation pass then works out what the
old models hold that no rule produced and writes it down without putting any of it back, so
what is left in a cell is what the target rules derive. Running the same migration with
`--preserve user` puts that content back, and a cell would then legitimately hold more than
the baseline - the difference would be the carried-over content and not a fidelity result.
Each cell's `preservation-report.md` is that list: the items to go through by hand after a
real migration; its `Left to deal with by hand` line is the `manual` number in the table.

## Does any of it compile

Every cell and every baseline is run through `javac`, and its `RUN.md` says what came
back. That is a separate result from the comparison above: a cell can hold exactly what
the target rules derive and still not compile, because a model comparison does not know
what Java requires.
`javac` rejects the Java of 42 of the 72 migrated cells.
The empty `Member.totalWeight` is the usual reason - the rules derive its signature and
never its body, `--preserve report` puts the body back nowhere, and a `double` method
without a `return` is not Java. That is this policy showing rather than a defect;
`--preserve user` is the run that puts the statements back.

The exception is the `config7` column: every migration into it compiles despite losing the body,
because those rules realize the classifiers holding it as Java interfaces, and a
body-less interface method is legal Java. The loss is the same, just silent to `javac` -
the cell's `preservation-report.md` is what still records it.

## The configurations

| configuration | how it differs from config1 |
|---|---|
| config1 | the baseline: `ClassCreation.Class`, `DataTypeCreation.Class` |
| config2 | `+ InterfacePrefix` |
| config3 | `+ AccessorGeneration` |
| config4 | `+ RealizationSuffix` |
| config5 | `+ ConstructorCreation` |
| config6 | `+ AttributeStaticCall`, `+ MethodStaticCall` |
| config7 | `+ ClassCreation.Interface`, `+ DataTypeCreation.Record`, `- ClassCreation.Class`, `- DataTypeCreation.Class` |
| config8 | `+ ClassCreation.Enum`, `+ DataTypeCreation.Record`, `- ClassCreation.Class`, `- DataTypeCreation.Class` |
| config9 | `+ InterfacePrefix`, `+ AccessorGeneration`, `+ AttributeStaticCall`, `+ MethodStaticCall`, `+ RealizationSuffix`, `+ ConstructorCreation` |

The feature model is `reactions/preprocessor/src/main/resources/feature-model.uvl`, the
selections are `../rules/config<n>.json`, and `../rules/config<n>-reactions` is what the
preprocessor makes of the annotated umljava reactions under each of them.

## Regenerating

Written by `ConfigMatrixArtifactGenerator` in the `reactions/migration` module, which owns
`../rules` and this folder and rewrites both. Everything else beside them is left alone.
`reactions/migration/generate-config-matrix` runs it - one JVM per cell, because JaMoPP's
classpath registry is global and a VSUM lifecycle leaves it changed, so cells sharing a
process do not derive the same models. It skips cells that already have a `RUN.md`, so an
interrupted sweep continues rather than starting over.

Regenerating with nothing else changed rewrites the `xmi:id` values in the derived
`library.uml` files and nothing more, so only regenerate when the models or the rules have
actually moved. The rule sets under `../rules` are the preprocessor's output and have to be
regenerated in the same session as the jars the runs use, or they would describe rules the
runs did not use; `reactions/migration/build-propagation-jars` builds those jars and
`reactions/migration/src/test/resources/propagations/README.md` describes the procedure.

Last written 2026-09-17.
