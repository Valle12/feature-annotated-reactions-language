# config9 migrated to config4

| | |
|---|---|
| input | the config9 baseline, `baselines/config9` |
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
| dirty rules | 20 |
| affected elements | 7 |
| preservation policy | REPORT |
| elements that would be kept | 7 |
| elements that could not be kept | 2 |
| open decisions nobody answered | 0 |
| items left to deal with by hand | 9 |
| phases | rule-diff, load, roots, dominance, classify, left-out, view-open, selection, snapshot, preregister, delete-commit, reinsert-commit, view-close, preserve, refresh |

## What the rule diff and the trigger mechanism found

| | |
|---|---|
| rules in the persisted registry | 140 |
| rules in the new specifications | 120 |
| dirty rules | 20 (0 added, 20 removed) |
| dirty rules whose trigger matches a source element | 8 |
| source elements probed | 54 |
| elements in the models | 437 |
| matched elements | 7 |
| elements added as referrers | 0 |
| elements left out | 15 |

### Dirty rules

```
- javaToUmlAttribute::JavaAttributeCreatedInClassEnforceAccessorGeneration  matches 0 source element(s)
- javaToUmlAttribute::JavaAttributeCreatedInEnumEnforceAccessorGeneration  matches 0 source element(s)
- javaToUmlAttribute::JavaAttributeMadeStaticRewriteCallSites  matches 0 source element(s)
- javaToUmlAttribute::JavaClassMethodInsertedInClassReplaceAutoAccessor  matches 0 source element(s)
- javaToUmlAttribute::JavaClassMethodInsertedInEnumReplaceAutoAccessor  matches 0 source element(s)
- javaToUmlAttribute::JavaFieldRemovedFromClassDeleteAccessors  matches 0 source element(s)
- javaToUmlAttribute::JavaFieldRemovedFromEnumDeleteAccessors  matches 0 source element(s)
- javaToUmlAttribute::JavaFieldRenamedRenameAccessors  matches 0 source element(s)
- javaToUmlClassifier::JavaClassInsertedAddDefaultConstructor  matches 0 source element(s)
- javaToUmlClassifier::JavaClassRenamedRenameConstructors  matches 0 source element(s)
- javaToUmlClassifier::JavaInterfaceCreatedAddPrefix  matches 0 source element(s)
- javaToUmlMethod::JavaMethodMadeStaticRewriteCallSites  matches 0 source element(s)
- umlToJavaAttribute::UmlAttributeMadeStaticRewriteCallSites  matches 1 source element(s)
- umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration  matches 10 source element(s)
- umlToJavaAttribute::UmlPropertyInsertedInDataTypeEnforceAccessorGeneration  matches 1 source element(s)
- umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor  matches 4 source element(s)
- umlToJavaClassifier::UmlClassRenamedRenameConstructors  matches 4 source element(s)
- umlToJavaClassifier::UmlInterfaceInsertedAddPrefix  matches 2 source element(s)
- umlToJavaClassifier::UmlOperationInsertedReplaceAutoDefault  matches 8 source element(s)
- umlToJavaMethod::UmlOperationMadeStaticRewriteCallSites  matches 1 source element(s)
```

### Affected elements

```
library.uml#/0/catalog/Identifiable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/IBorrowable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/Isbn/code  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInDataTypeEnforceAccessorGeneration
library.uml#/0/catalog/MediaImpl  uml::Class  matched by umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor, umlToJavaClassifier::UmlClassRenamedRenameConstructors
library.uml#/0/catalog/Book  uml::Class  matched by umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor, umlToJavaClassifier::UmlClassRenamedRenameConstructors
library.uml#/0/catalog/LibraryCard  uml::Class  matched by umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor, umlToJavaClassifier::UmlClassRenamedRenameConstructors
library.uml#/0/catalog/Member  uml::Class  matched by umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor, umlToJavaClassifier::UmlClassRenamedRenameConstructors
```

### Left out

```
library.uml#/0/catalog/Identifiable/getId/@ownedParameter.0  uml::Parameter  nothing corresponds to it, so tearing it down can only disturb what references it
library.uml#/0/catalog/IBorrowable/borrow/@ownedParameter.0  uml::Parameter  nothing corresponds to it, so tearing it down can only disturb what references it
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

## Against config4 from scratch

The migrated models and `baselines/config4` do not describe the same thing about 7 classifier(s), which is the number the matrix carries. Each line below names a classifier and how the two differ, per model, so a classifier wrong in both is listed twice here and counted once there; `expected` is the baseline.

### UML, 7 places

```
MISSING  Borrowable
  expected: interface | generalizes Identifiable | operation public borrow(memberId:int):boolean
DIFFERS  Isbn
  expected: dataType | attribute public code:String
  actual:   dataType | attribute private code:String
