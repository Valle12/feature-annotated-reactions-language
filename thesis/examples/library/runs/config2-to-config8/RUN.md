# config2 migrated to config8

| | |
|---|---|
| input | the config2 baseline, `baselines/config2` |
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
| dirty rules | 8 |
| affected elements | 8 |
| preservation policy | REPORT |
| elements that would be kept | 12 |
| elements that could not be kept | 1 |
| open decisions nobody answered | 1 |
| items left to deal with by hand | 14 |
| phases | rule-diff, load, roots, dominance, classify, left-out, view-open, selection, snapshot, preregister, delete-commit, reinsert-commit, view-close, preserve, refresh |

## What the rule diff and the trigger mechanism found

| | |
|---|---|
| rules in the persisted registry | 118 |
| rules in the new specifications | 116 |
| dirty rules | 8 (3 added, 5 removed) |
| dirty rules whose trigger matches a source element | 5 |
| source elements probed | 50 |
| elements in the models | 424 |
| matched elements | 8 |
| elements added as referrers | 0 |
| elements left out | 15 |

### Dirty rules

```
- javaToUmlClassifier::JavaClassInserted  matches 0 source element(s)
+ javaToUmlClassifier::JavaClassInsertedAsEnum  matches 0 source element(s)
- javaToUmlClassifier::JavaInterfaceCreatedAddPrefix  matches 0 source element(s)
- umlToJavaClassifier::UmlClassInserted  matches 4 source element(s)
+ umlToJavaClassifier::UmlClassInsertedAsEnum  matches 4 source element(s)
- umlToJavaClassifier::UmlDataTypeInserted  matches 2 source element(s)
+ umlToJavaClassifier::UmlDataTypeInsertedAsRecord  matches 2 source element(s)
- umlToJavaClassifier::UmlInterfaceInsertedAddPrefix  matches 2 source element(s)
```

### Affected elements

```
library.uml#/0/catalog/Identifiable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/IBorrowable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/MediaType  uml::Enumeration  matched by umlToJavaClassifier::UmlDataTypeInserted, umlToJavaClassifier::UmlDataTypeInsertedAsRecord
library.uml#/0/catalog/Isbn  uml::DataType  matched by umlToJavaClassifier::UmlDataTypeInserted, umlToJavaClassifier::UmlDataTypeInsertedAsRecord
library.uml#/0/catalog/Media  uml::Class  matched by umlToJavaClassifier::UmlClassInserted, umlToJavaClassifier::UmlClassInsertedAsEnum
library.uml#/0/catalog/Book  uml::Class  matched by umlToJavaClassifier::UmlClassInserted, umlToJavaClassifier::UmlClassInsertedAsEnum
library.uml#/0/catalog/LibraryCard  uml::Class  matched by umlToJavaClassifier::UmlClassInserted, umlToJavaClassifier::UmlClassInsertedAsEnum
library.uml#/0/catalog/Member  uml::Class  matched by umlToJavaClassifier::UmlClassInserted, umlToJavaClassifier::UmlClassInsertedAsEnum
```

### Left out

```
library.uml#/0/catalog/Identifiable/getId/@ownedParameter.0  uml::Parameter  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/catalog/IBorrowable/borrow/@ownedParameter.0  uml::Parameter  nothing corresponds to it, so tearing it down can only disturb what references it
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

## Against config8 from scratch

The migrated models and `baselines/config8` do not describe the same thing about 3 classifier(s), which is the number the matrix carries. Each line below names a classifier and how the two differ, per model, so a classifier wrong in both is listed twice here and counted once there; `expected` is the baseline.

### UML, 3 places

```
MISSING  Borrowable
  expected: interface | generalizes Identifiable | operation public borrow(memberId:int):boolean
DIFFERS  Media
  expected: class abstract | realizes Borrowable | attribute public title:String | attribute protected mediaId:int | attribute public type:MediaType | attribute public weight:double | operation public describe():void
  actual:   class abstract | realizes IBorrowable | attribute public title:String | attribute protected mediaId:int | attribute public type:MediaType | attribute public weight:double | operation public describe():void
UNEXPECTED  IBorrowable -> interface | generalizes Identifiable | operation public borrow(memberId:int):boolean
```

### Java, 2 places

```
MISSING  Borrowable
  expected: interface public  | extends Identifiable | method public borrow(memberId:int):boolean
UNEXPECTED  IBorrowable -> interface public  | extends Identifiable | method public borrow(memberId:int):boolean
```

## What could not be kept

- imports::ClassifierImport at src/catalog/Media.java#0/@imports.0 - several migrated elements could be the same one and nobody chose (it could be [imports::ClassifierImport at src/catalog/Media.java#0/@imports.0])

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
