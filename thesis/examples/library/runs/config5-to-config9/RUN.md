# config5 migrated to config9

| | |
|---|---|
| input | the config5 baseline, `baselines/config5` |
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
| migrated | true |
| migration mode | ID_DIFF |
| fell back to a full migration | false |
| reason for the fallback | - |
| dirty rules | 19 |
| affected elements | 15 |
| preservation policy | REPORT |
| elements that would be kept | 7 |
| elements that could not be kept | 11 |
| open decisions nobody answered | 0 |
| items left to deal with by hand | 18 |
| phases | rule-diff, load, roots, dominance, classify, left-out, view-open, selection, snapshot, preregister, delete-commit, reinsert-commit, view-close, preserve, refresh |

## What the rule diff and the trigger mechanism found

| | |
|---|---|
| rules in the persisted registry | 121 |
| rules in the new specifications | 140 |
| dirty rules | 19 (19 added, 0 removed) |
| dirty rules whose trigger matches a source element | 6 |
| source elements probed | 54 |
| elements in the models | 436 |
| matched elements | 15 |
| elements added as referrers | 0 |
| elements left out | 15 |

### Dirty rules

```
+ javaToUmlAttribute::JavaAttributeCreatedInClassEnforceAccessorGeneration  matches 0 source element(s)
+ javaToUmlAttribute::JavaAttributeCreatedInEnumEnforceAccessorGeneration  matches 0 source element(s)
+ javaToUmlAttribute::JavaAttributeMadeStaticRewriteCallSites  matches 0 source element(s)
+ javaToUmlAttribute::JavaClassMethodInsertedInClassReplaceAutoAccessor  matches 0 source element(s)
+ javaToUmlAttribute::JavaClassMethodInsertedInEnumReplaceAutoAccessor  matches 0 source element(s)
+ javaToUmlAttribute::JavaFieldRemovedFromClassDeleteAccessors  matches 0 source element(s)
+ javaToUmlAttribute::JavaFieldRemovedFromEnumDeleteAccessors  matches 0 source element(s)
+ javaToUmlAttribute::JavaFieldRenamedRenameAccessors  matches 0 source element(s)
+ javaToUmlClassifier::JavaClassImplementAddedAppendSuffix  matches 0 source element(s)
+ javaToUmlClassifier::JavaClassImplementRemovedStripSuffix  matches 0 source element(s)
+ javaToUmlClassifier::JavaInterfaceCreatedAddPrefix  matches 0 source element(s)
+ javaToUmlMethod::JavaMethodMadeStaticRewriteCallSites  matches 0 source element(s)
+ umlToJavaAttribute::UmlAttributeMadeStaticRewriteCallSites  matches 1 source element(s)
+ umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration  matches 10 source element(s)
+ umlToJavaAttribute::UmlPropertyInsertedInDataTypeEnforceAccessorGeneration  matches 1 source element(s)
+ umlToJavaClassifier::UmlInterfaceInsertedAddPrefix  matches 2 source element(s)
+ umlToJavaClassifier::UmlInterfaceRealizationCreatedAddSuffix  matches 1 source element(s)
+ umlToJavaClassifier::UmlInterfaceRealizationRemovedStripSuffix  matches 0 source element(s)
+ umlToJavaMethod::UmlOperationMadeStaticRewriteCallSites  matches 1 source element(s)
```

### Affected elements

```
library.uml#/0/catalog/Identifiable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/Borrowable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/Isbn/code  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInDataTypeEnforceAccessorGeneration
library.uml#/0/catalog/Media/title  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Media/mediaId  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Media/type  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Media/weight  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Media/Borrowable  uml::InterfaceRealization  matched by umlToJavaClassifier::UmlInterfaceRealizationCreatedAddSuffix
library.uml#/0/catalog/Book/isbn  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Book/pageCount  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/LibraryCard/cardNumber  uml::Property  matched by umlToJavaAttribute::UmlAttributeMadeStaticRewriteCallSites, umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Member/name  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Member/active  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Member/borrowed  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration
library.uml#/0/catalog/Member/register  uml::Operation  matched by umlToJavaMethod::UmlOperationMadeStaticRewriteCallSites
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

## Against config9 from scratch

The migrated models hold exactly what `baselines/config9` holds, listed in a different order. Nothing is missing, added or derived differently; a classifier's members simply came back in the order the repropagation rebuilt them in rather than the order a derivation from scratch produces.

### Java, same content in another order, 3 places

```
DIFFERS  Book
  expected: class public abstract  | extends MediaImpl | member Book | field private isbn:Isbn | method public getIsbn():Isbn | method public setIsbn(isbn:Isbn):void | field private pageCount:int | method public getPageCount():int | method public setPageCount(pageCount:int):void | method public final describe():void
  actual:   class public abstract  | extends MediaImpl | member Book | method public final describe():void | field private isbn:Isbn | method public getIsbn():Isbn | method public setIsbn(isbn:Isbn):void | field private pageCount:int | method public getPageCount():int | method public setPageCount(pageCount:int):void
