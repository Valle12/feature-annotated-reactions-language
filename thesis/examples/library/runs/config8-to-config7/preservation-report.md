# Migration preservation report

Policy: report (analysed only)
Left to deal with by hand: 35 (32 would be kept + 3 not kept + 0 open decisions)

## Would be kept (32)

Content no rule of the new specifications derives - hand-written above all. This run only recorded it; `--preserve user` is the run that re-attaches it.

- members::ClassMethod 'getIsbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.1
  into classifiers::Interface 'Book' at src/catalog/Book.java#0/@classifiers.0 (members)
- members::ClassMethod 'setIsbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.2
  into classifiers::Interface 'Book' at src/catalog/Book.java#0/@classifiers.0 (members)
- members::ClassMethod 'getPageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.4
  into classifiers::Interface 'Book' at src/catalog/Book.java#0/@classifiers.0 (members)
- members::ClassMethod 'setPageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.5
  into classifiers::Interface 'Book' at src/catalog/Book.java#0/@classifiers.0 (members)
- members::InterfaceMethod 'values' in Book at src/catalog/Book.java#0/@classifiers.0/@defaultMembers.0
  into classifiers::Interface 'Book' at src/catalog/Book.java#0/@classifiers.0 (defaultMembers)
- members::InterfaceMethod 'valueOf' in Book at src/catalog/Book.java#0/@classifiers.0/@defaultMembers.1
  into classifiers::Interface 'Book' at src/catalog/Book.java#0/@classifiers.0 (defaultMembers)
- members::ClassMethod 'getCardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.1
  into classifiers::Interface 'LibraryCard' at src/catalog/LibraryCard.java#0/@classifiers.0 (members)
- members::ClassMethod 'setCardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2
  into classifiers::Interface 'LibraryCard' at src/catalog/LibraryCard.java#0/@classifiers.0 (members)
- members::InterfaceMethod 'values' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@defaultMembers.0
  into classifiers::Interface 'LibraryCard' at src/catalog/LibraryCard.java#0/@classifiers.0 (defaultMembers)
- members::InterfaceMethod 'valueOf' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@defaultMembers.1
  into classifiers::Interface 'LibraryCard' at src/catalog/LibraryCard.java#0/@classifiers.0 (defaultMembers)
- members::ClassMethod 'getTitle' in Media at src/catalog/Media.java#0/@classifiers.0/@members.1
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (members)
- members::ClassMethod 'setTitle' in Media at src/catalog/Media.java#0/@classifiers.0/@members.2
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (members)
- members::ClassMethod 'getMediaId' in Media at src/catalog/Media.java#0/@classifiers.0/@members.4
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (members)
- members::ClassMethod 'setMediaId' in Media at src/catalog/Media.java#0/@classifiers.0/@members.5
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (members)
- members::ClassMethod 'getType' in Media at src/catalog/Media.java#0/@classifiers.0/@members.7
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (members)
- members::ClassMethod 'setType' in Media at src/catalog/Media.java#0/@classifiers.0/@members.8
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (members)
- members::ClassMethod 'getWeight' in Media at src/catalog/Media.java#0/@classifiers.0/@members.10
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (members)
- members::ClassMethod 'setWeight' in Media at src/catalog/Media.java#0/@classifiers.0/@members.11
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (members)
- members::InterfaceMethod 'values' in Media at src/catalog/Media.java#0/@classifiers.0/@defaultMembers.0
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (defaultMembers)
- members::InterfaceMethod 'valueOf' in Media at src/catalog/Media.java#0/@classifiers.0/@defaultMembers.1
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (defaultMembers)
- members::ClassMethod 'getName' in Member at src/catalog/Member.java#0/@classifiers.0/@members.1
  into classifiers::Interface 'Member' at src/catalog/Member.java#0/@classifiers.0 (members)
- members::ClassMethod 'setName' in Member at src/catalog/Member.java#0/@classifiers.0/@members.2
  into classifiers::Interface 'Member' at src/catalog/Member.java#0/@classifiers.0 (members)
- members::ClassMethod 'getActive' in Member at src/catalog/Member.java#0/@classifiers.0/@members.4
  into classifiers::Interface 'Member' at src/catalog/Member.java#0/@classifiers.0 (members)
