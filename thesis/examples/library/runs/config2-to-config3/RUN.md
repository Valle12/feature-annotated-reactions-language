# config2 migrated to config3

| | |
|---|---|
| input | the config2 baseline, `baselines/config2` |
| rules | `umljava-config3.jar` |
| dominance | explicit, uml |

Equivalent command:

```
migration --model <vsum> --propagations umljava-config3.jar \
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
| dirty rules | 11 |
| affected elements | 14 |
| preservation policy | REPORT |
| elements that would be kept | 10 |
| elements that could not be kept | 0 |
| open decisions nobody answered | 0 |
| items left to deal with by hand | 10 |
| phases | rule-diff, load, roots, dominance, classify, left-out, view-open, selection, snapshot, preregister, delete-commit, reinsert-commit, view-close, preserve, refresh |

## What the rule diff and the trigger mechanism found

| | |
|---|---|
| rules in the persisted registry | 118 |
| rules in the new specifications | 125 |
| dirty rules | 11 (9 added, 2 removed) |
| dirty rules whose trigger matches a source element | 3 |
| source elements probed | 50 |
| elements in the models | 424 |
| matched elements | 13 |
| elements added as referrers | 1 |
| elements left out | 15 |

### Dirty rules

```
+ javaToUmlAttribute::JavaAttributeCreatedInClassEnforceAccessorGeneration  matches 0 source element(s)
+ javaToUmlAttribute::JavaAttributeCreatedInEnumEnforceAccessorGeneration  matches 0 source element(s)
+ javaToUmlAttribute::JavaClassMethodInsertedInClassReplaceAutoAccessor  matches 0 source element(s)
+ javaToUmlAttribute::JavaClassMethodInsertedInEnumReplaceAutoAccessor  matches 0 source element(s)
+ javaToUmlAttribute::JavaFieldRemovedFromClassDeleteAccessors  matches 0 source element(s)
+ javaToUmlAttribute::JavaFieldRemovedFromEnumDeleteAccessors  matches 0 source element(s)
+ javaToUmlAttribute::JavaFieldRenamedRenameAccessors  matches 0 source element(s)
- javaToUmlClassifier::JavaInterfaceCreatedAddPrefix  matches 0 source element(s)
+ umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration  matches 10 source element(s)
+ umlToJavaAttribute::UmlPropertyInsertedInDataTypeEnforceAccessorGeneration  matches 1 source element(s)
- umlToJavaClassifier::UmlInterfaceInsertedAddPrefix  matches 2 source element(s)
```

### Affected elements

```
library.uml#/0/catalog/Identifiable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/IBorrowable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/Isbn/code  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInDataTypeEnforceAccessorGeneration
library.uml#/0/catalog/Media/title  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Media/mediaId  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Media/type  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Media/weight  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Book/isbn  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Book/pageCount  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/LibraryCard/cardNumber  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Member/name  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Member/active  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Member/borrowed  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Media/Borrowable  uml::InterfaceRealization  refers to library.uml#/0/catalog/IBorrowable
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

## Against config3 from scratch

The migrated models and `baselines/config3` do not describe the same thing about 3 classifier(s), which is the number the matrix carries. Each line below names a classifier and how the two differ, per model, so a classifier wrong in both is listed twice here and counted once there; `expected` is the baseline.

### UML, 3 places

```
MISSING  Borrowable
  expected: interface | generalizes Identifiable | operation public borrow(memberId:int):boolean
DIFFERS  Media
  expected: class abstract | realizes Borrowable | attribute private title:String | attribute private mediaId:int | attribute private type:MediaType | attribute private weight:double | operation public describe():void
  actual:   class abstract | realizes IBorrowable | attribute private title:String | attribute private mediaId:int | attribute private type:MediaType | attribute private weight:double | operation public describe():void
UNEXPECTED  IBorrowable -> interface | generalizes Identifiable | operation public borrow(memberId:int):boolean
```

### Java, 3 places

```
MISSING  Borrowable
  expected: interface public  | extends Identifiable | method public borrow(memberId:int):boolean
DIFFERS  Media
  expected: class public abstract  | implements Borrowable | field private title:String | method public getTitle():String | method public setTitle(title:String):void | field private mediaId:int | method public getMediaId():int | method public setMediaId(mediaId:int):void | field private type:MediaType | method public getType():MediaType | method public setType(type:MediaType):void | field private weight:double | method public getWeight():double | method public setWeight(weight:double):void | method public describe():void
  actual:   class public abstract  | implements IBorrowable | method public describe():void | field private title:String | method public getTitle():String | method public setTitle(title:String):void | field private mediaId:int | method public getMediaId():int | method public setMediaId(mediaId:int):void | field private type:MediaType | method public getType():MediaType | method public setType(type:MediaType):void | field private weight:double | method public getWeight():double | method public setWeight(weight:double):void
UNEXPECTED  IBorrowable -> interface public  | extends Identifiable | method public borrow(memberId:int):boolean
```

### Java, same content in another order, 2 places

```
DIFFERS  Book
  expected: class public abstract  | extends Media | field private isbn:Isbn | method public getIsbn():Isbn | method public setIsbn(isbn:Isbn):void | field private pageCount:int | method public getPageCount():int | method public setPageCount(pageCount:int):void | method public final describe():void
  actual:   class public abstract  | extends Media | method public final describe():void | field private isbn:Isbn | method public getIsbn():Isbn | method public setIsbn(isbn:Isbn):void | field private pageCount:int | method public getPageCount():int | method public setPageCount(pageCount:int):void
DIFFERS  Member
  expected: class public  | field private name:String | method public getName():String | method public setName(name:String):void | field private active:boolean | method public getActive():boolean | method public setActive(active:boolean):void | field private borrowed:ArrayList<Media> | method public getBorrowed():ArrayList<Media> | method public setBorrowed(borrowed:ArrayList<Media>):void | method public static register(card:LibraryCard):void | method public totalWeight():double
  actual:   class public  | method public static register(card:LibraryCard):void | method public totalWeight():double | field private name:String | method public getName():String | method public setName(name:String):void | field private active:boolean | method public getActive():boolean | method public setActive(active:boolean):void | field private borrowed:ArrayList<Media> | method public getBorrowed():ArrayList<Media> | method public setBorrowed(borrowed:ArrayList<Media>):void
```

## Does the Java compile

Yes; `javac` reports nothing about `src/catalog`.

## What is here

`model/library.uml` and `src/catalog/*.java` as this run left them, and the rule registry the
VSUM carries afterwards. Left out: the standard library stubs JaMoPP derives under
`src/java`, and the VSUM's own bookkeeping under `vsum`, which only records identities and
the location it was written at.
