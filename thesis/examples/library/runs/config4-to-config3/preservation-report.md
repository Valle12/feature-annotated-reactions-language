# Migration preservation report

Policy: report (analysed only)
Left to deal with by hand: 10 (10 would be kept + 0 not kept + 0 open decisions)

## Would be kept (10)

Content no rule of the new specifications derives - hand-written above all. This run only recorded it; `--preserve user` is the run that re-attaches it.

- modifiers::Public in Book.pageCount at src/catalog/Book.java#0/@classifiers.0/@members.3/@annotationsAndModifiers.0
  into members::Field 'pageCount' in Book at src/catalog/Book.java#0/@classifiers.0/@members.4 (annotationsAndModifiers)
- modifiers::Public in Isbn.code at src/catalog/Isbn.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'code' in Isbn at src/catalog/Isbn.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- modifiers::Public in LibraryCard.cardNumber at src/catalog/LibraryCard.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'cardNumber' in LibraryCard at src/catalog/LibraryCard.java#0/@classifiers.0/@members.0 (annotationsAndModifiers)
- modifiers::Public in MediaImpl.title at src/catalog/MediaImpl.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'title' in MediaImpl at src/catalog/MediaImpl.java#0/@classifiers.0/@members.1 (annotationsAndModifiers)
- modifiers::Protected in MediaImpl.mediaId at src/catalog/MediaImpl.java#0/@classifiers.0/@members.3/@annotationsAndModifiers.0
  into members::Field 'mediaId' in MediaImpl at src/catalog/MediaImpl.java#0/@classifiers.0/@members.4 (annotationsAndModifiers)
- modifiers::Public in MediaImpl.type at src/catalog/MediaImpl.java#0/@classifiers.0/@members.6/@annotationsAndModifiers.0
  into members::Field 'type' in MediaImpl at src/catalog/MediaImpl.java#0/@classifiers.0/@members.7 (annotationsAndModifiers)
- modifiers::Public in MediaImpl.weight at src/catalog/MediaImpl.java#0/@classifiers.0/@members.9/@annotationsAndModifiers.0
  into members::Field 'weight' in MediaImpl at src/catalog/MediaImpl.java#0/@classifiers.0/@members.10 (annotationsAndModifiers)
- modifiers::Public in Member.name at src/catalog/Member.java#0/@classifiers.0/@members.0/@annotationsAndModifiers.0
  into members::Field 'name' in Member at src/catalog/Member.java#0/@classifiers.0/@members.2 (annotationsAndModifiers)
- modifiers::Public in Member.active at src/catalog/Member.java#0/@classifiers.0/@members.3/@annotationsAndModifiers.0
  into members::Field 'active' in Member at src/catalog/Member.java#0/@classifiers.0/@members.5 (annotationsAndModifiers)
- modifiers::Public in Member.borrowed at src/catalog/Member.java#0/@classifiers.0/@members.6/@annotationsAndModifiers.0
  into members::Field 'borrowed' in Member at src/catalog/Member.java#0/@classifiers.0/@members.8 (annotationsAndModifiers)

## Not kept (0)


## Notes (1)

How existing content travelled through the migration - moves, values the new rules produce differently, containers restored only as carriers. Nothing here needs action, and none of it counts towards the number above.

- references::MethodCall in Member.totalWeight.Block at src/catalog/Member.java#0/@classifiers.0/@members.10/@statements.1/@statement/@statements.0/@expression/@value/@next.target
  the new rules produce a different value: pathmap:/javaclass/catalog.MediaImpl.java#//@classifiers.0/@members.11 is now src/catalog/MediaImpl.java#//@classifiers.0/@members.11
