# config9 migrated to config7

| | |
|---|---|
| input | the config9 baseline, `baselines/config9` |
| rules | `umljava-config7.jar` |
| dominance | explicit, uml |

Equivalent command:

```
migration --model <vsum> --propagations umljava-config7.jar \
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
| dirty rules | 30 |
| affected elements | 8 |
| preservation policy | REPORT |
| elements that would be kept | 38 |
| elements that could not be kept | 5 |
| open decisions nobody answered | 2 |
| items left to deal with by hand | 45 |
| phases | rule-diff, load, roots, dominance, classify, left-out, view-open, selection, snapshot, preregister, delete-commit, reinsert-commit, view-close, preserve, refresh |

## What the rule diff and the trigger mechanism found

| | |
|---|---|
| rules in the persisted registry | 140 |
| rules in the new specifications | 116 |
| dirty rules | 30 (3 added, 27 removed) |
| dirty rules whose trigger matches a source element | 13 |
| source elements probed | 54 |
| elements in the models | 437 |
| matched elements | 8 |
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
- javaToUmlClassifier::JavaClassImplementAddedAppendSuffix  matches 0 source element(s)
- javaToUmlClassifier::JavaClassImplementRemovedStripSuffix  matches 0 source element(s)
- javaToUmlClassifier::JavaClassInserted  matches 0 source element(s)
- javaToUmlClassifier::JavaClassInsertedAddDefaultConstructor  matches 0 source element(s)
+ javaToUmlClassifier::JavaClassInsertedAsInterface  matches 0 source element(s)
- javaToUmlClassifier::JavaClassRenamedRenameConstructors  matches 0 source element(s)
- javaToUmlClassifier::JavaInterfaceCreatedAddPrefix  matches 0 source element(s)
- javaToUmlMethod::JavaMethodMadeStaticRewriteCallSites  matches 0 source element(s)
- umlToJavaAttribute::UmlAttributeMadeStaticRewriteCallSites  matches 1 source element(s)
- umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration  matches 10 source element(s)
- umlToJavaAttribute::UmlPropertyInsertedInDataTypeEnforceAccessorGeneration  matches 1 source element(s)
- umlToJavaClassifier::UmlClassInserted  matches 4 source element(s)
- umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor  matches 4 source element(s)
+ umlToJavaClassifier::UmlClassInsertedAsInterface  matches 4 source element(s)
- umlToJavaClassifier::UmlClassRenamedRenameConstructors  matches 4 source element(s)
- umlToJavaClassifier::UmlDataTypeInserted  matches 2 source element(s)
+ umlToJavaClassifier::UmlDataTypeInsertedAsRecord  matches 2 source element(s)
- umlToJavaClassifier::UmlInterfaceInsertedAddPrefix  matches 2 source element(s)
- umlToJavaClassifier::UmlInterfaceRealizationCreatedAddSuffix  matches 1 source element(s)
- umlToJavaClassifier::UmlInterfaceRealizationRemovedStripSuffix  matches 0 source element(s)
- umlToJavaClassifier::UmlOperationInsertedReplaceAutoDefault  matches 8 source element(s)
- umlToJavaMethod::UmlOperationMadeStaticRewriteCallSites  matches 1 source element(s)
```

### Affected elements

```
library.uml#/0/catalog/Identifiable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/IBorrowable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/MediaType  uml::Enumeration  matched by umlToJavaClassifier::UmlDataTypeInserted, umlToJavaClassifier::UmlDataTypeInsertedAsRecord
library.uml#/0/catalog/Isbn  uml::DataType  matched by umlToJavaClassifier::UmlDataTypeInserted, umlToJavaClassifier::UmlDataTypeInsertedAsRecord
library.uml#/0/catalog/MediaImpl  uml::Class  matched by umlToJavaClassifier::UmlClassInserted, umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor, umlToJavaClassifier::UmlClassInsertedAsInterface, umlToJavaClassifier::UmlClassRenamedRenameConstructors
library.uml#/0/catalog/Book  uml::Class  matched by umlToJavaClassifier::UmlClassInserted, umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor, umlToJavaClassifier::UmlClassInsertedAsInterface, umlToJavaClassifier::UmlClassRenamedRenameConstructors
library.uml#/0/catalog/LibraryCard  uml::Class  matched by umlToJavaClassifier::UmlClassInserted, umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor, umlToJavaClassifier::UmlClassInsertedAsInterface, umlToJavaClassifier::UmlClassRenamedRenameConstructors
library.uml#/0/catalog/Member  uml::Class  matched by umlToJavaClassifier::UmlClassInserted, umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor, umlToJavaClassifier::UmlClassInsertedAsInterface, umlToJavaClassifier::UmlClassRenamedRenameConstructors
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

## Against config7 from scratch

The migrated models and `baselines/config7` do not describe the same thing about 8 classifier(s), which is the number the matrix carries. Each line below names a classifier and how the two differ, per model, so a classifier wrong in both is listed twice here and counted once there; `expected` is the baseline.

### UML, 8 places

```
MISSING  Borrowable
  expected: interface | generalizes Identifiable | operation public borrow(memberId:int):boolean
