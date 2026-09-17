# Migration preservation report

Policy: report (analysed only)
Left to deal with by hand: 6 (3 would be kept + 3 not kept + 0 open decisions)

## Would be kept (3)

Content no rule of the new specifications derives - hand-written above all. This run only recorded it; `--preserve user` is the run that re-attaches it.

- statements::LocalVariableStatement in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.11/@statements.0
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.10 (statements)
- statements::ForEachLoop in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.11/@statements.1
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.10 (statements)
- statements::Return in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.11/@statements.2
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.10 (statements)

## Not kept (3)

Content that could not be placed in the migrated models; each item names the reason. Putting it back is manual work.

These were kept in a folder beside the one that was migrated. This example was generated in a scratch area that has since been deleted, so there is nothing to point at here; a real migration names that folder at this spot and leaves it in place.

- containers::CompilationUnit 'catalog.Borrowable.java' at src/catalog/Borrowable.java#0/
  the model file has no counterpart after the migration
- imports::ClassifierImport at src/catalog/Media.java#0/@imports.0.classifier
  it references an element that no longer exists: the value classifiers::Interface 'Borrowable' at src/catalog/Borrowable.java#0/@classifiers.0 has no counterpart
- types::ClassifierReference in Media at src/catalog/Media.java#0/@classifiers.0/@implements.0/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Interface 'Borrowable' at src/catalog/Borrowable.java#0/@classifiers.0 has no counterpart
