# config6 migrated to config1

| | |
|---|---|
| input | the config6 baseline, `baselines/config6` |
| rules | `umljava-config1.jar` |
| dominance | explicit, uml |

Equivalent command:

```
migration --model <vsum> --propagations umljava-config1.jar \
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
| dirty rules | 4 |
| affected elements | 2 |
| preservation policy | REPORT |
| elements that would be kept | 4 |
| elements that could not be kept | 2 |
| open decisions nobody answered | 0 |
| items left to deal with by hand | 6 |
| phases | rule-diff, load, roots, dominance, classify, left-out, view-open, selection, snapshot, preregister, delete-commit, reinsert-commit, view-close, preserve, refresh |

## What the rule diff and the trigger mechanism found

| | |
|---|---|
| rules in the persisted registry | 120 |
| rules in the new specifications | 116 |
| dirty rules | 4 (0 added, 4 removed) |
| dirty rules whose trigger matches a source element | 2 |
| source elements probed | 50 |
| elements in the models | 425 |
| matched elements | 2 |
| elements added as referrers | 0 |
| elements left out | 15 |

### Dirty rules

```
- javaToUmlAttribute::JavaAttributeMadeStaticRewriteCallSites  matches 0 source element(s)
- javaToUmlMethod::JavaMethodMadeStaticRewriteCallSites  matches 0 source element(s)
- umlToJavaAttribute::UmlAttributeMadeStaticRewriteCallSites  matches 1 source element(s)
- umlToJavaMethod::UmlOperationMadeStaticRewriteCallSites  matches 1 source element(s)
```

### Affected elements

```
library.uml#/0/catalog/LibraryCard/cardNumber  uml::Property  matched by umlToJavaAttribute::UmlAttributeMadeStaticRewriteCallSites
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

## Against config1 from scratch

The migrated models and `baselines/config1` do not describe the same thing about 1 classifier(s), which is the number the matrix carries. Each line below names a classifier and how the two differ, per model, so a classifier wrong in both is listed twice here and counted once there; `expected` is the baseline.

### Java, 1 place

```
DIFFERS  Member
  expected: class public  | field public name:String | method public getName():String | method public setName(name:String):void | field public active:boolean | method public getActive():boolean | method public setActive(active:boolean):void | field public borrowed:ArrayList<Media> | method public getBorrowed():ArrayList<Media> | method public setBorrowed(borrowed:ArrayList<Media>):void | method public static register(card:LibraryCard):void | method public totalWeight():double
  actual:   class public  | field public name:String | method public getName():String | method public setName(name:String):void | field public active:boolean | method public getActive():boolean | method public setActive(active:boolean):void | field public borrowed:ArrayList<Media> | method public getBorrowed():ArrayList<Media> | method public setBorrowed(borrowed:ArrayList<Media>):void | method public totalWeight():double | method public final static register(card:LibraryCard):void
```

## What could not be kept

- references::IdentifierReference in LibraryCard.getCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.1/@statements.0/@returnValue - the counterpart feature is single-valued and the new rules already set it (statements::Return.returnValue already holds references::SelfReference)
- references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@value - the counterpart feature is single-valued and the new rules already set it (expressions::AssignmentExpression.value already holds references::IdentifierReference)

## Does the Java compile

Yes; `javac` reports nothing about `src/catalog`.

## What is here

`model/library.uml` and `src/catalog/*.java` as this run left them, and the rule registry the
VSUM carries afterwards. Left out: the standard library stubs JaMoPP derives under
`src/java`, and the VSUM's own bookkeeping under `vsum`, which only records identities and
the location it was written at.
