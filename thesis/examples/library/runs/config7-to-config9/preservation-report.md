# Migration preservation report

Policy: report (analysed only)
Left to deal with by hand: 29 (26 would be kept + 3 not kept + 0 open decisions)

## Would be kept (26)

Content no rule of the new specifications derives - hand-written above all. This run only recorded it; `--preserve user` is the run that re-attaches it.

- types::ClassifierReference in Book at src/catalog/Book.java#0/@classifiers.0/@defaultExtends.0
  into classifiers::Class 'Book' at src/catalog/Book.java#0/@classifiers.0 (defaultExtends)
- modifiers::Final in Isbn at src/catalog/Isbn.java#0/@classifiers.0/@annotationsAndModifiers.1
  into classifiers::Class 'Isbn' at src/catalog/Isbn.java#0/@classifiers.0 (annotationsAndModifiers)
- literals::NullLiteral in Book.isbn at src/catalog/Book.java#0/@classifiers.0/@members.0/@initialValue
  into members::Field 'isbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.1 (initialValue)
- modifiers::Public in Book.isbn at src/catalog/Book.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'isbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- modifiers::Static in Book.isbn at src/catalog/Book.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.1
  into members::Field 'isbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- modifiers::Final in Book.isbn at src/catalog/Book.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.2
  into members::Field 'isbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- literals::DecimalIntegerLiteral in Book.pageCount at src/catalog/Book.java#0/@classifiers.0/@members.1/@initialValue
  into members::Field 'pageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.4 (initialValue)
- modifiers::Public in Book.pageCount at src/catalog/Book.java#0/@classifiers.0/@members.1/@annotationsAndModifiers.0
  into members::Field 'pageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.4 (annotationsAndModifiers)
- modifiers::Static in Book.pageCount at src/catalog/Book.java#0/@classifiers.0/@members.1/@annotationsAndModifiers.1
  into members::Field 'pageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.4 (annotationsAndModifiers)
- modifiers::Final in Book.pageCount at src/catalog/Book.java#0/@classifiers.0/@members.1/@annotationsAndModifiers.2
  into members::Field 'pageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.4 (annotationsAndModifiers)
- modifiers::Public in Isbn.code at src/catalog/Isbn.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'code' in Isbn at src/catalog/Isbn.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- literals::NullLiteral in LibraryCard.cardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.0/@initialValue
  into members::Field 'cardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.1 (initialValue)
- modifiers::Public in LibraryCard.cardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'cardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- modifiers::Final in LibraryCard.cardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.2
  into members::Field 'cardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- literals::NullLiteral in Member.name at src/catalog/Member.java#0/@classifiers.0/@members.0/@initialValue
  into members::Field 'name' in Member at src/catalog/Member.java#0/@classifiers.0/@members.1 (initialValue)
- modifiers::Public in Member.name at src/catalog/Member.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'name' in Member at src/catalog/Member.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- modifiers::Static in Member.name at src/catalog/Member.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.1
  into members::Field 'name' in Member at src/catalog/Member.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- modifiers::Final in Member.name at src/catalog/Member.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.2
  into members::Field 'name' in Member at src/catalog/Member.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- literals::BooleanLiteral in Member.active at src/catalog/Member.java#0/@classifiers.0/@members.1/@initialValue
  into members::Field 'active' in Member at src/catalog/Member.java#0/@classifiers.0/@members.4 (initialValue)
- modifiers::Public in Member.active at src/catalog/Member.java#0/@classifiers.0/@members.1/@annotationsAndModifiers.0
  into members::Field 'active' in Member at src/catalog/Member.java#0/@classifiers.0/@members.4 (annotationsAndModifiers)
- modifiers::Static in Member.active at src/catalog/Member.java#0/@classifiers.0/@members.1/@annotationsAndModifiers.1
  into members::Field 'active' in Member at src/catalog/Member.java#0/@classifiers.0/@members.4 (annotationsAndModifiers)
- modifiers::Final in Member.active at src/catalog/Member.java#0/@classifiers.0/@members.1/@annotationsAndModifiers.2
  into members::Field 'active' in Member at src/catalog/Member.java#0/@classifiers.0/@members.4 (annotationsAndModifiers)
- literals::NullLiteral in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.2/@initialValue
  into members::Field 'borrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.7 (initialValue)
- modifiers::Public in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.2/@annotationsAndModifiers.0
  into members::Field 'borrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.7 (annotationsAndModifiers)
- modifiers::Static in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.2/@annotationsAndModifiers.1
  into members::Field 'borrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.7 (annotationsAndModifiers)
- modifiers::Final in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.2/@annotationsAndModifiers.2
  into members::Field 'borrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.7 (annotationsAndModifiers)

## Not kept (3)

Content that could not be placed in the migrated models; each item names the reason. Putting it back is manual work.

These were kept in a folder beside the one that was migrated. This example was generated in a scratch area that has since been deleted, so there is nothing to point at here; a real migration names that folder at this spot and leaves it in place.

- containers::CompilationUnit 'catalog.Borrowable.java' at src/catalog/Borrowable.java#0/
  the model file has no counterpart after the migration
- containers::CompilationUnit 'catalog.Media.java' at src/catalog/Media.java#0/
  the model file has no counterpart after the migration
- types::ClassifierReference in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.2/@typeReference/@classifierReferences.0/@typeArguments.0/@typeReference/@classifierReferences.0.target
  it references an element that no longer exists: the value classifiers::Interface 'Media' at src/catalog/Media.java#0/@classifiers.0 has no counterpart
