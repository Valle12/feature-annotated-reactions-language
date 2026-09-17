# Migration preservation report

Policy: report (analysed only)
Left to deal with by hand: 14 (4 would be kept + 10 not kept + 0 open decisions)

## Would be kept (4)

Content no rule of the new specifications derives - hand-written above all. This run only recorded it; `--preserve user` is the run that re-attaches it.

- modifiers::Static in LibraryCard.getCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.1/@annotationsAndModifiers.1
  into members::ClassMethod 'getCardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- modifiers::Static in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@annotationsAndModifiers.1
  into members::ClassMethod 'setCardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2 (annotationsAndModifiers)
- references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@child/@next
  into references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@value (next)
- references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@child.target
  into references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@value (target)

## Not kept (10)

Content that could not be placed in the migrated models; each item names the reason. Putting it back is manual work.

These were kept in a folder beside the one that was migrated. This example was generated in a scratch area that has since been deleted, so there is nothing to point at here; a real migration names that folder at this spot and leaves it in place.

- containers::CompilationUnit 'catalog.Media.java' at src/catalog/Media.java#0/
  the model file has no counterpart after the migration
- imports::ClassifierImport at src/catalog/Book.java#0/@imports.0.classifier
  it references an element that no longer exists: the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- types::ClassifierReference in Book at src/catalog/Book.java#0/@classifiers.0/@extends/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- types::ClassifierReference in Member.totalWeight.media at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.1/@next/@typeReference/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- types::ClassifierReference in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.6/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- types::ClassifierReference in Member.getBorrowed at src/catalog/Member.java#0/@classifiers.0/@members.7/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- types::ClassifierReference in Member.setBorrowed.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.8/@parameters.0/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- references::MethodCall in Member.totalWeight.Block at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.1/@statement/@statements.0/@expression/@value/@next.target
  it references an element that no longer exists: the value members::ClassMethod 'getWeight' in Media at src/catalog/Media.java#0/@classifiers.0/@members.10 has no counterpart
- references::IdentifierReference in LibraryCard.getCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.1/@statements.0/@returnValue
  the counterpart feature is single-valued and the new rules already set it: statements::Return.returnValue already holds references::SelfReference
- references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@value
  the counterpart feature is single-valued and the new rules already set it: expressions::AssignmentExpression.value already holds references::IdentifierReference

## Notes (1)

How existing content travelled through the migration - moves, values the new rules produce differently, containers restored only as carriers. Nothing here needs action, and none of it counts towards the number above.

- references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@child.target
  the hand-written value replaced the derived one: it replaced parameters::OrdinaryParameter 'cardNumber' in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@parameters.0
