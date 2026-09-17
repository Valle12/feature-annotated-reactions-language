# Migration preservation report

Policy: report (analysed only)
Left to deal with by hand: 35 (35 would be kept + 0 not kept + 0 open decisions)

## Would be kept (35)

Content no rule of the new specifications derives - hand-written above all. This run only recorded it; `--preserve user` is the run that re-attaches it.

- types::ClassifierReference in Book at src/catalog/Book.java#0/@classifiers.0/@defaultExtends.0
  into classifiers::Enumeration 'Book' at src/catalog/Book.java#0/@classifiers.0 (implements)
- types::ClassifierReference in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@defaultExtends.0
  into classifiers::Enumeration 'LibraryCard' at src/catalog/LibraryCard.java#0/@classifiers.0 (implements)
- types::ClassifierReference in Media at src/catalog/Media.java#0/@classifiers.0/@defaultExtends.0
  into classifiers::Enumeration 'Media' at src/catalog/Media.java#0/@classifiers.0 (implements)
- types::ClassifierReference in Member at src/catalog/Member.java#0/@classifiers.0/@defaultExtends.0
  into classifiers::Enumeration 'Member' at src/catalog/Member.java#0/@classifiers.0 (implements)
- literals::NullLiteral in Book.isbn at src/catalog/Book.java#0/@classifiers.0/@members.0/@initialValue
  into members::Field 'isbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.0 (initialValue)
- modifiers::Public in Book.isbn at src/catalog/Book.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'isbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- modifiers::Static in Book.isbn at src/catalog/Book.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.1
  into members::Field 'isbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- modifiers::Final in Book.isbn at src/catalog/Book.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.2
  into members::Field 'isbn' in Book at src/catalog/Book.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- literals::DecimalIntegerLiteral in Book.pageCount at src/catalog/Book.java#0/@classifiers.0/@members.1/@initialValue
  into members::Field 'pageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.3 (initialValue)
- modifiers::Static in Book.pageCount at src/catalog/Book.java#0/@classifiers.0/@members.1/@annotationsAndModifiers.1
  into members::Field 'pageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.3 (annotationsAndModifiers)
- modifiers::Final in Book.pageCount at src/catalog/Book.java#0/@classifiers.0/@members.1/@annotationsAndModifiers.2
  into members::Field 'pageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.3 (annotationsAndModifiers)
- literals::NullLiteral in LibraryCard.cardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.0/@initialValue
  into members::Field 'cardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.0 (initialValue)
- modifiers::Final in LibraryCard.cardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.2
  into members::Field 'cardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- literals::NullLiteral in Media.title at src/catalog/Media.java#0/@classifiers.0/@members.0/@initialValue
  into members::Field 'title' in Media at src/catalog/Media.java#0/@classifiers.0/@members.0 (initialValue)
- modifiers::Static in Media.title at src/catalog/Media.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.1
  into members::Field 'title' in Media at src/catalog/Media.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- modifiers::Final in Media.title at src/catalog/Media.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.2
  into members::Field 'title' in Media at src/catalog/Media.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- literals::DecimalIntegerLiteral in Media.mediaId at src/catalog/Media.java#0/@classifiers.0/@members.1/@initialValue
  into members::Field 'mediaId' in Media at src/catalog/Media.java#0/@classifiers.0/@members.3 (initialValue)
- modifiers::Public in Media.mediaId at src/catalog/Media.java#0/@classifiers.0/@members.1/@annotationsAndModifiers.0
  into members::Field 'mediaId' in Media at src/catalog/Media.java#0/@classifiers.0/@members.3 (annotationsAndModifiers)
- modifiers::Static in Media.mediaId at src/catalog/Media.java#0/@classifiers.0/@members.1/@annotationsAndModifiers.1
  into members::Field 'mediaId' in Media at src/catalog/Media.java#0/@classifiers.0/@members.3 (annotationsAndModifiers)
- modifiers::Final in Media.mediaId at src/catalog/Media.java#0/@classifiers.0/@members.1/@annotationsAndModifiers.2
  into members::Field 'mediaId' in Media at src/catalog/Media.java#0/@classifiers.0/@members.3 (annotationsAndModifiers)
- literals::NullLiteral in Media.type at src/catalog/Media.java#0/@classifiers.0/@members.2/@initialValue
  into members::Field 'type' in Media at src/catalog/Media.java#0/@classifiers.0/@members.6 (initialValue)
- modifiers::Static in Media.type at src/catalog/Media.java#0/@classifiers.0/@members.2/@annotationsAndModifiers.1
  into members::Field 'type' in Media at src/catalog/Media.java#0/@classifiers.0/@members.6 (annotationsAndModifiers)
- modifiers::Final in Media.type at src/catalog/Media.java#0/@classifiers.0/@members.2/@annotationsAndModifiers.2
  into members::Field 'type' in Media at src/catalog/Media.java#0/@classifiers.0/@members.6 (annotationsAndModifiers)
- literals::DecimalDoubleLiteral in Media.weight at src/catalog/Media.java#0/@classifiers.0/@members.3/@initialValue
  into members::Field 'weight' in Media at src/catalog/Media.java#0/@classifiers.0/@members.9 (initialValue)
- modifiers::Static in Media.weight at src/catalog/Media.java#0/@classifiers.0/@members.3/@annotationsAndModifiers.1
  into members::Field 'weight' in Media at src/catalog/Media.java#0/@classifiers.0/@members.9 (annotationsAndModifiers)
- modifiers::Final in Media.weight at src/catalog/Media.java#0/@classifiers.0/@members.3/@annotationsAndModifiers.2
  into members::Field 'weight' in Media at src/catalog/Media.java#0/@classifiers.0/@members.9 (annotationsAndModifiers)
- literals::NullLiteral in Member.name at src/catalog/Member.java#0/@classifiers.0/@members.0/@initialValue
  into members::Field 'name' in Member at src/catalog/Member.java#0/@classifiers.0/@members.0 (initialValue)
- modifiers::Static in Member.name at src/catalog/Member.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.1
  into members::Field 'name' in Member at src/catalog/Member.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- modifiers::Final in Member.name at src/catalog/Member.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.2
  into members::Field 'name' in Member at src/catalog/Member.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- literals::BooleanLiteral in Member.active at src/catalog/Member.java#0/@classifiers.0/@members.1/@initialValue
  into members::Field 'active' in Member at src/catalog/Member.java#0/@classifiers.0/@members.3 (initialValue)
- modifiers::Static in Member.active at src/catalog/Member.java#0/@classifiers.0/@members.1/@annotationsAndModifiers.1
  into members::Field 'active' in Member at src/catalog/Member.java#0/@classifiers.0/@members.3 (annotationsAndModifiers)
- modifiers::Final in Member.active at src/catalog/Member.java#0/@classifiers.0/@members.1/@annotationsAndModifiers.2
  into members::Field 'active' in Member at src/catalog/Member.java#0/@classifiers.0/@members.3 (annotationsAndModifiers)
- literals::NullLiteral in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.2/@initialValue
  into members::Field 'borrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.6 (initialValue)
- modifiers::Static in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.2/@annotationsAndModifiers.1
  into members::Field 'borrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.6 (annotationsAndModifiers)
- modifiers::Final in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.2/@annotationsAndModifiers.2
  into members::Field 'borrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.6 (annotationsAndModifiers)

## Not kept (0)

