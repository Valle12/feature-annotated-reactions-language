# Migration preservation report

Policy: report (analysed only)
Left to deal with by hand: 16 (8 would be kept + 8 not kept + 0 open decisions)

## Would be kept (8)

Content no rule of the new specifications derives - hand-written above all. This run only recorded it; `--preserve user` is the run that re-attaches it.

- modifiers::Public in Book.pageCount at src/catalog/Book.java#0/@classifiers.0/@members.3/@annotationsAndModifiers.0
  into members::Field 'pageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.4 (annotationsAndModifiers)
- modifiers::Public in Isbn.code at src/catalog/Isbn.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'code' in Isbn at src/catalog/Isbn.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- modifiers::Public in LibraryCard.cardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'cardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- modifiers::Public in Member.name at src/catalog/Member.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'name' in Member at src/catalog/Member.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- modifiers::Public in Member.active at src/catalog/Member.java#0/@classifiers.0/@members.3/@annotationsAndModifiers.0
  into members::Field 'active' in Member at src/catalog/Member.java#0/@classifiers.0/@members.4 (annotationsAndModifiers)
- modifiers::Public in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.6/@annotationsAndModifiers.0
  into members::Field 'borrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.7 (annotationsAndModifiers)
- statements::LocalVariableStatement in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.0
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.11 (statements)
- statements::Return in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.2
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.11 (statements)

## Not kept (8)

Content that could not be placed in the migrated models; each item names the reason. Putting it back is manual work.

These were kept in a folder beside the one that was migrated. This example was generated in a scratch area that has since been deleted, so there is nothing to point at here; a real migration names that folder at this spot and leaves it in place.

- containers::CompilationUnit 'catalog.Borrowable.java' at src/catalog/Borrowable.java#0/
  the model file has no counterpart after the migration
- containers::CompilationUnit 'catalog.Media.java' at src/catalog/Media.java#0/
  the model file has no counterpart after the migration
- imports::ClassifierImport at src/catalog/Book.java#0/@imports.0.classifier
  it references an element that no longer exists: the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- types::ClassifierReference in Book at src/catalog/Book.java#0/@classifiers.0/@extends/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- types::ClassifierReference in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.6/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- types::ClassifierReference in Member.getBorrowed at src/catalog/Member.java#0/@classifiers.0/@members.7/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- types::ClassifierReference in Member.setBorrowed.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.8/@parameters.0/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- statements::ForEachLoop in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.1
  it references an element that no longer exists