DIFFERS  Isbn
  expected: dataType | attribute public code:String
  actual:   dataType | attribute private code:String
MISSING  Media
  expected: class abstract | realizes Borrowable | attribute public title:String | attribute protected mediaId:int | attribute public type:MediaType | attribute public weight:double | operation public describe():void
DIFFERS  Book
  expected: class abstract | generalizes Media | attribute private isbn:Isbn | attribute public pageCount:int | operation public describe():void
  actual:   class abstract | generalizes MediaImpl | attribute private isbn:Isbn | attribute private pageCount:int | operation public describe():void | operation public Book():void
DIFFERS  LibraryCard
  expected: class final | attribute public static cardNumber:String
  actual:   class final | attribute private static cardNumber:String | operation public LibraryCard():void
DIFFERS  Member
  expected: class | attribute public name:String | attribute public active:boolean | attribute public borrowed:Media[0..*] | operation public static register(card:LibraryCard):void | operation public totalWeight():double
  actual:   class | attribute private name:String | attribute private active:boolean | attribute private borrowed:MediaImpl[0..*] | operation public static register(card:LibraryCard):void | operation public totalWeight():double | operation public Member():void
UNEXPECTED  IBorrowable -> interface | generalizes Identifiable | operation public borrow(memberId:int):boolean
UNEXPECTED  MediaImpl -> class abstract | realizes IBorrowable | attribute private title:String | attribute private mediaId:int | attribute private type:MediaType | attribute private weight:double | operation public describe():void | operation public MediaImpl():void
```

### Java, 8 places

```
DIFFERS  Book
  expected: interface public  | field public static final isbn:Isbn | field public static final pageCount:int | method public describe():void
  actual:   interface public  | field public static final isbn:Isbn | field public static final pageCount:int | method public describe():void | method public Book():void
MISSING  Borrowable
  expected: interface public  | extends Identifiable | method public borrow(memberId:int):boolean
DIFFERS  Isbn
  expected: class public final  | field public code:String | method public getCode():String | method public setCode(code:String):void
  actual:   class public final  | field private code:String | method public getCode():String | method public setCode(code:String):void
DIFFERS  LibraryCard
  expected: interface public  | field public static final cardNumber:String
  actual:   interface public  | field public static final cardNumber:String | method public LibraryCard():void
MISSING  Media
  expected: interface public  | field public static final title:String | field public static final mediaId:int | field public static final type:MediaType | field public static final weight:double | method public describe():void
DIFFERS  Member
  expected: interface public  | field public static final name:String | field public static final active:boolean | field public static final borrowed:ArrayList<Media> | method public register(card:LibraryCard):void | method public totalWeight():double
  actual:   interface public  | field public static final name:String | field public static final active:boolean | field public static final borrowed:ArrayList<MediaImpl> | method public register(card:LibraryCard):void | method public totalWeight():double | method public Member():void
UNEXPECTED  IBorrowable -> interface public  | extends Identifiable | method public borrow(memberId:int):boolean
UNEXPECTED  MediaImpl -> interface public  | field public static final title:String | field public static final mediaId:int | field public static final type:MediaType | field public static final weight:double | method public describe():void | method public MediaImpl():void
```

## What could not be kept

- imports::ClassifierImport at src/catalog/MediaImpl.java#0/@imports.0 - several migrated elements could be the same one and nobody chose (it could be [imports::ClassifierImport at src/catalog/MediaImpl.java#0/@imports.0])
- statements::ForEachLoop in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.11/@statements.1 - the counterpart metaclass has no feature that can hold it (members::InterfaceMethod has no containment feature accepting statements::ForEachLoop)
- statements::LocalVariableStatement in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.11/@statements.0 - the counterpart metaclass has no feature that can hold it (members::InterfaceMethod has no containment feature accepting statements::LocalVariableStatement)
- statements::Return in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.11/@statements.2 - the counterpart metaclass has no feature that can hold it (members::InterfaceMethod has no containment feature accepting statements::Return)
- types::NamespaceClassifierReference in MediaImpl at src/catalog/MediaImpl.java#0/@classifiers.0/@implements.0 - several features of the counterpart metaclass could hold it (classifiers::Interface could hold types::NamespaceClassifierReference in [extends, defaultExtends])

## Does the Java compile

Yes; `javac` reports nothing about `src/catalog`.

## What is here

`model/library.uml` and `src/catalog/*.java` as this run left them, and the rule registry the
VSUM carries afterwards. Left out: the standard library stubs JaMoPP derives under
`src/java`, and the VSUM's own bookkeeping under `vsum`, which only records identities and
the location it was written at.
