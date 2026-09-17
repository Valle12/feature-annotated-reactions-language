#!/usr/bin/env bash
#
# classify-reaction-changes.sh -- Classify how every reaction and routine of the
# umljava ruleset changed while the feature annotations were introduced.
#
# Both revisions are taken from GitHub, so the result does not depend on any
# local clone: the annotated branch of the fork is compared against the commit
# where that branch forked off the original repository. Everything is fetched
# into a temporary blobless clone that is removed again afterwards, which means
# the script needs network access but no setup.
#
# Every "reaction <Name> { ... }" and "routine <name>(...) { ... }" block is
# extracted from both revisions and compared after dropping comments and
# normalising whitespace. Blocks are matched by file + kind + name. Annotation
# lines directly preceding a block belong to that block, which is what
# separates a pure annotation from a change to the rule itself.
#
# Every block falls into exactly one category:
#   unchanged                 annotation and body are the same as before
#   annotation only           existing block whose annotation changed
#   annotation and body       existing block whose annotation and body changed
#   body only                 existing block whose body changed
#   renamed                   the same rule under a new name (see below)
#   added with annotation     new block carrying an annotation
#   added without annotation  new block without annotation
# A block that exists only in the baseline and an added block of the same file
# and kind count as one renamed block when they can be paired unambiguously:
# reactions by an identical trigger line, routines by an identical body apart
# from the name. Whether a renamed block was annotated or changed as well is
# only visible in the details below the table.
#
# A second table splits the lines of code the head adds to the baseline, counted
# like count-loc.sh (non-blank lines that are not comment-only), into annotation
# lines, lines of added blocks, lines added and removed in changed and renamed
# blocks, and lines outside any block. A changed line counts as one removed and
# one added line. Every changed or renamed block is then listed under the cause
# of its change, taken from the commits of the fork that changed it; a block with
# two causes appears under both.
#
# Below the tables every block that is not unchanged is listed. Two checks
# verify that no block was swallowed by a brace mis-count and that every
# annotation line was attached to a block; a mismatch prints a warning and
# yields exit status 1, as does a changed block without a cause.
#
# Usage:
#   ./classify-reaction-changes.sh
#
set -euo pipefail

origin_url="https://github.com/vitruv-tools/Vitruv-CaseStudies.git"
fork_url="https://github.com/Valle12/Vitruv-CaseStudies.git"
branch="feature-annotations"
path="umljava/src/main/reactions"

name_of() { sed -e 's|.*github[.]com/||' -e 's|[.]git$||' <<< "$1"; }

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

clone="$tmp/repo"
parse_awk="$tmp/parse.awk"
classify_awk="$tmp/classify.awk"

# A blobless clone carries the history but downloads file contents only when
# they are asked for, which keeps the two checkouts below to a few seconds.
echo "Fetching $(name_of "$fork_url") and $(name_of "$origin_url") ..." >&2
git clone --filter=blob:none --no-checkout --single-branch --branch "$branch" \
    --quiet "$fork_url" "$clone"
git -C "$clone" remote add origin-repo "$origin_url"
git -C "$clone" fetch --filter=blob:none --no-tags --quiet origin-repo HEAD

head_rev=$(git -C "$clone" rev-parse "origin/$branch")
base=$(git -C "$clone" merge-base FETCH_HEAD "$head_rev")
base_label="$(git -C "$clone" rev-parse --short "$base") (fork point from $(name_of "$origin_url"))"
head_label="$(git -C "$clone" rev-parse --short "$head_rev") ($(name_of "$fork_url") $branch)"

# Splits one .reactions file into blocks and prints, per block, a tab separated
# record: file, kind, name, start line, annotations and body. Comments are
# dropped, so a reworded comment does not count as a change to the rule.
# The multi-line fields are joined with SOH so that one block stays one line.
cat > "$parse_awk" <<'AWK'
BEGIN { SEP = sprintf("%c", 1); BSLASH = sprintf("%c", 92) }

# Cuts off the line comment. With drop_strings set, string literals are removed
# as well, leaving only the structural braces.
function clean(s, drop_strings,   i, c, out, ins, prev) {
  out = ""; ins = 0; prev = ""
  for (i = 1; i <= length(s); i++) {
    c = substr(s, i, 1)
    if (ins) {
      if (!drop_strings) out = out c
      if (c == "\"" && prev != BSLASH) ins = 0
    }
    else if (c == "\"") { ins = 1; if (!drop_strings) out = out c }
    else if (c == "/" && substr(s, i + 1, 1) == "/") break
    else out = out c
    prev = c
  }
  return out
}

