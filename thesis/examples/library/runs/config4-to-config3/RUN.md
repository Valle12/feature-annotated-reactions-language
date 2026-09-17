# config4 migrated to config3

| | |
|---|---|
| input | the config4 baseline, `baselines/config4` |
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
| dirty rules | 13 |
| affected elements | 12 |
| preservation policy | REPORT |
| elements that would be kept | 10 |
| elements that could not be kept | 0 |
| open decisions nobody answered | 0 |
| items left to deal with by hand | 10 |
| phases | rule-diff, load, roots, dominance, classify, left-out, view-open, selection, snapshot, preregister, delete-commit, reinsert-commit, view-close, preserve, refresh |

## What the rule diff and the trigger mechanism found

| | |
|---|---|
| rules in the persisted registry | 120 |
| rules in the new specifications | 125 |
| dirty rules | 13 (9 added, 4 removed) |
| dirty rules whose trigger matches a source element | 3 |
| source elements probed | 50 |
| elements in the models | 424 |
| matched elements | 12 |
| elements added as referrers | 0 |
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
- javaToUmlClassifier::JavaClassImplementAddedAppendSuffix  matches 0 source element(s)
- javaToUmlClassifier::JavaClassImplementRemovedStripSuffix  matches 0 source element(s)
+ umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration  matches 10 source element(s)
+ umlToJavaAttribute::UmlPropertyInsertedInDataTypeEnforceAccessorGeneration  matches 1 source element(s)
- umlToJavaClassifier::UmlInterfaceRealizationCreatedAddSuffix  matches 1 source element(s)
- umlToJavaClassifier::UmlInterfaceRealizationRemovedStripSuffix  matches 0 source element(s)
```

### Affected elements

```
library.uml#/0/catalog/Isbn/code  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInDataTypeEnforceAccessorGeneration
library.uml#/0/catalog/MediaImpl/title  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/MediaImpl/mediaId  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/MediaImpl/type  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/MediaImpl/weight  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/MediaImpl/Borrowable  uml::InterfaceRealization  matched by umlToJavaClassifier::UmlInterfaceRealizationCreatedAddSuffix
library.uml#/0/catalog/Book/isbn  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Book/pageCount  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/LibraryCard/cardNumber  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Member/name  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Member/active  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Member/borrowed  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
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

## Against config3 from scratch

The migrated models and `baselines/config3` do not describe the same thing about 4 classifier(s), which is the number the matrix carries. Each line below names a classifier and how the two differ, per model, so a classifier wrong in both is listed twice here and counted once there; `expected` is the baseline.

### UML, 4 places

```
MISSING  Media
  expected: class abstract | realizes Borrowable | attribute private title:String | attribute private mediaId:int | attribute private type:MediaType | attribute private weight:double | operation public describe():void
DIFFERS  Book
  expected: class abstract | generalizes Media | attribute private isbn:Isbn | attribute private pageCount:int | operation public describe():void
  actual:   class abstract | generalizes MediaImpl | attribute private isbn:Isbn | attribute private pageCount:int | operation public describe():void
DIFFERS  Member
  expected: class | attribute private name:String | attribute private active:boolean | attribute private borrowed:Media[0..*] | operation public static register(card:LibraryCard):void | operation public totalWeight():double
  actual:   class | attribute private name:String | attribute private active:boolean | attribute private borrowed:MediaImpl[0..*] | operation public static register(card:LibraryCard):void | operation public totalWeight():double
UNEXPECTED  MediaImpl -> class abstract | realizes Borrowable | attribute private title:String | attribute private mediaId:int | attribute private type:MediaType | attribute private weight:double | operation public describe():void
```

### Java, 4 places

```
DIFFERS  Book
  expected: class public abstract  | extends Media | field private isbn:Isbn | method public getIsbn():Isbn | method public setIsbn(isbn:Isbn):void | field private pageCount:int | method public getPageCount():int | method public setPageCount(pageCount:int):void | method public final describe():void
  actual:   class public abstract  | extends MediaImpl | method public final describe():void | field private isbn:Isbn | method public getIsbn():Isbn | method public setIsbn(isbn:Isbn):void | field private pageCount:int | method public getPageCount():int | method public setPageCount(pageCount:int):void
MISSING  Media
  expected: class public abstract  | implements Borrowable | field private title:String | method public getTitle():String | method public setTitle(title:String):void | field private mediaId:int | method public getMediaId():int | method public setMediaId(mediaId:int):void | field private type:MediaType | method public getType():MediaType | method public setType(type:MediaType):void | field private weight:double | method public getWeight():double | method public setWeight(weight:double):void | method public describe():void
DIFFERS  Member
  expected: class public  | field private name:String | method public getName():String | method public setName(name:String):void | field private active:boolean | method public getActive():boolean | method public setActive(active:boolean):void | field private borrowed:ArrayList<Media> | method public getBorrowed():ArrayList<Media> | method public setBorrowed(borrowed:ArrayList<Media>):void | method public static register(card:LibraryCard):void | method public totalWeight():double
  actual:   class public  | method public static register(card:LibraryCard):void | method public totalWeight():double | field private name:String | method public getName():String | method public setName(name:String):void | field private active:boolean | method public getActive():boolean | method public setActive(active:boolean):void | field private borrowed:ArrayList<MediaImpl> | method public getBorrowed():ArrayList<MediaImpl> | method public setBorrowed(borrowed:ArrayList<MediaImpl>):void
UNEXPECTED  MediaImpl -> class public abstract  | implements Borrowable | method public describe():void | field private title:String | method public getTitle():String | method public setTitle(title:String):void | field private mediaId:int | method public getMediaId():int | method public setMediaId(mediaId:int):void | field private type:MediaType | method public getType():MediaType | method public setType(type:MediaType):void | field private weight:double | method public getWeight():double | method public setWeight(weight:double):void
```

## Does the Java compile

Yes; `javac` reports nothing about `src/catalog`.

## What is here

`model/library.uml` and `src/catalog/*.java` as this run left them, and the rule registry the
VSUM carries afterwards. Left out: the standard library stubs JaMoPP derives under
`src/java`, and the VSUM's own bookkeeping under `vsum`, which only records identities and
the location it was written at.
