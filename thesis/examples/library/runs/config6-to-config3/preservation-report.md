# Migration preservation report

Policy: report (analysed only)
Left to deal with by hand: 16 (14 would be kept + 2 not kept + 0 open decisions)

## Would be kept (14)

Content no rule of the new specifications derives - hand-written above all. This run only recorded it; `--preserve user` is the run that re-attaches it.

- modifiers::Public in Book.pageCount at src/catalog/Book.java#0/@classifiers.0/@members.3/@annotationsAndModifiers.0
  into members::Field 'pageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.4 (annotationsAndModifiers)
- modifiers::Public in Isbn.code at src/catalog/Isbn.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'code' in Isbn at src/catalog/Isbn.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- modifiers::Public in LibraryCard.cardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'cardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- modifiers::Static in LibraryCard.getCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.1/@annotationsAndModifiers.1
  into members::ClassMethod 'getCardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- modifiers::Static in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@annotationsAndModifiers.1
  into members::ClassMethod 'setCardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2 (annotationsAndModifiers)
- modifiers::Public in Media.title at src/catalog/Media.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'title' in Media at src/catalog/Media.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- modifiers::Protected in Media.mediaId at src/catalog/Media.java#0/@classifiers.0/@members.3/@annotationsAndModifiers.0
  into members::Field 'mediaId' in Media at src/catalog/Media.java#0/@classifiers.0/@members.4 (annotationsAndModifiers)
- modifiers::Public in Media.type at src/catalog/Media.java#0/@classifiers.0/@members.6/@annotationsAndModifiers.0
  into members::Field 'type' in Media at src/catalog/Media.java#0/@classifiers.0/@members.7 (annotationsAndModifiers)
- modifiers::Public in Media.weight at src/catalog/Media.java#0/@classifiers.0/@members.9/@annotationsAndModifiers.0
  into members::Field 'weight' in Media at src/catalog/Media.java#0/@classifiers.0/@members.10 (annotationsAndModifiers)
- modifiers::Public in Member.name at src/catalog/Member.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'name' in Member at src/catalog/Member.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- modifiers::Public in Member.active at src/catalog/Member.java#0/@classifiers.0/@members.3/@annotationsAndModifiers.0
  into members::Field 'active' in Member at src/catalog/Member.java#0/@classifiers.0/@members.4 (annotationsAndModifiers)
- modifiers::Public in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.6/@annotationsAndModifiers.0
  into members::Field 'borrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.7 (annotationsAndModifiers)
- references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@child/@next
  into references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@value (next)
- references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@child.target
  into references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@value (target)

## Not kept (2)

Content that could not be placed in the migrated models; each item names the reason. Putting it back is manual work.

These were kept in a folder beside the one that was migrated. This example was generated in a scratch area that has since been deleted, so there is nothing to point at here; a real migration names that folder at this spot and leaves it in place.

- references::IdentifierReference in LibraryCard.getCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.1/@statements.0/@returnValue
  the counterpart feature is single-valued and the new rules already set it: statements::Return.returnValue already holds references::SelfReference
- references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@value
  the counterpart feature is single-valued and the new rules already set it: expressions::AssignmentExpression.value already holds references::IdentifierReference

## Notes (2)

How existing content travelled through the migration - moves, values the new rules produce differently, containers restored only as carriers. Nothing here needs action, and none of it counts towards the number above.

- references::MethodCall in Member.totalWeight.Block at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.1/@statement/@statements.0/@expression/@value/@next.target
  the new rules produce a different value: pathmap:/javaclass/catalog.Media.java#//@classifiers.0/@members.11 is now src/catalog/Media.java#//@classifiers.0/@members.11
- references::IdentifierReference in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@statements.0/@expression/@child.target
  the hand-written value replaced the derived one: it replaced parameters::OrdinaryParameter 'cardNumber' in LibraryCard.setCardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.2/@parameters.0
