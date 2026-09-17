# Migration preservation report

Policy: report (analysed only)
Left to deal with by hand: 9 (2 would be kept + 7 not kept + 0 open decisions)

## Would be kept (2)

Content no rule of the new specifications derives - hand-written above all. This run only recorded it; `--preserve user` is the run that re-attaches it.

- statements::LocalVariableStatement in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.11/@statements.0
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.10 (statements)
- statements::Return in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.11/@statements.2
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.10 (statements)

## Not kept (7)

Content that could not be placed in the migrated models; each item names the reason. Putting it back is manual work.

These were kept in a folder beside the one that was migrated. This example was generated in a scratch area that has since been deleted, so there is nothing to point at here; a real migration names that folder at this spot and leaves it in place.

- containers::CompilationUnit 'catalog.Media.java' at src/catalog/Media.java#0/
  the model file has no counterpart after the migration
- imports::ClassifierImport at src/catalog/Book.java#0/@imports.0.classifier
  it references an element that no longer exists: the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- types::ClassifierReference in Book at src/catalog/Book.java#0/@classifiers.0/@extends/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- types::ClassifierReference in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.7/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- types::ClassifierReference in Member.getBorrowed at src/catalog/Member.java#0/@classifiers.0/@members.8/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- types::ClassifierReference in Member.setBorrowed.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.9/@parameters.0/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
- statements::ForEachLoop in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.11/@statements.1
  it references an element that no longer exists
