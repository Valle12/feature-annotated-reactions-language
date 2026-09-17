# config9 migrated to config9

Source and target rules are the same, so this cell is the one that must not change
anything: the persisted rule registry already matches the new specifications, no rule is
dirty, and the selective migration returns without opening a view.

| | |
|---|---|
| input | the config9 baseline, `baselines/config9` |
| rules | `umljava-config9.jar` |
| dominance | explicit, uml |

Equivalent command:

```
migration --model <vsum> --propagations umljava-config9.jar \
          --strategy explicit --dominant uml \
          --mode ids --source-update none --preserve report --ask never
```

## What the migration reported

| | |
|---|---|
| migrated | false |
| migration mode | ID_DIFF |
| fell back to a full migration | false |
| reason for the fallback | - |
| dirty rules | 0 |
| affected elements | 0 |
| preservation policy | REPORT |
| elements that would be kept | 0 |
| elements that could not be kept | 0 |
| open decisions nobody answered | 0 |
| items left to deal with by hand | 0 |
| phases | rule-diff |

## What the rule diff and the trigger mechanism found

| | |
|---|---|
| rules in the persisted registry | 140 |
| rules in the new specifications | 140 |
| dirty rules | 0 (0 added, 0 removed) |
| dirty rules whose trigger matches a source element | 0 |
| source elements probed | 0 |
| elements in the models | 0 |
| matched elements | 0 |
| elements added as referrers | 0 |
| elements left out | 0 |

Nothing is dirty, so nothing was selected.

## Against config9 from scratch

The migrated models describe exactly what `baselines/config9` describes. Under `--preserve report` nothing is carried over into the models, so what is left is what the target rules derive - and that is what the baseline derives from the same UML.

## Does the Java compile

Yes; `javac` reports nothing about `src/catalog`.

## What is here

`model/library.uml` and `src/catalog/*.java` as this run left them, and the rule registry the
VSUM carries afterwards. Left out: the standard library stubs JaMoPP derives under
`src/java`, and the VSUM's own bookkeeping under `vsum`, which only records identities and
the location it was written at.
