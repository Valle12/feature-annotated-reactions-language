# config7 migrated to config8

| | |
|---|---|
| input | the config7 baseline, `baselines/config7` |
| rules | `umljava-config8.jar` |
| dominance | explicit, uml |

Equivalent command:

```
migration --model <vsum> --propagations umljava-config8.jar \
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
| dirty rules | 4 |
| affected elements | 4 |
| preservation policy | REPORT |
| elements that would be kept | 35 |
| elements that could not be kept | 0 |
| open decisions nobody answered | 0 |
| items left to deal with by hand | 35 |
| phases | rule-diff, load, roots, dominance, classify, left-out, view-open, selection, snapshot, preregister, delete-commit, reinsert-commit, view-close, preserve, refresh |

## What the rule diff and the trigger mechanism found

| | |
|---|---|
| rules in the persisted registry | 116 |
| rules in the new specifications | 116 |
| dirty rules | 4 (2 added, 2 removed) |
| dirty rules whose trigger matches a source element | 2 |
| source elements probed | 50 |
| elements in the models | 216 |
| matched elements | 4 |
| elements added as referrers | 0 |
| elements left out | 17 |

### Dirty rules

```
+ javaToUmlClassifier::JavaClassInsertedAsEnum  matches 0 source element(s)
- javaToUmlClassifier::JavaClassInsertedAsInterface  matches 0 source element(s)
+ umlToJavaClassifier::UmlClassInsertedAsEnum  matches 4 source element(s)
- umlToJavaClassifier::UmlClassInsertedAsInterface  matches 4 source element(s)
```

### Affected elements

```
library.uml#/0/catalog/Media  uml::Class  matched by umlToJavaClassifier::UmlClassInsertedAsEnum, umlToJavaClassifier::UmlClassInsertedAsInterface
library.uml#/0/catalog/Book  uml::Class  matched by umlToJavaClassifier::UmlClassInsertedAsEnum, umlToJavaClassifier::UmlClassInsertedAsInterface
library.uml#/0/catalog/LibraryCard  uml::Class  matched by umlToJavaClassifier::UmlClassInsertedAsEnum, umlToJavaClassifier::UmlClassInsertedAsInterface
library.uml#/0/catalog/Member  uml::Class  matched by umlToJavaClassifier::UmlClassInsertedAsEnum, umlToJavaClassifier::UmlClassInsertedAsInterface
```

### Left out

```
library.uml#/0/catalog/Identifiable/getId/@ownedParameter.0  uml::Parameter  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/catalog/Borrowable/borrow/@ownedParameter.0  uml::Parameter  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/catalog/Media/Borrowable  uml::InterfaceRealization  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/catalog/Media/describe/returnParameter  uml::Parameter  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/catalog/Book/@generalization.0  uml::Generalization  nothing corresponds to it, so tearing it down can only disturb what references it
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

## Against config8 from scratch

The migrated models describe exactly what `baselines/config8` describes. Under `--preserve report` nothing is carried over into the models, so what is left is what the target rules derive - and that is what the baseline derives from the same UML.

## Does the Java compile

No, 1 error:

```
Member.java:32 missing return statement
```

## What is here

`model/library.uml` and `src/catalog/*.java` as this run left them, and the rule registry the
VSUM carries afterwards. Left out: the standard library stubs JaMoPP derives under
`src/java`, and the VSUM's own bookkeeping under `vsum`, which only records identities and
the location it was written at.
