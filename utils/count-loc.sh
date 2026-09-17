#!/usr/bin/env bash
#
# count-loc.sh -- Count lines of code in all files within a folder (recursive).
#
# Blank lines and comment-only lines are always ignored.
#
# Usage:
#   ./count-loc.sh <folder> [options]
#
# Options:
#   -e, --ext <ext>     Only count files with this extension (repeatable),
#                       e.g. -e reactions -e xtend
#   -q, --quiet         Print only the grand total
#   -h, --help          Show this help
#
# Example:
#   ./count-loc.sh "E:/projects/IntelliJ/Vitruv-CaseStudies/umljava/src/main/reactions/tools/vitruv/applications/umljava"
#
set -euo pipefail

usage() { sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'; }

folder=""
exts=()
quiet=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    -e|--ext)  exts+=("${2#.}"); shift 2 ;;
    -q|--quiet) quiet=1; shift ;;
    -h|--help)  usage; exit 0 ;;
    -*)         echo "Unknown option: $1" >&2; usage >&2; exit 1 ;;
    *)          folder="$1"; shift ;;
  esac
done

[[ -n "$folder" ]] || { echo "Error: no folder given." >&2; usage >&2; exit 1; }
[[ -d "$folder" ]] || { echo "Error: '$folder' is not a directory." >&2; exit 1; }

# Normalise the root so listed paths are always relative to it, no matter how
# it was written on the command line (trailing slash, backslashes, "..", ...).
root=$(cd "$folder" && pwd)

# Collect files (NUL-separated so spaces in paths are safe).
find_args=("$root" -type f)
# Skip the usual noise directories / binaries.
find_args+=(-not -path '*/.git/*' -not -path '*/node_modules/*' -not -path '*/bin/*'
            -not -path '*/build/*' -not -path '*/target/*' -not -path '*/.gradle/*')

if [[ ${#exts[@]} -gt 0 ]]; then
  find_args+=(\()
  first=1
  for e in "${exts[@]}"; do
    [[ $first -eq 1 ]] || find_args+=(-o)
    find_args+=(-name "*.$e")
    first=0
  done
  find_args+=(\))
fi

files=()
while IFS= read -r -d '' f; do files+=("$f"); done < <(find "${find_args[@]}" -print0 | sort -z)

[[ ${#files[@]} -gt 0 ]] || { echo "No matching files found in '$folder'."; exit 0; }

# Counts one file, echoes "<lines>".
count_file() {
  awk '
    {
      line = $0
      gsub(/^[ \t]+|[ \t]+$/, "", line)
      if (line == "") next
      if (line ~ /^(\/\/|#|--|\*|\/\*|\*\/)/) next
      n++
    }
    END { print n + 0 }
  ' "$1"
}

total=0
declare -A ext_lines ext_files
[[ $quiet -eq 1 ]] || printf '%8s  %s\n' "LINES" "FILE"
[[ $quiet -eq 1 ]] || printf '%8s  %s\n' "--------" "----------------------------------------"

for f in "${files[@]}"; do
  n=$(count_file "$f")
  total=$(( total + n ))
  rel="${f#"$root/"}"
  base="${f##*/}"
  if [[ "$base" == *.* ]]; then ext="${base##*.}"; else ext="(none)"; fi
  ext_lines["$ext"]=$(( ${ext_lines["$ext"]:-0} + n ))
  ext_files["$ext"]=$(( ${ext_files["$ext"]:-0} + 1 ))
  [[ $quiet -eq 1 ]] || printf '%8d  %s\n' "$n" "$rel"
done

if [[ $quiet -eq 1 ]]; then
  echo "$total"
  exit 0
fi

echo
echo "By extension:"
for ext in $(printf '%s\n' "${!ext_lines[@]}" | sort); do
  printf '%8d  %-12s (%d file(s))\n' "${ext_lines[$ext]}" ".$ext" "${ext_files[$ext]}"
done

echo
printf '%8d  TOTAL in %d file(s), excluding blank + comment-only lines\n' "$total" "${#files[@]}"
