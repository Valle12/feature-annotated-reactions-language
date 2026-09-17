# config5 migrated to config7

| | |
|---|---|
| input | the config5 baseline, `baselines/config5` |
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
| dirty rules | 11 |
| affected elements | 6 |
| preservation policy | REPORT |
| elements that would be kept | 29 |
| elements that could not be kept | 5 |
| open decisions nobody answered | 2 |
| items left to deal with by hand | 36 |
| phases | rule-diff, load, roots, dominance, classify, left-out, view-open, selection, snapshot, preregister, delete-commit, reinsert-commit, view-close, preserve, refresh |

## What the rule diff and the trigger mechanism found

| | |
|---|---|
| rules in the persisted registry | 121 |
| rules in the new specifications | 116 |
| dirty rules | 11 (3 added, 8 removed) |
| dirty rules whose trigger matches a source element | 7 |
| source elements probed | 54 |
| elements in the models | 436 |
| matched elements | 6 |
| elements added as referrers | 0 |
| elements left out | 15 |

### Dirty rules

```
- javaToUmlClassifier::JavaClassInserted  matches 0 source element(s)
- javaToUmlClassifier::JavaClassInsertedAddDefaultConstructor  matches 0 source element(s)
+ javaToUmlClassifier::JavaClassInsertedAsInterface  matches 0 source element(s)
- javaToUmlClassifier::JavaClassRenamedRenameConstructors  matches 0 source element(s)
- umlToJavaClassifier::UmlClassInserted  matches 4 source element(s)
- umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor  matches 4 source element(s)
+ umlToJavaClassifier::UmlClassInsertedAsInterface  matches 4 source element(s)
- umlToJavaClassifier::UmlClassRenamedRenameConstructors  matches 4 source element(s)
- umlToJavaClassifier::UmlDataTypeInserted  matches 2 source element(s)
+ umlToJavaClassifier::UmlDataTypeInsertedAsRecord  matches 2 source element(s)
- umlToJavaClassifier::UmlOperationInsertedReplaceAutoDefault  matches 8 source element(s)
```

### Affected elements

```
library.uml#/0/catalog/MediaType  uml::Enumeration  matched by umlToJavaClassifier::UmlDataTypeInserted, umlToJavaClassifier::UmlDataTypeInsertedAsRecord
library.uml#/0/catalog/Isbn  uml::DataType  matched by umlToJavaClassifier::UmlDataTypeInserted, umlToJavaClassifier::UmlDataTypeInsertedAsRecord
library.uml#/0/catalog/Media  uml::Class  matched by umlToJavaClassifier::UmlClassInserted, umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor, umlToJavaClassifier::UmlClassInsertedAsInterface, umlToJavaClassifier::UmlClassRenamedRenameConstructors
library.uml#/0/catalog/Book  uml::Class  matched by umlToJavaClassifier::UmlClassInserted, umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor, umlToJavaClassifier::UmlClassInsertedAsInterface, umlToJavaClassifier::UmlClassRenamedRenameConstructors
library.uml#/0/catalog/LibraryCard  uml::Class  matched by umlToJavaClassifier::UmlClassInserted, umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor, umlToJavaClassifier::UmlClassInsertedAsInterface, umlToJavaClassifier::UmlClassRenamedRenameConstructors
library.uml#/0/catalog/Member  uml::Class  matched by umlToJavaClassifier::UmlClassInserted, umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor, umlToJavaClassifier::UmlClassInsertedAsInterface, umlToJavaClassifier::UmlClassRenamedRenameConstructors
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

## Against config7 from scratch

The migrated models and `baselines/config7` do not describe the same thing about 4 classifier(s), which is the number the matrix carries. Each line below names a classifier and how the two differ, per model, so a classifier wrong in both is listed twice here and counted once there; `expected` is the baseline.

### UML, 4 places

```
DIFFERS  Media
  expected: class abstract | realizes Borrowable | attribute public title:String | attribute protected mediaId:int | attribute public type:MediaType | attribute public weight:double | operation public describe():void
  actual:   class abstract | realizes Borrowable | attribute public title:String | attribute protected mediaId:int | attribute public type:MediaType | attribute public weight:double | operation public describe():void | operation public Media():void
DIFFERS  Book
  expected: class abstract | generalizes Media | attribute private isbn:Isbn | attribute public pageCount:int | operation public describe():void
  actual:   class abstract | generalizes Media | attribute private isbn:Isbn | attribute public pageCount:int | operation public describe():void | operation public Book():void
DIFFERS  LibraryCard
  expected: class final | attribute public static cardNumber:String
  actual:   class final | attribute public static cardNumber:String | operation public LibraryCard():void
DIFFERS  Member
  expected: class | attribute public name:String | attribute public active:boolean | attribute public borrowed:Media[0..*] | operation public static register(card:LibraryCard):void | operation public totalWeight():double
  actual:   class | attribute public name:String | attribute public active:boolean | attribute public borrowed:Media[0..*] | operation public static register(card:LibraryCard):void | operation public totalWeight():double | operation public Member():void
```

### Java, 4 places

```
DIFFERS  Book
  expected: interface public  | field public static final isbn:Isbn | field public static final pageCount:int | method public describe():void
  actual:   interface public  | field public static final isbn:Isbn | field public static final pageCount:int | method public describe():void | method public Book():void
DIFFERS  LibraryCard
  expected: interface public  | field public static final cardNumber:String
  actual:   interface public  | field public static final cardNumber:String | method public LibraryCard():void
DIFFERS  Media
  expected: interface public  | field public static final title:String | field public static final mediaId:int | field public static final type:MediaType | field public static final weight:double | method public describe():void
  actual:   interface public  | field public static final title:String | field public static final mediaId:int | field public static final type:MediaType | field public static final weight:double | method public describe():void | method public Media():void
DIFFERS  Member
  expected: interface public  | field public static final name:String | field public static final active:boolean | field public static final borrowed:ArrayList<Media> | method public register(card:LibraryCard):void | method public totalWeight():double
  actual:   interface public  | field public static final name:String | field public static final active:boolean | field public static final borrowed:ArrayList<Media> | method public register(card:LibraryCard):void | method public totalWeight():double | method public Member():void
```

## What could not be kept

- imports::ClassifierImport at src/catalog/Media.java#0/@imports.0 - several migrated elements could be the same one and nobody chose (it could be [imports::ClassifierImport at src/catalog/Media.java#0/@imports.0])
- statements::ForEachLoop in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.11/@statements.1 - the counterpart metaclass has no feature that can hold it (members::InterfaceMethod has no containment feature accepting statements::ForEachLoop)
- statements::LocalVariableStatement in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.11/@statements.0 - the counterpart metaclass has no feature that can hold it (members::InterfaceMethod has no containment feature accepting statements::LocalVariableStatement)
- statements::Return in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.11/@statements.2 - the counterpart metaclass has no feature that can hold it (members::InterfaceMethod has no containment feature accepting statements::Return)
- types::NamespaceClassifierReference in Media at src/catalog/Media.java#0/@classifiers.0/@implements.0 - several features of the counterpart metaclass could hold it (classifiers::Interface could hold types::NamespaceClassifierReference in [extends, defaultExtends])

## Does the Java compile

Yes; `javac` reports nothing about `src/catalog`.

## What is here

`model/library.uml` and `src/catalog/*.java` as this run left them, and the rule registry the
VSUM carries afterwards. Left out: the standard library stubs JaMoPP derives under
`src/java`, and the VSUM's own bookkeeping under `vsum`, which only records identities and
the location it was written at.
