# Migration preservation report

Policy: report (analysed only)
Left to deal with by hand: 14 (9 would be kept + 5 not kept + 0 open decisions)

## Would be kept (9)

Content no rule of the new specifications derives - hand-written above all. This run only recorded it; `--preserve user` is the run that re-attaches it.

- members::InterfaceMethod 'values' in Book at src/catalog/Book.java#0/@classifiers.0/@defaultMembers.0
  into classifiers::Class 'Book' at src/catalog/Book.java#0/@classifiers.0 (defaultMembers)
- members::InterfaceMethod 'valueOf' in Book at src/catalog/Book.java#0/@classifiers.0/@defaultMembers.1
  into classifiers::Class 'Book' at src/catalog/Book.java#0/@classifiers.0 (defaultMembers)
- modifiers::Final in Isbn at src/catalog/Isbn.java#0/@classifiers.0/@annotationsAndModifiers.1
  into classifiers::Class 'Isbn' at src/catalog/Isbn.java#0/@classifiers.0 (annotationsAndModifiers)
- members::InterfaceMethod 'values' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@defaultMembers.0
  into classifiers::Class 'LibraryCard' at src/catalog/LibraryCard.java#0/@classifiers.0 (defaultMembers)
- members::InterfaceMethod 'valueOf' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@defaultMembers.1
  into classifiers::Class 'LibraryCard' at src/catalog/LibraryCard.java#0/@classifiers.0 (defaultMembers)
- members::InterfaceMethod 'values' in Member at src/catalog/Member.java#0/@classifiers.0/@defaultMembers.0
  into classifiers::Class 'Member' at src/catalog/Member.java#0/@classifiers.0 (defaultMembers)
- members::InterfaceMethod 'valueOf' in Member at src/catalog/Member.java#0/@classifiers.0/@defaultMembers.1
  into classifiers::Class 'Member' at src/catalog/Member.java#0/@classifiers.0 (defaultMembers)
- statements::LocalVariableStatement in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.0
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.10 (statements)
- statements::Return in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.2
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.10 (statements)

## Not kept (5)

Content that could not be placed in the migrated models; each item names the reason. Putting it back is manual work.

These were kept in a folder beside the one that was migrated. This example was generated in a scratch area that has since been deleted, so there is nothing to point at here; a real migration names that folder at this spot and leaves it in place.

- containers::CompilationUnit 'catalog.Media.java' at src/catalog/Media.java#0/
  the model file has no counterpart after the migration
- types::ClassifierReference in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.6/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Enumeration 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- types::ClassifierReference in Member.getBorrowed at src/catalog/Member.java#0/@classifiers.0/@members.7/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Enumeration 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- types::ClassifierReference in Member.setBorrowed.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.8/@parameters.0/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Enumeration 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- statements::ForEachLoop in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.1
  it references an element that no longer exists