function norm(s) {
  gsub(/\r/, "", s)
  gsub(/^[ \t]+/, "", s); gsub(/[ \t]+$/, "", s); gsub(/[ \t]+/, " ", s)
  return s
}

function occurrences(s, ch,   i, n) {
  n = 0
  for (i = 1; i <= length(s); i++) if (substr(s, i, 1) == ch) n++
  return n
}

function append(acc, s) { return acc == "" ? s : acc SEP s }

!inblock {
  if (norm($0) ~ /^@/) { anno = append(anno, norm($0)); next }
  if (match($0, /^[ \t]*(reaction|routine)[ \t]+[A-Za-z0-9_]+/)) {
    split(norm(substr($0, RSTART, RLENGTH)), parts, " ")
    kind = parts[1]; name = parts[2]
    inblock = 1; start = FNR; body = ""; depth = 0; seen = 0
  } else { anno = ""; next }
}

inblock {
  nl = norm(clean($0, 0))
  if (nl != "") body = append(body, nl)
  s = clean($0, 1)
  depth += occurrences(s, "{") - occurrences(s, "}")
  if (index(s, "{") > 0) seen = 1
  if (seen && depth <= 0) {
    printf "%s\t%s\t%s\t%d\t%s\t%s\n", file, kind, name, start, anno, body
    inblock = 0; anno = ""
  }
}
AWK

# Compares the two record sets and prints the summary table, the checks and
# the list of changed blocks.
cat > "$classify_awk" <<'AWK'
BEGIN {
  FS = "\t"; SEP = sprintf("%c", 1)
  n = split("unchanged|annotation only|annotation and body|body only|renamed|added with annotation|added without annotation", order, "|")

  ncauses = split("Vitruvius upgrade|defect of the original rules|previously unsupported case|feature interaction", causes, "|")
  commits["Vitruvius upgrade"] = "4aebe5b30"
  commits["defect of the original rules"] = "d1f7fb65e, 67fc9a843"
  commits["previously unsupported case"] = "04594ef19, 67fc9a843"
  commits["feature interaction"] = "21112d9a9, 67fc9a843, 74a1f1651"
  # kind|file|name of every changed or renamed block (renamed ones under their new name) -> causes
  cause["routine|java2uml/JavaToUmlClassifier.reactions|addUmlElementToModelOrPackage"] = "Vitruvius upgrade"
  cause["routine|java2uml/JavaToUmlClassifier.reactions|createOrFindUmlClass"] = "Vitruvius upgrade"
  cause["routine|java2uml/JavaToUmlClassifier.reactions|createUmlPackage"] = "Vitruvius upgrade"
  cause["routine|java2uml/JavaToUmlTypePropagation.reactions|createExistingUmlClass"] = "Vitruvius upgrade"
  cause["routine|java2uml/JavaToUmlTypePropagation.reactions|createExistingUmlInterface"] = "Vitruvius upgrade"
  cause["routine|java2uml/JavaToUmlClassifier.reactions|createOrFindUmlEnum"] = "Vitruvius upgrade|feature interaction"
  cause["routine|java2uml/JavaToUmlClassifier.reactions|createOrFindUmlInterface"] = "Vitruvius upgrade|feature interaction"
  cause["routine|java2uml/JavaToUmlAttribute.reactions|createUmlAttributeInClass"] = "defect of the original rules"
  cause["routine|java2uml/JavaToUmlAttribute.reactions|createUmlAttributeInEnum"] = "defect of the original rules"
  cause["routine|uml2java/UmlToJavaClassifier.reactions|deleteJavaClassImplementsReference"] = "defect of the original rules"
  cause["reaction|java2uml/JavaToUmlAttribute.reactions|JavaAttributeCreatedInInterface"] = "previously unsupported case"
  cause["routine|uml2java/UmlToJavaAttribute.reactions|createOrFindJavaField"] = "previously unsupported case"
  cause["reaction|uml2java/UmlToJavaAttribute.reactions|UmlPropertyInsertedInInterface"] = "previously unsupported case"
  cause["reaction|java2uml/JavaToUmlMethod.reactions|JavaClassMethodCreatedInInterface"] = "previously unsupported case"
  cause["routine|java2uml/JavaToUmlAttribute.reactions|setUmlAttributeFinal"] = "feature interaction"
  cause["routine|java2uml/JavaToUmlMethod.reactions|changeUmlNamedElementVisibility"] = "feature interaction"
  cause["routine|java2uml/JavaToUmlMethod.reactions|setUmlFeatureStatic"] = "feature interaction"
  cause["routine|uml2java/UmlToJavaMethod.reactions|createOrFindJavaClassMethod"] = "feature interaction"
  cause["routine|uml2java/UmlToJavaMethod.reactions|createOrFindJavaConstructor"] = "feature interaction"
  cause["routine|uml2java/UmlToJavaClassifier.reactions|createJavaEnum"] = "feature interaction"
  cause["routine|uml2java/UmlToJavaClassifier.reactions|createJavaInterface"] = "feature interaction"
  cause["routine|uml2java/UmlToJavaClassifier.reactions|createOrFindJavaClass"] = "feature interaction"
  cause["routine|uml2java/UmlToJavaClassifier.reactions|createOrFindJavaInterface"] = "feature interaction"
}

