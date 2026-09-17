# config6 migrated to config7

| | |
|---|---|
| input | the config6 baseline, `baselines/config6` |
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
| dirty rules | 10 |
| affected elements | 6 |
| preservation policy | REPORT |
| elements that would be kept | 30 |
| elements that could not be kept | 5 |
| open decisions nobody answered | 2 |
| items left to deal with by hand | 37 |
| phases | rule-diff, load, roots, dominance, classify, left-out, view-open, selection, snapshot, preregister, delete-commit, reinsert-commit, view-close, preserve, refresh |

## What the rule diff and the trigger mechanism found

| | |
|---|---|
| rules in the persisted registry | 120 |
| rules in the new specifications | 116 |
| dirty rules | 10 (3 added, 7 removed) |
| dirty rules whose trigger matches a source element | 6 |
| source elements probed | 50 |
| elements in the models | 425 |
| matched elements | 6 |
| elements added as referrers | 0 |
| elements left out | 15 |

### Dirty rules

```
- javaToUmlAttribute::JavaAttributeMadeStaticRewriteCallSites  matches 0 source element(s)
- javaToUmlClassifier::JavaClassInserted  matches 0 source element(s)
+ javaToUmlClassifier::JavaClassInsertedAsInterface  matches 0 source element(s)
- javaToUmlMethod::JavaMethodMadeStaticRewriteCallSites  matches 0 source element(s)
- umlToJavaAttribute::UmlAttributeMadeStaticRewriteCallSites  matches 1 source element(s)
- umlToJavaClassifier::UmlClassInserted  matches 4 source element(s)
+ umlToJavaClassifier::UmlClassInsertedAsInterface  matches 4 source element(s)
- umlToJavaClassifier::UmlDataTypeInserted  matches 2 source element(s)
+ umlToJavaClassifier::UmlDataTypeInsertedAsRecord  matches 2 source element(s)
- umlToJavaMethod::UmlOperationMadeStaticRewriteCallSites  matches 1 source element(s)
```

### Affected elements

```
library.uml#/0/catalog/MediaType  uml::Enumeration  matched by umlToJavaClassifier::UmlDataTypeInserted, umlToJavaClassifier::UmlDataTypeInsertedAsRecord
library.uml#/0/catalog/Isbn  uml::DataType  matched by umlToJavaClassifier::UmlDataTypeInserted, umlToJavaClassifier::UmlDataTypeInsertedAsRecord
library.uml#/0/catalog/Media  uml::Class  matched by umlToJavaClassifier::UmlClassInserted, umlToJavaClassifier::UmlClassInsertedAsInterface
library.uml#/0/catalog/Book  uml::Class  matched by umlToJavaClassifier::UmlClassInserted, umlToJavaClassifier::UmlClassInsertedAsInterface
library.uml#/0/catalog/LibraryCard  uml::Class  matched by umlToJavaClassifier::UmlClassInserted, umlToJavaClassifier::UmlClassInsertedAsInterface
library.uml#/0/catalog/Member  uml::Class  matched by umlToJavaClassifier::UmlClassInserted, umlToJavaClassifier::UmlClassInsertedAsInterface
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

The migrated models describe exactly what `baselines/config7` describes. Under `--preserve report` nothing is carried over into the models, so what is left is what the target rules derive - and that is what the baseline derives from the same UML.

## What could not be kept

- imports::ClassifierImport at src/catalog/Media.java#0/@imports.0 - several migrated elements could be the same one and nobody chose (it could be [imports::ClassifierImport at src/catalog/Media.java#0/@imports.0])
- statements::ForEachLoop in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.1 - the counterpart metaclass has no feature that can hold it (members::InterfaceMethod has no containment feature accepting statements::ForEachLoop)
- statements::LocalVariableStatement in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.0 - the counterpart metaclass has no feature that can hold it (members::InterfaceMethod has no containment feature accepting statements::LocalVariableStatement)
- statements::Return in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.2 - the counterpart metaclass has no feature that can hold it (members::InterfaceMethod has no containment feature accepting statements::Return)
- types::NamespaceClassifierReference in Media at src/catalog/Media.java#0/@classifiers.0/@implements.0 - several features of the counterpart metaclass could hold it (classifiers::Interface could hold types::NamespaceClassifierReference in [extends, defaultExtends])

## Does the Java compile

Yes; `javac` reports nothing about `src/catalog`.

## What is here

`model/library.uml` and `src/catalog/*.java` as this run left them, and the rule registry the
VSUM carries afterwards. Left out: the standard library stubs JaMoPP derives under
`src/java`, and the VSUM's own bookkeeping under `vsum`, which only records identities and
the location it was written at.
