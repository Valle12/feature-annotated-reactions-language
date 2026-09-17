# Migration preservation report

Policy: report (analysed only)
Left to deal with by hand: 20 (16 would be kept + 3 not kept + 1 open decision)

## Would be kept (16)

Content no rule of the new specifications derives - hand-written above all. This run only recorded it; `--preserve user` is the run that re-attaches it.

- imports::ClassifierImport at src/catalog/Book.java#0/@imports.0
  into containers::CompilationUnit 'catalog.Book.java' at src/catalog/Book.java#0/ (imports)
- modifiers::Abstract in Book at src/catalog/Book.java#0/@classifiers.0/@annotationsAndModifiers.1
  into classifiers::Enumeration 'Book' at src/catalog/Book.java#0/@classifiers.0 (annotationsAndModifiers)
- types::NamespaceClassifierReference in Book at src/catalog/Book.java#0/@classifiers.0/@extends
  into classifiers::Enumeration 'Book' at src/catalog/Book.java#0/@classifiers.0 (implements)
- modifiers::Final in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@annotationsAndModifiers.1
  into classifiers::Enumeration 'LibraryCard' at src/catalog/LibraryCard.java#0/@classifiers.0 (annotationsAndModifiers)
- types::ClassifierReference in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@defaultExtends
  into classifiers::Enumeration 'LibraryCard' at src/catalog/LibraryCard.java#0/@classifiers.0 (implements)
- modifiers::Abstract in Media at src/catalog/Media.java#0/@classifiers.0/@annotationsAndModifiers.1
  into classifiers::Enumeration 'Media' at src/catalog/Media.java#0/@classifiers.0 (annotationsAndModifiers)
- types::NamespaceClassifierReference in Media at src/catalog/Media.java#0/@classifiers.0/@implements.0
  into classifiers::Enumeration 'Media' at src/catalog/Media.java#0/@classifiers.0 (implements)
- types::ClassifierReference in Media at src/catalog/Media.java#0/@classifiers.0/@defaultExtends
  into classifiers::Enumeration 'Media' at src/catalog/Media.java#0/@classifiers.0 (implements)
- types::ClassifierReference in Member at src/catalog/Member.java#0/@classifiers.0/@defaultExtends
  into classifiers::Enumeration 'Member' at src/catalog/Member.java#0/@classifiers.0 (implements)
- modifiers::Static in LibraryCard.getCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.1/@annotationsAndModifiers.1
  into members::ClassMethod 'getCardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- modifiers::Static in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@annotationsAndModifiers.1
  into members::ClassMethod 'setCardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2 (annotationsAndModifiers)
- statements::LocalVariableStatement in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.0
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.10 (statements)
- statements::ForEachLoop in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.1
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.10 (statements)
- statements::Return in Member.totalWeight at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.2
  into members::ClassMethod 'totalWeight' in Member at src/catalog/Member.java#0/@classifiers.0/@members.10 (statements)
- references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@child/@next
  into references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@value (next)
- references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@child.target
  into references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@value (target)

## Not kept (3)

Content that could not be placed in the migrated models; each item names the reason. Putting it back is manual work.

These were kept in a folder beside the one that was migrated. This example was generated in a scratch area that has since been deleted, so there is nothing to point at here; a real migration names that folder at this spot and leaves it in place.

- imports::ClassifierImport at src/catalog/Media.java#0/@imports.0
  several migrated elements could be the same one and nobody chose: it could be [imports::ClassifierImport at src/catalog/Media.java#0/@imports.0]
- references::IdentifierReference in LibraryCard.getCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.1/@statements.0/@returnValue
  the counterpart feature is single-valued and the new rules already set it: statements::Return.returnValue already holds references::SelfReference
- references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@value
  the counterpart feature is single-valued and the new rules already set it: expressions::AssignmentExpression.value already holds references::IdentifierReference

## Open decisions (1)

Choices this run could not make alone, so nothing was done about them; what they concern is work left over.

- Which migrated element continues imports::ClassifierImport at src/catalog/Media.java#0/@imports.0?
  nobody could decide: imports::ClassifierImport at src/catalog/Media.java#0/@imports.0

## Notes (3)

How existing content travelled through the migration - moves, values the new rules produce differently, containers restored only as carriers. Nothing here needs action, and none of it counts towards the number above.

- types::NamespaceClassifierReference in Book at src/catalog/Book.java#0/@classifiers.0/@extends
  restored only to carry hand-written content: the parts only the old rules derived were left out
- types::NamespaceClassifierReference in Media at src/catalog/Media.java#0/@classifiers.0/@implements.0
  restored only to carry hand-written content: the parts only the old rules derived were left out
- references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@child.target
  the hand-written value replaced the derived one: it replaced parameters::OrdinaryParameter 'cardNumber' in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@parameters.0
