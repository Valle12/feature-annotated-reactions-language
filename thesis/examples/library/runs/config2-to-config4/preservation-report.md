# Migration preservation report

Policy: report (analysed only)
Left to deal with by hand: 8 (0 would be kept + 8 not kept + 0 open decisions)

## Would be kept (0)


## Not kept (8)

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