function record(cat, kind) { count[cat]++; count[cat, kind]++ }

function lines(body,   p) { return body == "" ? 0 : split(body, p, SEP) }

# Lines of the new body without a counterpart in the old one, and the other way
# round, returned as "+added/-removed" and added to the running totals.
function linediff(old, new,   p, q, m, c, i, left, plus, minus, line) {
  m = split(old, p, SEP); c = split(new, q, SEP)
  for (i = 1; i <= m; i++) left[p[i]]++
  plus = 0; minus = 0
  for (i = 1; i <= c; i++) { if (left[q[i]] > 0) left[q[i]]--; else plus++ }
  for (line in left) minus += left[line]
  changed_plus += plus; changed_minus += minus
  return "+" plus "/-" minus
}

# Files a changed or renamed block under each of its causes.
function file_cause(kind, file, name, diff,   key, parts, m, i) {
  key = kind "|" short(file) "|" name
  used[key] = 1
  if (!(key in cause)) { uncaused = uncaused "\n  " kind " " short(file) " " name; return }
  m = split(cause[key], parts, "|")
  for (i = 1; i <= m; i++) {
    cn[parts[i]]++
    cl[parts[i], cn[parts[i]]] = sprintf("  %-8s  %-44s  %-36s  %s%s", kind, short(file), name, diff, m > 1 ? "  (two causes)" : "")
  }
}

# The last two path components are enough to tell the files apart.
function short(file,   p, m) { m = split(file, p, "/"); return m > 1 ? p[m - 1] "/" p[m] : file }

# The body with the name in the header line blanked out, so that the bodies
# of a renamed block can be compared.
function nameless(body,   p, m, i, out) {
  m = split(body, p, SEP)
  if (p[1] ~ /^reaction /) sub(/^reaction [A-Za-z0-9_]+/, "reaction _", p[1])
  else sub(/^routine [A-Za-z0-9_]+/, "routine _", p[1])
  out = p[1]
  for (i = 2; i <= m; i++) out = out SEP p[i]
  return out
}

# What identifies a block across a rename: the trigger line of a reaction,
# the nameless body of a routine.
function identity(kind, body,   p) {
  if (kind == "reaction") { split(body, p, SEP); return p[2] }
  return nameless(body)
}

function detail(cat, kind, file, name, rest,   f) {
  f = short(file); gsub(SEP, " ", rest)
  dn[cat]++; dl[cat, dn[cat]] = kind "\t" f "\t" name "\t" rest
  if (length(f) > wf) wf = length(f)
  if (length(name) > wn) wn = length(name)
}

function annolines(anno,   p) { return anno == "" ? 0 : split(anno, p, SEP) }

NR == FNR {
  k = $1 SUBSEP $2 SUBSEP $3
  okey[++no] = k; known[k] = 1; o_anno[k] = $5; o_body[k] = $6
  o_total[$2]++; o_alines += annolines($5); o_blines += lines($6)
  next
}

{
  k = $1 SUBSEP $2 SUBSEP $3
  nkey[++nn] = k; present[k] = 1; n_anno[k] = $5; n_body[k] = $6
  n_total[$2]++; n_alines += annolines($5); n_blines += lines($6)
}

