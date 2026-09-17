# Migration preservation report

Policy: report (analysed only)
Left to deal with by hand: 12 (12 would be kept + 0 not kept + 0 open decisions)

## Would be kept (12)

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
- members::InterfaceMethod 'values' in Media at src/catalog/Media.java#0/@classifiers.0/@defaultMembers.0
  into classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 (defaultMembers)
- members::InterfaceMethod 'valueOf' in Media at src/catalog/Media.java#0/@classifiers.0/@defaultMembers.1
  into classifiers::Class 'Media' at src/catalog/Media.java#0/@classifiers.0 (defaultMembers)
- members::InterfaceMethod 'values' in Member at src/catalog/Member.java#0/@classifiers.0/@defaultMembers.0
  into classifiers::Class 'Member' at src/catalog/Member.java#0/@classifiers.0 (defaultMembers)
- members::InterfaceMethod 'valueOf' in Member at src/catalog/Member.java#0/@classifiers.0/@defaultMembers.1
  into classifiers::Class 'Member' at src/catalog/Member.java#0/@classifiers.0 (defaultMembers)
- statements::LocalVariableStatement in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.0
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.10 (statements)
- statements::ForEachLoop in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.1
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.10 (statements)
- statements::Return in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.2
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.10 (statements)

## Not kept (0)

