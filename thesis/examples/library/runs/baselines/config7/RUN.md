# The config7 baseline

The library example as this configuration's rules derive it into an empty VSUM, with no
migration involved. Every cell in the row `config7-to-*` starts from this state, and every
cell in the column `*-to-config7` is read against it: a migration that ends where this
does has re-derived everything the target rules would have produced anyway.

Rules: `umljava-config7.jar`, built from `../rules/config7-reactions`.

The other baselines carry one thing the rules do not derive - the body of
`Member.totalWeight` - and this one cannot. This configuration realizes the classifiers
holding it as Java interfaces, an interface method carries no body, and the Java metamodel
here predates `default`, so there is nowhere to write the statements. A row starting here
therefore has no hand-written content for the preservation pass to report on. That is a
property of the configuration, not of the migration.

## Does the Java compile

Yes; `javac` reports nothing about `src/catalog`.

## What is here

`model/library.uml` and `src/catalog/*.java` as this run left them, and the rule registry the
VSUM carries afterwards. Left out: the standard library stubs JaMoPP derives under
`src/java`, and the VSUM's own bookkeeping under `vsum`, which only records identities and
the location it was written at.