- members::ClassMethod 'setActive' in Member at src/catalog/Member.java#0/@classifiers.0/@members.5
  into classifiers::Interface 'Member' at src/catalog/Member.java#0/@classifiers.0 (members)
- members::ClassMethod 'getBorrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.7
  into classifiers::Interface 'Member' at src/catalog/Member.java#0/@classifiers.0 (members)
- members::ClassMethod 'setBorrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.8
  into classifiers::Interface 'Member' at src/catalog/Member.java#0/@classifiers.0 (members)
- members::InterfaceMethod 'values' in Member at src/catalog/Member.java#0/@classifiers.0/@defaultMembers.0
  into classifiers::Interface 'Member' at src/catalog/Member.java#0/@classifiers.0 (defaultMembers)
- members::InterfaceMethod 'valueOf' in Member at src/catalog/Member.java#0/@classifiers.0/@defaultMembers.1
  into classifiers::Interface 'Member' at src/catalog/Member.java#0/@classifiers.0 (defaultMembers)
- modifiers::Private in Book.isbn at src/catalog/Book.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'isbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- modifiers::Final in Book.describe at src/catalog/Book.java#0/@classifiers.0/@members.6/@annotationsAndModifiers.1
  into members::InterfaceMethod 'describe' in Book at src/catalog/Book.java#0/@classifiers.0/@members.2 (annotationsAndModifiers)
- modifiers::Protected in Media.mediaId at src/catalog/Media.java#0/@classifiers.0/@members.3/@annotationsAndModifiers.0
  into members::Field 'mediaId' in Media at src/catalog/Media.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- modifiers::Static in Member.register at src/catalog/Member.java#0/@classifiers.0/@members.9/@annotationsAndModifiers.1
  into members::InterfaceMethod 'register' in Member at src/catalog/Member.java#0/@classifiers.0/@members.3 (annotationsAndModifiers)

## Not kept (3)

Content that could not be placed in the migrated models; each item names the reason. Putting it back is manual work.

These were kept in a folder beside the one that was migrated. This example was generated in a scratch area that has since been deleted, so there is nothing to point at here; a real migration names that folder at this spot and leaves it in place.

- statements::LocalVariableStatement in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.0
  the counterpart metaclass has no feature that can hold it: members::InterfaceMethod has no containment feature accepting statements::LocalVariableStatement
- statements::ForEachLoop in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.1
  the counterpart metaclass has no feature that can hold it: members::InterfaceMethod has no containment feature accepting statements::ForEachLoop
- statements::Return in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.2
  the counterpart metaclass has no feature that can hold it: members::InterfaceMethod has no containment feature accepting statements::Return

## Notes (20)

How existing content travelled through the migration - moves, values the new rules produce differently, containers restored only as carriers. Nothing here needs action, and none of it counts towards the number above.

- members::ClassMethod 'getIsbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.1
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setIsbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.2
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getPageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.4
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setPageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.5
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getCardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.1
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setCardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getTitle' in Media at src/catalog/Media.java#0/@classifiers.0/@members.1
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setTitle' in Media at src/catalog/Media.java#0/@classifiers.0/@members.2
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getMediaId' in Media at src/catalog/Media.java#0/@classifiers.0/@members.4
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setMediaId' in Media at src/catalog/Media.java#0/@classifiers.0/@members.5
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getType' in Media at src/catalog/Media.java#0/@classifiers.0/@members.7
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setType' in Media at src/catalog/Media.java#0/@classifiers.0/@members.8
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getWeight' in Media at src/catalog/Media.java#0/@classifiers.0/@members.10
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setWeight' in Media at src/catalog/Media.java#0/@classifiers.0/@members.11
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getName' in Member at src/catalog/Member.java#0/@classifiers.0/@members.1
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setName' in Member at src/catalog/Member.java#0/@classifiers.0/@members.2
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getActive' in Member at src/catalog/Member.java#0/@classifiers.0/@members.4
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setActive' in Member at src/catalog/Member.java#0/@classifiers.0/@members.5
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getBorrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.7
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setBorrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.8
  restored only to carry hand-written content: the parts only the old rules derived were left out
