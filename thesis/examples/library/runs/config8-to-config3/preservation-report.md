# Migration preservation report

Policy: report (analysed only)
Left to deal with by hand: 22 (22 would be kept + 0 not kept + 0 open decisions)

## Would be kept (22)

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
- modifiers::Public in Book.pageCount at src/catalog/Book.java#0/@classifiers.0/@members.3/@annotationsAndModifiers.0
  into members::Field 'pageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.3 (annotationsAndModifiers)
- modifiers::Public in Isbn.code at src/catalog/Isbn.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'code' in Isbn at src/catalog/Isbn.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- modifiers::Public in LibraryCard.cardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'cardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- modifiers::Public in Media.title at src/catalog/Media.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'title' in Media at src/catalog/Media.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- modifiers::Protected in Media.mediaId at src/catalog/Media.java#0/@classifiers.0/@members.3/@annotationsAndModifiers.0
  into members::Field 'mediaId' in Media at src/catalog/Media.java#0/@classifiers.0/@members.3 (annotationsAndModifiers)
- modifiers::Public in Media.type at src/catalog/Media.java#0/@classifiers.0/@members.6/@annotationsAndModifiers.0
  into members::Field 'type' in Media at src/catalog/Media.java#0/@classifiers.0/@members.6 (annotationsAndModifiers)
- modifiers::Public in Media.weight at src/catalog/Media.java#0/@classifiers.0/@members.9/@annotationsAndModifiers.0
  into members::Field 'weight' in Media at src/catalog/Media.java#0/@classifiers.0/@members.9 (annotationsAndModifiers)
- modifiers::Public in Member.name at src/catalog/Member.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'name' in Member at src/catalog/Member.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- modifiers::Public in Member.active at src/catalog/Member.java#0/@classifiers.0/@members.3/@annotationsAndModifiers.0
  into members::Field 'active' in Member at src/catalog/Member.java#0/@classifiers.0/@members.3 (annotationsAndModifiers)
- modifiers::Public in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.6/@annotationsAndModifiers.0
  into members::Field 'borrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.6 (annotationsAndModifiers)
- statements::LocalVariableStatement in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.0
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.10 (statements)
- statements::ForEachLoop in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.1
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.10 (statements)
- statements::Return in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.2
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.10 (statements)

## Not kept (0)