END {
  # Pair removed and added blocks that are the same rule under a new name.
  for (i = 1; i <= no; i++) {
    k = okey[i]; if (k in present) continue
    split(k, p, SUBSEP); id = p[1] SUBSEP p[2] SUBSEP identity(p[2], o_body[k])
    rem_n[id]++; rem_k[id] = k
  }
  for (i = 1; i <= nn; i++) {
    k = nkey[i]; if (k in known) continue
    split(k, p, SUBSEP); id = p[1] SUBSEP p[2] SUBSEP identity(p[2], n_body[k])
    add_n[id]++; add_k[id] = k
  }
  for (id in rem_n)
    if (rem_n[id] == 1 && add_n[id] == 1) { old_of[add_k[id]] = rem_k[id]; renamed[rem_k[id]] = 1 }

  for (i = 1; i <= nn; i++) {
    k = nkey[i]; split(k, p, SUBSEP); file = p[1]; kind = p[2]; name = p[3]
    if (k in known) {
      a = (o_anno[k] != n_anno[k]); b = (o_body[k] != n_body[k])
      cat = (!a && !b) ? "unchanged" : (a && b) ? "annotation and body" : a ? "annotation only" : "body only"
      record(cat, kind)
      rest = n_anno[k]
      if (b) {
        d = linediff(o_body[k], n_body[k]); changed_blocks++
        file_cause(kind, file, name, d)
        rest = (rest == "" ? "" : rest "  ") d
      }
      if (cat != "unchanged") detail(cat, kind, file, name, rest)
    } else if (k in old_of) {
      ok = old_of[k]; split(ok, q, SUBSEP); oldname = q[3]
      a = (o_anno[ok] != n_anno[k]); b = (nameless(o_body[ok]) != nameless(n_body[k]))
      rest = n_anno[k]
      if (a && rest == "") rest = "annotation removed"
      d = linediff(o_body[ok], n_body[k]); changed_blocks++
      file_cause(kind, file, name, d)
      if (b) rest = rest "  body changed"
      rest = rest "  " d
      record("renamed", kind)
      detail("renamed", kind, file, oldname " -> " name, rest)
    } else {
      cat = (n_anno[k] != "") ? "added with annotation" : "added without annotation"
      record(cat, kind)
      added_blocks++; added_lines += lines(n_body[k])
      detail(cat, kind, file, name, n_anno[k])
    }
  }
  for (i = 1; i <= no; i++) {
    k = okey[i]; if ((k in present) || (k in renamed)) continue
    split(k, p, SUBSEP)
    unpaired = unpaired "\n  " p[2] " " short(p[1]) " " p[3]
  }

  printf "baseline: %s   head: %s   path: %s\n\n", base, head, path
  printf "%-26s %6s %9s %9s\n", "CATEGORY", "TOTAL", "REACTIONS", "ROUTINES"
  for (i = 1; i <= n; i++) {
    cat = order[i]
    printf "%-26s %6d %9d %9d\n", cat, count[cat] + 0, count[cat, "reaction"] + 0, count[cat, "routine"] + 0
  }
  printf "%-26s %6d %9d %9d\n", "blocks in baseline", no + 0, o_total["reaction"] + 0, o_total["routine"] + 0
  printf "%-26s %6d %9d %9d\n", "blocks in head", nn + 0, n_total["reaction"] + 0, n_total["routine"] + 0

  o_outside = o_loc - o_alines - o_blines; n_outside = n_loc - n_alines - n_blines
  printf "\n%-44s %9s %9s %11s\n", "LINES OF CODE", "BASELINE", "HEAD", "DIFFERENCE"
  printf "%-44s %9d %9d %+11d\n", "total", o_loc, n_loc, n_loc - o_loc
  printf "%-44s %9d %9d %+11d\n", "annotation lines", o_alines, n_alines, n_alines - o_alines
  printf "%-44s %9d %9d %+11d\n", "lines outside blocks", o_outside, n_outside, n_outside - o_outside
  printf "%-44s %9d %9d\n", "lines in blocks", o_blines, n_blines
  printf "%-44s %9s %9d %+11d\n", "  in " (added_blocks + 0) " added blocks", "", added_lines, added_lines
  printf "%-44s %9s %9s %11s\n", "  in " (changed_blocks + 0) " changed or renamed blocks", "", "", "+" (changed_plus + 0) "/-" (changed_minus + 0)
  printf "%-44s %9s %9s %+11d\n", "sum of the differences", "", "",
    (n_alines - o_alines) + (n_outside - o_outside) + added_lines + changed_plus - changed_minus

  printf "\nCHANGED OR RENAMED BLOCKS BY CAUSE\n"
  for (i = 1; i <= ncauses; i++) {
    c = causes[i]
    printf "%s (%d blocks; %s)\n", c, cn[c] + 0, commits[c]
    for (j = 1; j <= cn[c]; j++) print cl[c, j]
  }

  status = 0
  if (uncaused != "") {
    print "WARNING: changed or renamed block(s) without a cause:" uncaused > "/dev/stderr"; status = 1
  }
  for (key in cause) if (!(key in used)) {
    print "WARNING: the cause list names a block that did not change: " key > "/dev/stderr"; status = 1
  }
  printf "\nchecks: baseline %d header lines / %d blocks parsed, %d annotation lines / %d attached to a block\n", o_headers, no + 0, o_atlines, o_alines + 0
  printf "        head     %d header lines / %d blocks parsed, %d annotation lines / %d attached to a block\n", n_headers, nn + 0, n_atlines, n_alines + 0
  if (o_headers != no + 0 || n_headers != nn + 0) {
    print "WARNING: not every reaction/routine header became a block (brace mis-count?)" > "/dev/stderr"; status = 1
  }
  if (o_atlines != o_alines + 0 || n_atlines != n_alines + 0) {
    print "WARNING: not every annotation line was attached to a block (blank line or comment between annotation and block?)" > "/dev/stderr"; status = 1
  }
  if (unpaired != "") {
    print "WARNING: block(s) exist only in the baseline and are not shown in the table:" unpaired > "/dev/stderr"; status = 1
  }

  fmt = "  %-8s  %-" wf "s  %-" wn "s  %s"
  for (i = 2; i <= n; i++) {
    cat = order[i]; if (dn[cat] == 0) continue
    printf "\n%s\n", toupper(cat)
    for (j = 1; j <= dn[cat]; j++) {
      split(dl[cat, j], f, "\t")
      line = sprintf(fmt, f[1], f[2], f[3], f[4]); sub(/[ \t]+$/, "", line); print line
    }
  }
  exit status
}
AWK

