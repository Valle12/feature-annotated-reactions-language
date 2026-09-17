# config1 migrated to config2

| | |
|---|---|
| input | the config1 baseline, `baselines/config1` |
| rules | `umljava-config2.jar` |
| dominance | explicit, uml |

Equivalent command:

```
migration --model <vsum> --propagations umljava-config2.jar \
          --strategy explicit --dominant uml \
          --mode ids --source-update none --preserve report --ask never
```

## What the migration reported

| | |
|---|---|
| migrated | true |
| migration mode | ID_DIFF |
| fell back to a full migration | false |
| reason for the fallback | - |
| dirty rules | 2 |
| affected elements | 3 |
| preservation policy | REPORT |
| elements that would be kept | 0 |
| elements that could not be kept | 3 |
| open decisions nobody answered | 0 |
| items left to deal with by hand | 3 |
| phases | rule-diff, load, roots, dominance, classify, left-out, view-open, selection, snapshot, preregister, delete-commit, reinsert-commit, view-close, preserve, refresh |

## What the rule diff and the trigger mechanism found

| | |
|---|---|
| rules in the persisted registry | 116 |
| rules in the new specifications | 118 |
| dirty rules | 2 (2 added, 0 removed) |
| dirty rules whose trigger matches a source element | 1 |
| source elements probed | 50 |
| elements in the models | 424 |
| matched elements | 2 |
| elements added as referrers | 1 |
| elements left out | 15 |

### Dirty rules

```
+ javaToUmlClassifier::JavaInterfaceCreatedAddPrefix  matches 0 source element(s)
+ umlToJavaClassifier::UmlInterfaceInsertedAddPrefix  matches 2 source element(s)
```

### Affected elements

```
library.uml#/0/catalog/Identifiable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/Borrowable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/Media/Borrowable  uml::InterfaceRealization  refers to library.uml#/0/catalog/Borrowable
```

### Left out

```
library.uml#/0/catalog/Identifiable/getId/@ownedParameter.0  uml::Parameter  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/catalog/Borrowable/borrow/@ownedParameter.0  uml::Parameter  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/catalog/Media/describe/returnParameter  uml::Parameter  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/catalog/Book/describe/returnParameter  uml::Parameter  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/catalog/Member/borrowed/@lowerValue  uml::LiteralInteger  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/catalog/Member/borrowed/@upperValue  uml::LiteralUnlimitedNatural  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/catalog/Member/register/returnParameter  uml::Parameter  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/catalog/Member/totalWeight/@ownedParameter.0  uml::Parameter  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/int  uml::PrimitiveType  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/boolean  uml::PrimitiveType  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/String  uml::PrimitiveType  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/double  uml::PrimitiveType  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/java  uml::Package  it corresponds to src/java/package-info.java#/, outside the models
library.uml#/0/java/lang  uml::Package  it corresponds to src/java/lang/package-info.java#/, outside the models
library.uml#/0/java/lang/String  uml::Class  it corresponds to pathmap:/javaclass/java.lang.String.java#//@classifiers.0, outside the models
```

## Against config2 from scratch

The migrated models describe exactly what `baselines/config2` describes. Under `--preserve report` nothing is carried over into the models, so what is left is what the target rules derive - and that is what the baseline derives from the same UML.

## What could not be kept

- containers::CompilationUnit 'catalog.Borrowable.java' at src/catalog/Borrowable.java#0/ - the model file has no counterpart after the migration
- imports::ClassifierImport at src/catalog/Media.java#0/@imports.0.classifier - it references an element that no longer exists (the value classifiers::Interface 'Borrowable' at src/catalog/Borrowable.java#0/@classifiers.0 has no counterpart)
- types::ClassifierReference in Media at src/catalog/Media.java#0/@classifiers.0/@implements.0/@classifierReferences.0.target - it references an element that no longer exists (the value classifiers::Interface 'Borrowable' at src/catalog/Borrowable.java#0/@classifiers.0 has no counterpart)

## Does the Java compile

Yes; `javac` reports nothing about `src/catalog`.

## What is here

`model/library.uml` and `src/catalog/*.java` as this run left them, and the rule registry the
VSUM carries afterwards. Left out: the standard library stubs JaMoPP derives under
`src/java`, and the VSUM's own bookkeeping under `vsum`, which only records identities and
the location it was written at.