DIFFERS  MediaImpl
  expected: class public abstract  | implements IBorrowable | member MediaImpl | field private title:String | method public getTitle():String | method public setTitle(title:String):void | field private mediaId:int | method public getMediaId():int | method public setMediaId(mediaId:int):void | field private type:MediaType | method public getType():MediaType | method public setType(type:MediaType):void | field private weight:double | method public getWeight():double | method public setWeight(weight:double):void | method public describe():void
  actual:   class public abstract  | implements IBorrowable | member MediaImpl | method public describe():void | field private title:String | method public getTitle():String | method public setTitle(title:String):void | field private mediaId:int | method public getMediaId():int | method public setMediaId(mediaId:int):void | field private type:MediaType | method public getType():MediaType | method public setType(type:MediaType):void | field private weight:double | method public getWeight():double | method public setWeight(weight:double):void
DIFFERS  Member
  expected: class public  | member Member | field private name:String | method public getName():String | method public setName(name:String):void | field private active:boolean | method public getActive():boolean | method public setActive(active:boolean):void | field private borrowed:ArrayList<MediaImpl> | method public getBorrowed():ArrayList<MediaImpl> | method public setBorrowed(borrowed:ArrayList<MediaImpl>):void | method public static final register(card:LibraryCard):void | method public totalWeight():double
  actual:   class public  | member Member | method public totalWeight():double | field private name:String | method public getName():String | method public setName(name:String):void | field private active:boolean | method public getActive():boolean | method public setActive(active:boolean):void | field private borrowed:ArrayList<MediaImpl> | method public getBorrowed():ArrayList<MediaImpl> | method public setBorrowed(borrowed:ArrayList<MediaImpl>):void | method public static final register(card:LibraryCard):void
```

## What could not be kept

- containers::CompilationUnit 'catalog.Borrowable.java' at src/catalog/Borrowable.java#0/ - the model file has no counterpart after the migration
- containers::CompilationUnit 'catalog.Media.java' at src/catalog/Media.java#0/ - the model file has no counterpart after the migration
- imports::ClassifierImport at src/catalog/Book.java#0/@imports.0.classifier - it references an element that no longer exists (the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart)
- references::MethodCall in Member.totalWeight.Block at src/catalog/Member.java#0/@classifiers.0/@members.11/@statements.1/@statement/@statements.0/@expression/@value/@next.target - it references an element that no longer exists (the value members::ClassMethod 'getWeight' in Media at src/catalog/Media.java#0/@classifiers.0/@members.11 has no counterpart)
- references::SelfReference in LibraryCard.getCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@returnValue - the counterpart feature is single-valued and the new rules already set it (statements::Return.returnValue already holds references::IdentifierReference)
- references::SelfReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.3/@statements.0/@expression/@child - the counterpart feature is single-valued and the new rules already set it (expressions::AssignmentExpression.child already holds references::IdentifierReference)
- types::ClassifierReference in Book at src/catalog/Book.java#0/@classifiers.0/@extends/@classifierReferences.0.target - it references an element that no longer exists (the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart)
- types::ClassifierReference in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.7/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target - it references an element that no longer exists (the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart)
- types::ClassifierReference in Member.getBorrowed at src/catalog/Member.java#0/@classifiers.0/@members.8/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target - it references an element that no longer exists (the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart)
- types::ClassifierReference in Member.setBorrowed.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.9/@parameters.0/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target - it references an element that no longer exists (the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart)
- types::ClassifierReference in Member.totalWeight.media at src/catalog/Member.java#0/@classifiers.0/@members.11/@statements.1/@next/@typeReference/@classifierReferences.0.target - it references an element that no longer exists (the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart)

## Does the Java compile

Yes; `javac` reports nothing about `src/catalog`.

## What is here

`model/library.uml` and `src/catalog/*.java` as this run left them, and the rule registry the
VSUM carries afterwards. Left out: the standard library stubs JaMoPP derives under
`src/java`, and the VSUM's own bookkeeping under `vsum`, which only records identities and
the location it was written at.
