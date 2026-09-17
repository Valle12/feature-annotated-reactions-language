# Migration preservation report

Policy: report (analysed only)
Left to deal with by hand: 36 (29 would be kept + 5 not kept + 2 open decisions)

## Would be kept (29)

Content no rule of the new specifications derives - hand-written above all. This run only recorded it; `--preserve user` is the run that re-attaches it.

- imports::ClassifierImport at src/catalog/Book.java#0/@imports.0
  into containers::CompilationUnit 'catalog.Book.java' at src/catalog/Book.java#0/ (imports)
- members::ClassMethod 'getIsbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.2
  into classifiers::Interface 'Book' at src/catalog/Book.java#0/@classifiers.0 (members)
- members::ClassMethod 'setIsbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.3
  into classifiers::Interface 'Book' at src/catalog/Book.java#0/@classifiers.0 (members)
- members::ClassMethod 'getPageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.5
  into classifiers::Interface 'Book' at src/catalog/Book.java#0/@classifiers.0 (members)
- members::ClassMethod 'setPageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.6
  into classifiers::Interface 'Book' at src/catalog/Book.java#0/@classifiers.0 (members)
- modifiers::Abstract in Book at src/catalog/Book.java#0/@classifiers.0/@annotationsAndModifiers.1
  into classifiers::Interface 'Book' at src/catalog/Book.java#0/@classifiers.0 (annotationsAndModifiers)
- types::NamespaceClassifierReference in Book at src/catalog/Book.java#0/@classifiers.0/@extends
  into classifiers::Interface 'Book' at src/catalog/Book.java#0/@classifiers.0 (extends)
- members::ClassMethod 'getCardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2
  into classifiers::Interface 'LibraryCard' at src/catalog/LibraryCard.java#0/@classifiers.0 (members)
- members::ClassMethod 'setCardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.3
  into classifiers::Interface 'LibraryCard' at src/catalog/LibraryCard.java#0/@classifiers.0 (members)
- modifiers::Final in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@annotationsAndModifiers.1
  into classifiers::Interface 'LibraryCard' at src/catalog/LibraryCard.java#0/@classifiers.0 (annotationsAndModifiers)
- members::ClassMethod 'getTitle' in Media at src/catalog/Media.java#0/@classifiers.0/@members.2
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (members)
- members::ClassMethod 'setTitle' in Media at src/catalog/Media.java#0/@classifiers.0/@members.3
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (members)
- members::ClassMethod 'getMediaId' in Media at src/catalog/Media.java#0/@classifiers.0/@members.5
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (members)
- members::ClassMethod 'setMediaId' in Media at src/catalog/Media.java#0/@classifiers.0/@members.6
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (members)
- members::ClassMethod 'getType' in Media at src/catalog/Media.java#0/@classifiers.0/@members.8
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (members)
- members::ClassMethod 'setType' in Media at src/catalog/Media.java#0/@classifiers.0/@members.9
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (members)
- members::ClassMethod 'getWeight' in Media at src/catalog/Media.java#0/@classifiers.0/@members.11
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (members)
- members::ClassMethod 'setWeight' in Media at src/catalog/Media.java#0/@classifiers.0/@members.12
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (members)
- modifiers::Abstract in Media at src/catalog/Media.java#0/@classifiers.0/@annotationsAndModifiers.1
  into classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 (annotationsAndModifiers)
- members::ClassMethod 'getName' in Member at src/catalog/Member.java#0/@classifiers.0/@members.2
  into classifiers::Interface 'Member' at src/catalog/Member.java#0/@classifiers.0 (members)
- members::ClassMethod 'setName' in Member at src/catalog/Member.java#0/@classifiers.0/@members.3
  into classifiers::Interface 'Member' at src/catalog/Member.java#0/@classifiers.0 (members)
- members::ClassMethod 'getActive' in Member at src/catalog/Member.java#0/@classifiers.0/@members.5
  into classifiers::Interface 'Member' at src/catalog/Member.java#0/@classifiers.0 (members)
- members::ClassMethod 'setActive' in Member at src/catalog/Member.java#0/@classifiers.0/@members.6
  into classifiers::Interface 'Member' at src/catalog/Member.java#0/@classifiers.0 (members)
- members::ClassMethod 'getBorrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.8
  into classifiers::Interface 'Member' at src/catalog/Member.java#0/@classifiers.0 (members)
- members::ClassMethod 'setBorrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.9
  into classifiers::Interface 'Member' at src/catalog/Member.java#0/@classifiers.0 (members)
