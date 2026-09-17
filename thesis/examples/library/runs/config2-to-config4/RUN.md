# config2 migrated to config4

| | |
|---|---|
| input | the config2 baseline, `baselines/config2` |
| rules | `umljava-config4.jar` |
| dominance | explicit, uml |

Equivalent command:

```
migration --model <vsum> --propagations umljava-config4.jar \
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
| dirty rules | 6 |
| affected elements | 3 |
| preservation policy | REPORT |
| elements that would be kept | 0 |
| elements that could not be kept | 8 |
| open decisions nobody answered | 0 |
| items left to deal with by hand | 8 |
| phases | rule-diff, load, roots, dominance, classify, left-out, view-open, selection, snapshot, preregister, delete-commit, reinsert-commit, view-close, preserve, refresh |

## What the rule diff and the trigger mechanism found

| | |
|---|---|
| rules in the persisted registry | 118 |
| rules in the new specifications | 120 |
| dirty rules | 6 (4 added, 2 removed) |
| dirty rules whose trigger matches a source element | 2 |
| source elements probed | 50 |
| elements in the models | 424 |
| matched elements | 3 |
| elements added as referrers | 0 |
| elements left out | 15 |

### Dirty rules

```
+ javaToUmlClassifier::JavaClassImplementAddedAppendSuffix  matches 0 source element(s)
+ javaToUmlClassifier::JavaClassImplementRemovedStripSuffix  matches 0 source element(s)
- javaToUmlClassifier::JavaInterfaceCreatedAddPrefix  matches 0 source element(s)
- umlToJavaClassifier::UmlInterfaceInsertedAddPrefix  matches 2 source element(s)
+ umlToJavaClassifier::UmlInterfaceRealizationCreatedAddSuffix  matches 1 source element(s)
+ umlToJavaClassifier::UmlInterfaceRealizationRemovedStripSuffix  matches 0 source element(s)
```

### Affected elements

```
library.uml#/0/catalog/Identifiable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/IBorrowable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/Media/Borrowable  uml::InterfaceRealization  matched by umlToJavaClassifier::UmlInterfaceRealizationCreatedAddSuffix
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

## Against config4 from scratch

The migrated models and `baselines/config4` do not describe the same thing about 3 classifier(s), which is the number the matrix carries. Each line below names a classifier and how the two differ, per model, so a classifier wrong in both is listed twice here and counted once there; `expected` is the baseline.

### UML, 3 places

```
MISSING  Borrowable
  expected: interface | generalizes Identifiable | operation public borrow(memberId:int):boolean
DIFFERS  MediaImpl
  expected: class abstract | realizes Borrowable | attribute public title:String | attribute protected mediaId:int | attribute public type:MediaType | attribute public weight:double | operation public describe():void
  actual:   class abstract | realizes IBorrowable | attribute public title:String | attribute protected mediaId:int | attribute public type:MediaType | attribute public weight:double | operation public describe():void
UNEXPECTED  IBorrowable -> interface | generalizes Identifiable | operation public borrow(memberId:int):boolean
```

### Java, 3 places

```
MISSING  Borrowable
  expected: interface public  | extends Identifiable | method public borrow(memberId:int):boolean
DIFFERS  MediaImpl
  expected: class public abstract  | implements Borrowable | field public title:String | method public getTitle():String | method public setTitle(title:String):void | field protected mediaId:int | method public getMediaId():int | method public setMediaId(mediaId:int):void | field public type:MediaType | method public getType():MediaType | method public setType(type:MediaType):void | field public weight:double | method public getWeight():double | method public setWeight(weight:double):void | method public describe():void
  actual:   class public abstract  | implements IBorrowable | field public title:String | method public getTitle():String | method public setTitle(title:String):void | field protected mediaId:int | method public getMediaId():int | method public setMediaId(mediaId:int):void | field public type:MediaType | method public getType():MediaType | method public setType(type:MediaType):void | field public weight:double | method public getWeight():double | method public setWeight(weight:double):void | method public describe():void
UNEXPECTED  IBorrowable -> interface public  | extends Identifiable | method public borrow(memberId:int):boolean
```

## What could not be kept

- containers::CompilationUnit 'catalog.Media.java' at src/catalog/Media.java#0/ - the model file has no counterpart after the migration
- imports::ClassifierImport at src/catalog/Book.java#0/@imports.0.classifier - it references an element that no longer exists (the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart)
- references::MethodCall in Member.totalWeight.Block at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.1/@statement/@statements.0/@expression/@value/@next.target - it references an element that no longer exists (the value members::ClassMethod 'getWeight' in Media at src/catalog/Media.java#0/@classifiers.0/@members.10 has no counterpart)
- types::ClassifierReference in Book at src/catalog/Book.java#0/@classifiers.0/@extends/@classifierReferences.0.target - it references an element that no longer exists (the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart)
- types::ClassifierReference in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.6/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target - it references an element that no longer exists (the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart)
- types::ClassifierReference in Member.getBorrowed at src/catalog/Member.java#0/@classifiers.0/@members.7/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target - it references an element that no longer exists (the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart)
- types::ClassifierReference in Member.setBorrowed.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.8/@parameters.0/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target - it references an element that no longer exists (the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart)
- types::ClassifierReference in Member.totalWeight.media at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.1/@next/@typeReference/@classifierReferences.0.target - it references an element that no longer exists (the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart)

## Does the Java compile

Yes; `javac` reports nothing about `src/catalog`.

## What is here

`model/library.uml` and `src/catalog/*.java` as this run left them, and the rule registry the
VSUM carries afterwards. Left out: the standard library stubs JaMoPP derives under
`src/java`, and the VSUM's own bookkeeping under `vsum`, which only records identities and
the location it was written at.
