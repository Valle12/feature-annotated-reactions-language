# config4 migrated to config2

| | |
|---|---|
| input | the config4 baseline, `baselines/config4` |
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
| dirty rules | 6 |
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
| rules in the persisted registry | 120 |
| rules in the new specifications | 118 |
| dirty rules | 6 (2 added, 4 removed) |
| dirty rules whose trigger matches a source element | 2 |
| source elements probed | 50 |
| elements in the models | 424 |
| matched elements | 3 |
| elements added as referrers | 0 |
| elements left out | 15 |

### Dirty rules

```
- javaToUmlClassifier::JavaClassImplementAddedAppendSuffix  matches 0 source element(s)
- javaToUmlClassifier::JavaClassImplementRemovedStripSuffix  matches 0 source element(s)
+ javaToUmlClassifier::JavaInterfaceCreatedAddPrefix  matches 0 source element(s)
+ umlToJavaClassifier::UmlInterfaceInsertedAddPrefix  matches 2 source element(s)
- umlToJavaClassifier::UmlInterfaceRealizationCreatedAddSuffix  matches 1 source element(s)
- umlToJavaClassifier::UmlInterfaceRealizationRemovedStripSuffix  matches 0 source element(s)
```

### Affected elements

```
library.uml#/0/catalog/Identifiable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/Borrowable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/MediaImpl/Borrowable  uml::InterfaceRealization  matched by umlToJavaClassifier::UmlInterfaceRealizationCreatedAddSuffix
```

### Left out

```
library.uml#/0/catalog/Identifiable/getId/@ownedParameter.0  uml::Parameter  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/catalog/Borrowable/borrow/@ownedParameter.0  uml::Parameter  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/catalog/MediaImpl/describe/returnParameter  uml::Parameter  nothing corresponds to it, so tearing it down can only disturb what references it
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

The migrated models and `baselines/config2` do not describe the same thing about 4 classifier(s), which is the number the matrix carries. Each line below names a classifier and how the two differ, per model, so a classifier wrong in both is listed twice here and counted once there; `expected` is the baseline.

### UML, 4 places

```
MISSING  Media
  expected: class abstract | realizes IBorrowable | attribute public title:String | attribute protected mediaId:int | attribute public type:MediaType | attribute public weight:double | operation public describe():void
DIFFERS  Book
  expected: class abstract | generalizes Media | attribute private isbn:Isbn | attribute public pageCount:int | operation public describe():void
  actual:   class abstract | generalizes MediaImpl | attribute private isbn:Isbn | attribute public pageCount:int | operation public describe():void
DIFFERS  Member
  expected: class | attribute public name:String | attribute public active:boolean | attribute public borrowed:Media[0..*] | operation public static register(card:LibraryCard):void | operation public totalWeight():double
  actual:   class | attribute public name:String | attribute public active:boolean | attribute public borrowed:MediaImpl[0..*] | operation public static register(card:LibraryCard):void | operation public totalWeight():double
UNEXPECTED  MediaImpl -> class abstract | realizes IBorrowable | attribute public title:String | attribute protected mediaId:int | attribute public type:MediaType | attribute public weight:double | operation public describe():void
```

### Java, 4 places

```
DIFFERS  Book
  expected: class public abstract  | extends Media | field private isbn:Isbn | method public getIsbn():Isbn | method public setIsbn(isbn:Isbn):void | field public pageCount:int | method public getPageCount():int | method public setPageCount(pageCount:int):void | method public final describe():void
  actual:   class public abstract  | extends MediaImpl | field private isbn:Isbn | method public getIsbn():Isbn | method public setIsbn(isbn:Isbn):void | field public pageCount:int | method public getPageCount():int | method public setPageCount(pageCount:int):void | method public final describe():void
MISSING  Media
  expected: class public abstract  | implements IBorrowable | field public title:String | method public getTitle():String | method public setTitle(title:String):void | field protected mediaId:int | method public getMediaId():int | method public setMediaId(mediaId:int):void | field public type:MediaType | method public getType():MediaType | method public setType(type:MediaType):void | field public weight:double | method public getWeight():double | method public setWeight(weight:double):void | method public describe():void
DIFFERS  Member
  expected: class public  | field public name:String | method public getName():String | method public setName(name:String):void | field public active:boolean | method public getActive():boolean | method public setActive(active:boolean):void | field public borrowed:ArrayList<Media> | method public getBorrowed():ArrayList<Media> | method public setBorrowed(borrowed:ArrayList<Media>):void | method public static register(card:LibraryCard):void | method public totalWeight():double
  actual:   class public  | field public name:String | method public getName():String | method public setName(name:String):void | field public active:boolean | method public getActive():boolean | method public setActive(active:boolean):void | field public borrowed:ArrayList<MediaImpl> | method public getBorrowed():ArrayList<MediaImpl> | method public setBorrowed(borrowed:ArrayList<MediaImpl>):void | method public static register(card:LibraryCard):void | method public totalWeight():double
UNEXPECTED  MediaImpl -> class public abstract  | implements IBorrowable | field public title:String | method public getTitle():String | method public setTitle(title:String):void | field protected mediaId:int | method public getMediaId():int | method public setMediaId(mediaId:int):void | field public type:MediaType | method public getType():MediaType | method public setType(type:MediaType):void | field public weight:double | method public getWeight():double | method public setWeight(weight:double):void | method public describe():void
```

## What could not be kept

- containers::CompilationUnit 'catalog.Borrowable.java' at src/catalog/Borrowable.java#0/ - the model file has no counterpart after the migration
- imports::ClassifierImport at src/catalog/MediaImpl.java#0/@imports.0.classifier - it references an element that no longer exists (the value classifiers::Interface 'Borrowable' at src/catalog/Borrowable.java#0/@classifiers.0 has no counterpart)
- types::ClassifierReference in MediaImpl at src/catalog/MediaImpl.java#0/@classifiers.0/@implements.0/@classifierReferences.0.target - it references an element that no longer exists (the value classifiers::Interface 'Borrowable' at src/catalog/Borrowable.java#0/@classifiers.0 has no counterpart)

## Does the Java compile

Yes; `javac` reports nothing about `src/catalog`.

## What is here

`model/library.uml` and `src/catalog/*.java` as this run left them, and the rule registry the
VSUM carries afterwards. Left out: the standard library stubs JaMoPP derives under
`src/java`, and the VSUM's own bookkeeping under `vsum`, which only records identities and
the location it was written at.
