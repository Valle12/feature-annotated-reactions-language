# config1 migrated to config9

| | |
|---|---|
| input | the config1 baseline, `baselines/config1` |
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
| dirty rules | 24 |
| affected elements | 7 |
| preservation policy | REPORT |
| elements that would be kept | 9 |
| elements that could not be kept | 10 |
| open decisions nobody answered | 0 |
| items left to deal with by hand | 19 |
| phases | rule-diff, load, roots, dominance, classify, left-out, view-open, selection, snapshot, preregister, delete-commit, reinsert-commit, view-close, preserve, refresh |

## What the rule diff and the trigger mechanism found

| | |
|---|---|
| rules in the persisted registry | 116 |
| rules in the new specifications | 140 |
| dirty rules | 24 (24 added, 0 removed) |
| dirty rules whose trigger matches a source element | 9 |
| source elements probed | 50 |
| elements in the models | 424 |
| matched elements | 7 |
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
+ javaToUmlClassifier::JavaClassInsertedAddDefaultConstructor  matches 0 source element(s)
+ javaToUmlClassifier::JavaClassRenamedRenameConstructors  matches 0 source element(s)
+ javaToUmlClassifier::JavaInterfaceCreatedAddPrefix  matches 0 source element(s)
+ javaToUmlMethod::JavaMethodMadeStaticRewriteCallSites  matches 0 source element(s)
+ umlToJavaAttribute::UmlAttributeMadeStaticRewriteCallSites  matches 1 source element(s)
+ umlToJavaAttribute::UmlPropertyInsertedInClassEnforceAccessorGeneration  matches 10 source element(s)
+ umlToJavaAttribute::UmlPropertyInsertedInDataTypeEnforceAccessorGeneration  matches 1 source element(s)
+ umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor  matches 4 source element(s)
+ umlToJavaClassifier::UmlClassRenamedRenameConstructors  matches 4 source element(s)
+ umlToJavaClassifier::UmlInterfaceInsertedAddPrefix  matches 2 source element(s)
+ umlToJavaClassifier::UmlInterfaceRealizationCreatedAddSuffix  matches 1 source element(s)
+ umlToJavaClassifier::UmlInterfaceRealizationRemovedStripSuffix  matches 0 source element(s)
+ umlToJavaClassifier::UmlOperationInsertedReplaceAutoDefault  matches 4 source element(s)
+ umlToJavaMethod::UmlOperationMadeStaticRewriteCallSites  matches 1 source element(s)
```

### Affected elements

```
library.uml#/0/catalog/Identifiable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/Borrowable  uml::Interface  matched by umlToJavaClassifier::UmlInterfaceInsertedAddPrefix
library.uml#/0/catalog/Isbn/code  uml::Property  matched by umlToJavaAttribute::UmlPropertyInsertedInDataTypeEnforceAccessorGeneration
library.uml#/0/catalog/Media  uml::Class  matched by umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor, umlToJavaClassifier::UmlClassRenamedRenameConstructors
library.uml#/0/catalog/Book  uml::Class  matched by umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor, umlToJavaClassifier::UmlClassRenamedRenameConstructors
library.uml#/0/catalog/LibraryCard  uml::Class  matched by umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor, umlToJavaClassifier::UmlClassRenamedRenameConstructors
library.uml#/0/catalog/Member  uml::Class  matched by umlToJavaClassifier::UmlClassInsertedAddDefaultConstructor, umlToJavaClassifier::UmlClassRenamedRenameConstructors
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

The migrated models describe exactly what `baselines/config9` describes. Under `--preserve report` nothing is carried over into the models, so what is left is what the target rules derive - and that is what the baseline derives from the same UML.

## What could not be kept

- containers::CompilationUnit 'catalog.Borrowable.java' at src/catalog/Borrowable.java#0/ - the model file has no counterpart after the migration
- containers::CompilationUnit 'catalog.Media.java' at src/catalog/Media.java#0/ - the model file has no counterpart after the migration
- imports::ClassifierImport at src/catalog/Book.java#0/@imports.0.classifier - it references an element that no longer exists (the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart)
- references::SelfReference in LibraryCard.getCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.1/@statements.0/@returnValue - the counterpart feature is single-valued and the new rules already set it (statements::Return.returnValue already holds references::IdentifierReference)
- references::SelfReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@child - the counterpart feature is single-valued and the new rules already set it (expressions::AssignmentExpression.child already holds references::IdentifierReference)
- statements::ForEachLoop in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.1 - it references an element that no longer exists
- types::ClassifierReference in Book at src/catalog/Book.java#0/@classifiers.0/@extends/@classifierReferences.0.target - it references an element that no longer exists (the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart)
- types::ClassifierReference in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.6/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target - it references an element that no longer exists (the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart)
- types::ClassifierReference in Member.getBorrowed at src/catalog/Member.java#0/@classifiers.0/@members.7/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target - it references an element that no longer exists (the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart)
- types::ClassifierReference in Member.setBorrowed.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.8/@parameters.0/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target - it references an element that no longer exists (the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart)

## Does the Java compile

No, 1 error:

```
Member.java:34 missing return statement
```

## What is here

`model/library.uml` and `src/catalog/*.java` as this run left them, and the rule registry the
VSUM carries afterwards. Left out: the standard library stubs JaMoPP derives under
`src/java`, and the VSUM's own bookkeeping under `vsum`, which only records identities and
the location it was written at.
