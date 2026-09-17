# Migration preservation report

Policy: report (analysed only)
Left to deal with by hand: 3 (0 would be kept + 3 not kept + 0 open decisions)

## Would be kept (0)


## Not kept (3)

Content that could not be placed in the migrated models; each item names the reason. Putting it back is manual work.

These were kept in a folder beside the one that was migrated. This example was generated in a scratch area that has since been deleted, so there is nothing to point at here; a real migration names that folder at this spot and leaves it in place.

- containers::CompilationUnit 'catalog.Borrowable.java' at src/catalog/Borrowable.java#0/
  the model file has no counterpart after the migration
- imports::ClassifierImport at src/catalog/MediaImpl.java#0/@imports.0.classifier
  it references an element that no longer exists: the value classifiers::Interface 'Borrowable' at src/catalog/Borrowable.java#0/@classifiers.0 has no counterpart
- types::ClassifierReference in MediaImpl at src/catalog/MediaImpl.java#0/@classifiers.0/@implements.0/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Interface 'Borrowable' at src/catalog/Borrowable.java#0/@classifiers.0 has no counterpart

## Notes (1)

How existing content travelled through the migration - moves, values the new rules produce differently, containers restored only as carriers. Nothing here needs action, and none of it counts towards the number above.

- references::MethodCall in Member.totalWeight.Block at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.1/@statement/@statements.0/@expression/@value/@next.target
  the new rules produce a different value: pathmap:/javaclass/catalog.MediaImpl.java#//@classifiers.0/@members.10 is now src/catalog/MediaImpl.java#//@classifiers.0/@members.10
