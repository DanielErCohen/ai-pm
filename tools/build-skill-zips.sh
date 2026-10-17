#!/usr/bin/env bash
# Builds one zip per Claude skill into ai-pm/downloads/<skill-name>.zip.
# Each zip holds the skill folder at its top level (<skill>/SKILL.md), the layout the
# Claude app expects when you upload a skill (Customize, Skills, "+", Create skill, Upload a skill).
#
# Sources, relative to the ai-pm folder:
#   ../how-i-work/skills/recipient-panel, product-sparring, voice
#   ../how-i-work/meeting-review
#   ../cv-tailor/skills/*
# distill-to-gh-issue is not zipped: it needs gh and a local repository, so it works in Claude Code only.
#
# The zips are built from a staging copy, so the source repositories stay untouched:
#   - the Claude app accepts only these frontmatter keys: name, description, license,
#     compatibility, metadata, allowed-tools. The `effort:` and `argument-hint:` lines are removed
#     from the staged SKILL.md, and the build stops if any other key remains;
#   - cv-review and cv-tailor get guides/07-ats-checks.md from cv-tailor as <skill>/ats-checks.md,
#     where their SKILL.md looks for it when it runs outside the repository.
#
# Run from anywhere: bash ai-pm/tools/build-skill-zips.sh
# Stops with an error if a source folder or its SKILL.md is missing, or if a private
# file (config.local.md) ends up inside a zip.
set -euo pipefail

SITE="$(cd "$(dirname "$0")/.." && pwd)"
ROOT="$(cd "$SITE/.." && pwd)"
HIW="$ROOT/how-i-work"
CVT="$ROOT/cv-tailor"
OUT="$SITE/downloads"
ALLOWED_KEYS='name|description|license|compatibility|metadata|allowed-tools'

fail() { echo "build-skill-zips: $*" >&2; exit 1; }

command -v zip >/dev/null 2>&1 || fail "zip is not installed"
command -v unzip >/dev/null 2>&1 || fail "unzip is not installed"

SOURCES=(
  "$HIW/skills/recipient-panel"
  "$HIW/skills/product-sparring"
  "$HIW/skills/voice"
  "$HIW/meeting-review"
)

[ -d "$CVT/skills" ] || fail "missing source folder: $CVT/skills"
cv_count=0
for d in "$CVT"/skills/*/; do
  [ -d "$d" ] || continue
  SOURCES+=("${d%/}")
  cv_count=$((cv_count + 1))
done
[ "$cv_count" -gt 0 ] || fail "no skill folders found in $CVT/skills"

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

mkdir -p "$OUT"
seen=" "
for src in "${SOURCES[@]}"; do
  [ -d "$src" ] || fail "missing source folder: $src"
  [ -f "$src/SKILL.md" ] || fail "no SKILL.md in $src"
  name="$(basename "$src")"
  case "$seen" in *" $name "*) fail "two skills share the name $name" ;; esac
  seen="$seen$name "

  # Staging copy: the repository sources stay as they are.
  cp -R "$src" "$STAGE/$name"
  find "$STAGE/$name" \( -name '.DS_Store' -o -name '*.local.md' \) -delete

  # Remove the frontmatter keys the Claude app rejects, then check what is left.
  awk '
    NR == 1 && $0 == "---" { fm = 1; print; next }
    fm == 1 && $0 == "---" { fm = 2; print; next }
    fm == 1 && /^(effort|argument-hint):/ { next }
    { print }
  ' "$STAGE/$name/SKILL.md" > "$STAGE/$name/SKILL.md.new"
  mv "$STAGE/$name/SKILL.md.new" "$STAGE/$name/SKILL.md"
  bad_keys="$(awk 'NR == 1 && $0 != "---" { exit } NR > 1 && $0 == "---" { exit } NR > 1 && /^[A-Za-z][A-Za-z0-9_-]*:/ { sub(/:.*/, ""); print }' "$STAGE/$name/SKILL.md" | grep -vxE "$ALLOWED_KEYS" || true)"
  [ -z "$bad_keys" ] || fail "$name/SKILL.md has frontmatter keys the Claude app rejects: $(echo $bad_keys)"

  # The ATS checklist sits beside SKILL.md in the two skills that read it.
  case "$name" in
    cv-review|cv-tailor)
      [ -f "$CVT/guides/07-ats-checks.md" ] || fail "missing $CVT/guides/07-ats-checks.md"
      cp "$CVT/guides/07-ats-checks.md" "$STAGE/$name/ats-checks.md"
      ;;
  esac

  zip_path="$OUT/$name.zip"
  rm -f "$zip_path"
  (cd "$STAGE" && zip -r -X -q "$zip_path" "$name" -x '*.DS_Store' -x '*.local.md') \
    || fail "zip failed for $src"

  listing="$(unzip -Z1 "$zip_path")"
  printf '%s\n' "$listing" | grep -qx "$name/SKILL.md" || fail "$zip_path has no $name/SKILL.md at its top level"
  if printf '%s\n' "$listing" | grep -v "^$name/" | grep -q .; then
    fail "$zip_path has entries outside the $name/ folder"
  fi
  if printf '%s\n' "$listing" | grep -q '\.local\.md$'; then
    fail "$zip_path contains a private .local.md file"
  fi

  printf '%-24s %6s bytes  %s files\n' "$name.zip" "$(wc -c < "$zip_path" | tr -d ' ')" "$(printf '%s\n' "$listing" | grep -vc '/$')"
done

echo "Built ${#SOURCES[@]} zips in $OUT"