- modifiers::Private in Book.isbn at src/catalog/Book.java#0/@classifiers.0/@members.1/@annotationsAndModifiers.0
  into members::Field 'isbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- modifiers::Final in Book.describe at src/catalog/Book.java#0/@classifiers.0/@members.7/@annotationsAndModifiers.1
  into members::InterfaceMethod 'describe' in Book at src/catalog/Book.java#0/@classifiers.0/@members.2 (annotationsAndModifiers)
- modifiers::Protected in Media.mediaId at src/catalog/Media.java#0/@classifiers.0/@members.4/@annotationsAndModifiers.0
  into members::Field 'mediaId' in Media at src/catalog/Media.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- modifiers::Static in Member.register at src/catalog/Member.java#0/@classifiers.0/@members.10/@annotationsAndModifiers.1
  into members::InterfaceMethod 'register' in Member at src/catalog/Member.java#0/@classifiers.0/@members.3 (annotationsAndModifiers)

## Not kept (5)

Content that could not be placed in the migrated models; each item names the reason. Putting it back is manual work.

These were kept in a folder beside the one that was migrated. This example was generated in a scratch area that has since been deleted, so there is nothing to point at here; a real migration names that folder at this spot and leaves it in place.

- imports::ClassifierImport at src/catalog/Media.java#0/@imports.0
  several migrated elements could be the same one and nobody chose: it could be [imports::ClassifierImport at src/catalog/Media.java#0/@imports.0]
- types::NamespaceClassifierReference in Media at src/catalog/Media.java#0/@classifiers.0/@implements.0
  several features of the counterpart metaclass could hold it: classifiers::Interface could hold types::NamespaceClassifierReference in [extends, defaultExtends]
- statements::LocalVariableStatement in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.11/@statements.0
  the counterpart metaclass has no feature that can hold it: members::InterfaceMethod has no containment feature accepting statements::LocalVariableStatement
- statements::ForEachLoop in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.11/@statements.1
  the counterpart metaclass has no feature that can hold it: members::InterfaceMethod has no containment feature accepting statements::ForEachLoop
- statements::Return in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.11/@statements.2
  the counterpart metaclass has no feature that can hold it: members::InterfaceMethod has no containment feature accepting statements::Return

## Open decisions (2)

Choices this run could not make alone, so nothing was done about them; what they concern is work left over.

- Which migrated element continues imports::ClassifierImport at src/catalog/Media.java#0/@imports.0?
  nobody could decide: imports::ClassifierImport at src/catalog/Media.java#0/@imports.0
- Which feature of classifiers::Interface should hold types::NamespaceClassifierReference in Media at src/catalog/Media.java#0/@classifiers.0/@implements.0?
  nobody could decide: extends : TypeReference, defaultExtends : TypeReference

## Notes (21)

How existing content travelled through the migration - moves, values the new rules produce differently, containers restored only as carriers. Nothing here needs action, and none of it counts towards the number above.

- members::ClassMethod 'getIsbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.2
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setIsbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.3
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getPageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.5
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setPageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.6
  restored only to carry hand-written content: the parts only the old rules derived were left out
- types::NamespaceClassifierReference in Book at src/catalog/Book.java#0/@classifiers.0/@extends
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getCardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setCardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.3
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getTitle' in Media at src/catalog/Media.java#0/@classifiers.0/@members.2
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setTitle' in Media at src/catalog/Media.java#0/@classifiers.0/@members.3
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getMediaId' in Media at src/catalog/Media.java#0/@classifiers.0/@members.5
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setMediaId' in Media at src/catalog/Media.java#0/@classifiers.0/@members.6
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getType' in Media at src/catalog/Media.java#0/@classifiers.0/@members.8
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setType' in Media at src/catalog/Media.java#0/@classifiers.0/@members.9
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getWeight' in Media at src/catalog/Media.java#0/@classifiers.0/@members.11
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setWeight' in Media at src/catalog/Media.java#0/@classifiers.0/@members.12
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getName' in Member at src/catalog/Member.java#0/@classifiers.0/@members.2
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setName' in Member at src/catalog/Member.java#0/@classifiers.0/@members.3
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getActive' in Member at src/catalog/Member.java#0/@classifiers.0/@members.5
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setActive' in Member at src/catalog/Member.java#0/@classifiers.0/@members.6
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'getBorrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.8
  restored only to carry hand-written content: the parts only the old rules derived were left out
- members::ClassMethod 'setBorrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.9
  restored only to carry hand-written content: the parts only the old rules derived were left out