DIFFERS  MediaImpl
  expected: class abstract | realizes Borrowable | attribute public title:String | attribute protected mediaId:int | attribute public type:MediaType | attribute public weight:double | operation public describe():void
  actual:   class abstract | realizes IBorrowable | attribute private title:String | attribute private mediaId:int | attribute private type:MediaType | attribute private weight:double | operation public describe():void | operation public MediaImpl():void
DIFFERS  Book
  expected: class abstract | generalizes MediaImpl | attribute private isbn:Isbn | attribute public pageCount:int | operation public describe():void
  actual:   class abstract | generalizes MediaImpl | attribute private isbn:Isbn | attribute private pageCount:int | operation public describe():void | operation public Book():void
DIFFERS  LibraryCard
  expected: class final | attribute public static cardNumber:String
  actual:   class final | attribute private static cardNumber:String | operation public LibraryCard():void
DIFFERS  Member
  expected: class | attribute public name:String | attribute public active:boolean | attribute public borrowed:MediaImpl[0..*] | operation public static register(card:LibraryCard):void | operation public totalWeight():double
  actual:   class | attribute private name:String | attribute private active:boolean | attribute private borrowed:MediaImpl[0..*] | operation public static register(card:LibraryCard):void | operation public totalWeight():double | operation public Member():void
UNEXPECTED  IBorrowable -> interface | generalizes Identifiable | operation public borrow(memberId:int):boolean
```

### Java, 7 places

```
DIFFERS  Book
  expected: class public abstract  | extends MediaImpl | field private isbn:Isbn | method public getIsbn():Isbn | method public setIsbn(isbn:Isbn):void | field public pageCount:int | method public getPageCount():int | method public setPageCount(pageCount:int):void | method public final describe():void
  actual:   class public abstract  | extends MediaImpl | field private isbn:Isbn | method public getIsbn():Isbn | method public setIsbn(isbn:Isbn):void | field private pageCount:int | method public getPageCount():int | method public setPageCount(pageCount:int):void | method public final describe():void | member Book
MISSING  Borrowable
  expected: interface public  | extends Identifiable | method public borrow(memberId:int):boolean
DIFFERS  Isbn
  expected: class public  | field public code:String | method public getCode():String | method public setCode(code:String):void
  actual:   class public  | field private code:String | method public getCode():String | method public setCode(code:String):void
DIFFERS  LibraryCard
  expected: class public final  | field public static cardNumber:String | method public getCardNumber():String | method public setCardNumber(cardNumber:String):void
  actual:   class public final  | field private static cardNumber:String | method public getCardNumber():String | method public setCardNumber(cardNumber:String):void | member LibraryCard
DIFFERS  MediaImpl
  expected: class public abstract  | implements Borrowable | field public title:String | method public getTitle():String | method public setTitle(title:String):void | field protected mediaId:int | method public getMediaId():int | method public setMediaId(mediaId:int):void | field public type:MediaType | method public getType():MediaType | method public setType(type:MediaType):void | field public weight:double | method public getWeight():double | method public setWeight(weight:double):void | method public describe():void
  actual:   class public abstract  | implements IBorrowable | field private title:String | method public getTitle():String | method public setTitle(title:String):void | field private mediaId:int | method public getMediaId():int | method public setMediaId(mediaId:int):void | field private type:MediaType | method public getType():MediaType | method public setType(type:MediaType):void | field private weight:double | method public getWeight():double | method public setWeight(weight:double):void | method public describe():void | member MediaImpl
DIFFERS  Member
  expected: class public  | field public name:String | method public getName():String | method public setName(name:String):void | field public active:boolean | method public getActive():boolean | method public setActive(active:boolean):void | field public borrowed:ArrayList<MediaImpl> | method public getBorrowed():ArrayList<MediaImpl> | method public setBorrowed(borrowed:ArrayList<MediaImpl>):void | method public static register(card:LibraryCard):void | method public totalWeight():double
  actual:   class public  | field private name:String | method public getName():String | method public setName(name:String):void | field private active:boolean | method public getActive():boolean | method public setActive(active:boolean):void | field private borrowed:ArrayList<MediaImpl> | method public getBorrowed():ArrayList<MediaImpl> | method public setBorrowed(borrowed:ArrayList<MediaImpl>):void | method public final static register(card:LibraryCard):void | method public totalWeight():double | member Member
UNEXPECTED  IBorrowable -> interface public  | extends Identifiable | method public borrow(memberId:int):boolean
```

## What could not be kept

- references::IdentifierReference in LibraryCard.getCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@returnValue - the counterpart feature is single-valued and the new rules already set it (statements::Return.returnValue already holds references::SelfReference)
- references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.3/@statements.0/@expression/@value - the counterpart feature is single-valued and the new rules already set it (expressions::AssignmentExpression.value already holds references::IdentifierReference)

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
