# The config1 baseline

The library example as this configuration's rules derive it into an empty VSUM, with no
migration involved. Every cell in the row `config1-to-*` starts from this state, and every
cell in the column `*-to-config1` is read against it: a migration that ends where this
does has re-derived everything the target rules would have produced anyway.

Rules: `umljava-config1.jar`, built from `../rules/config1-reactions`.

It carries one thing the rules do not derive: the body of `Member.totalWeight`, which sums
the weights of the media a member borrowed. The rules derive that method's signature from
the UML operation and nothing about what it computes. That body is what the preservation
pass has to account for, and what each cell's `preservation-report.md` is about.

## Does the Java compile

Yes; `javac` reports nothing about `src/catalog`.

## What is here

`model/library.uml` and `src/catalog/*.java` as this run left them, and the rule registry the
VSUM carries afterwards. Left out: the standard library stubs JaMoPP derives under
`src/java`, and the VSUM's own bookkeeping under `vsum`, which only records identities and
the location it was written at.