# Unpacks the reactions of one revision and turns them into block records.
# One archive per revision keeps the blobless clone to a single fetch each.
extract() { # <rev> <name>
  local rev="$1" dir="$tmp/$2" out="$tmp/$2.tsv" f
  mkdir -p "$dir"
  git -C "$clone" archive "$rev" -- "$path" | tar -x -C "$dir"
  : > "$out"
  while IFS= read -r f; do
    awk -v file="${f#$dir/}" -f "$parse_awk" "$f" >> "$out"
  done < <(find "$dir" -name '*.reactions')
  LC_ALL=C sort -o "$out" "$out"
}

# Counts the lines matching a pattern over all reactions of one revision, to
# verify the parser against. grep exits 1 when it counts nothing.
count_lines() { # <name> <regex>
  find "$tmp/$1" -name '*.reactions' -exec cat {} + | grep -cE "$2" || true
}

extract "$base" old
extract "$head_rev" new

[[ -s "$tmp/new.tsv" ]] || { echo "No .reactions files found under '$path'." >&2; exit 1; }

header_re='^[[:space:]]*(reaction|routine)[[:space:]]+[A-Za-z0-9_]+'
anno_re='^[[:space:]]*@'
# The lines count-loc.sh counts, file by file: not blank and not starting with a
# comment marker.
loc() { # <name>
  find "$tmp/$1" -name '*.reactions' -exec awk '
    { line = $0; sub(/\r$/, "", line); gsub(/^[ \t]+|[ \t]+$/, "", line)
      if (line == "" || line ~ /^(\/\/|#|--|\*|\/\*|\*\/)/) next
      n++ }
    END { print n + 0 }' {} + | awk '{ total += $1 } END { print total + 0 }'
}
status=0
awk -v base="$base_label" -v head="$head_label" -v path="$path" \
    -v o_headers="$(count_lines old "$header_re")" -v o_atlines="$(count_lines old "$anno_re")" \
    -v n_headers="$(count_lines new "$header_re")" -v n_atlines="$(count_lines new "$anno_re")" \
    -v o_loc="$(loc old)" -v n_loc="$(loc new)" \
    -f "$classify_awk" "$tmp/old.tsv" "$tmp/new.tsv" || status=$?

exit "$status"
