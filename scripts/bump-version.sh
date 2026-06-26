#!/usr/bin/env bash
# scripts/bump-version.sh — single-source version sync + audit for project-protocol
#
# Usage:
#   bump-version.sh <new-version>   Set version in all declared files (semver validated)
#   bump-version.sh --check         Print each file's version; exit 1 if they disagree
#   bump-version.sh --audit         --check + stale-string grep + skill-count + description validation
#   bump-version.sh --validate      Scan descriptions for Cowork-forbidden content (< > and URLs)
#
# Config is read from .version-bump.json at the repo root (python3, no jq required).

set -euo pipefail

# ── Locate repo root (directory containing .version-bump.json) ────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG="$REPO_ROOT/.version-bump.json"

if [[ ! -f "$CONFIG" ]]; then
  echo "ERROR: .version-bump.json not found at $REPO_ROOT" >&2
  exit 1
fi

# ── Python helpers (no jq) ────────────────────────────────────────────────────

# Read the version field from a JSON file
py_get_version() {
  local json_path="$1"
  local field="$2"
  python3 - "$json_path" "$field" <<'PYEOF'
import sys, json
path, field = sys.argv[1], sys.argv[2]
data = json.load(open(path))
print(data[field])
PYEOF
}

# Write (update) a single field in a JSON file, preserving 2-space indent
py_set_version() {
  local json_path="$1"
  local field="$2"
  local new_val="$3"
  python3 - "$json_path" "$field" "$new_val" <<'PYEOF'
import sys, json
path, field, new_val = sys.argv[1], sys.argv[2], sys.argv[3]
with open(path) as f:
    data = json.load(f)
data[field] = new_val
with open(path, 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')   # trailing newline
PYEOF
}

# Read the list of declared version-carrying files+fields from .version-bump.json
# Output: one "path<TAB>field" pair per line (tab separator avoids colon ambiguity)
py_list_files() {
  python3 - "$CONFIG" <<'PYEOF'
import sys, json
cfg = json.load(open(sys.argv[1]))
for entry in cfg['files']:
    print(entry['path'] + '\t' + entry['field'])
PYEOF
}

# Read the audit.exclude list; output one glob/name per line
py_list_excludes() {
  python3 - "$CONFIG" <<'PYEOF'
import sys, json
cfg = json.load(open(sys.argv[1]))
for pat in cfg.get('audit', {}).get('exclude', []):
    print(pat)
PYEOF
}

# ── Semver validation ─────────────────────────────────────────────────────────
validate_semver() {
  local v="$1"
  if ! [[ "$v" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9._-]+)?(\+[a-zA-Z0-9._-]+)?$ ]]; then
    echo "ERROR: '$v' does not look like a semver (expected X.Y.Z or X.Y.Z-pre)" >&2
    exit 1
  fi
}

# ── MODE: --check ─────────────────────────────────────────────────────────────
# Print each declared file's version; exit non-zero if any disagree.
cmd_check() {
  local first_version=""
  local drift=0

  echo "Version check (declared files):"
  while IFS=$'\t' read -r rel_path field; do
    local abs_path="$REPO_ROOT/$rel_path"
    if [[ ! -f "$abs_path" ]]; then
      echo "  ERROR: file not found: $rel_path" >&2
      drift=1
      continue
    fi
    local ver
    ver=$(py_get_version "$abs_path" "$field")
    echo "  $rel_path  →  $ver"

    if [[ -z "$first_version" ]]; then
      first_version="$ver"
    elif [[ "$ver" != "$first_version" ]]; then
      echo "  DRIFT: $rel_path is $ver but expected $first_version" >&2
      drift=1
    fi
  done < <(py_list_files)

  if [[ $drift -eq 0 ]]; then
    echo "  ✓ All files agree: $first_version"
  else
    echo "" >&2
    echo "  ✗ Version drift detected — run: bump-version.sh <version>" >&2
  fi

  return $drift
}

# ── MODE: --audit ─────────────────────────────────────────────────────────────
# 1. Run --check (version sync)
# 2. Grep repo for version strings that don't match the declared version
# 3. Verify skill count vs. "N skills" stated in manifests + README.md
cmd_audit() {
  local exit_code=0

  # Step 1 — version sync check
  if ! cmd_check; then
    exit_code=1
  fi
  echo ""

  # Determine the canonical version (from the first declared file)
  local first_path first_field canonical_version
  IFS=$'\t' read -r first_path first_field < <(py_list_files | head -1)
  canonical_version=$(py_get_version "$REPO_ROOT/$first_path" "$first_field")

  # Step 2 — stale version string grep
  # Build grep exclude args from .version-bump.json audit.exclude list.
  # Patterns ending in / are treated as directories; globs (containing *)
  # are passed as --exclude-glob; plain names as --exclude or --exclude-dir.
  echo "Stale-version grep (looking for version strings ≠ $canonical_version):"

  local grep_excludes=()
  while IFS= read -r pat; do
    if [[ "$pat" == *"*"* ]]; then
      # Glob pattern (e.g. AUDIT-*.md) — file exclusion
      grep_excludes+=("--exclude=$pat")
    elif [[ "$pat" == *"."* ]] || [[ "$pat" == *"/"* ]]; then
      # Pattern contains a dot (file extension) or slash (path) — file exclusion
      grep_excludes+=("--exclude=$(basename "$pat")")
    else
      # No dot, no glob, no slash — treat as a directory name
      # Works with grep -r when the search root is '.' (relative path)
      grep_excludes+=("--exclude-dir=$pat")
    fi
  done < <(py_list_excludes)

  # We search for version-flavored X.Y.Z strings that are NOT the canonical version.
  # The pattern anchors to common version contexts to avoid false positives
  # (WCAG spec numbers like 1.4.11, Node semver ranges like >=22.0.0, etc.):
  #   "version": "X.Y.Z"   — JSON version field
  #   v X.Y.Z              — bare v-prefix (changelog, prose, tags)
  #   [X.Y.Z]              — changelog "## [X.Y.Z]" header
  #   vX.Y.Z.md            — migration filename reference in prose
  #   pre-X.Y.Z            — pre-migration version marker
  # NOTE: grep --exclude-dir only works when recursing from a relative path (not an
  # absolute path on Linux). We cd into $REPO_ROOT so grep walks '.' and directory
  # exclusions apply correctly; then strip the leading './' from output paths.
  local stale_hits
  stale_hits=$(
    cd "$REPO_ROOT" && \
    grep -rn --include="*.json" --include="*.md" --include="*.sh" \
         --include="*.yaml" --include="*.yml" --include="*.txt" \
         "${grep_excludes[@]}" \
         -E '("version"[[:space:]]*:[[:space:]]*"|v[0-9]|\[[0-9])[0-9]*\.[0-9]+\.[0-9]+' \
         . 2>/dev/null \
      | sed 's|^\./||' \
      | grep -v ":.*${canonical_version//./\\.}" \
      | grep -v 'pre-[0-9]' \
      | grep -v 'v[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.md' \
      || true
  )

  if [[ -n "$stale_hits" ]]; then
    echo "  STALE version strings found (lines that contain a version ≠ $canonical_version):"
    echo "$stale_hits" | sed 's/^/    /'
    echo ""
    echo "  ✗ Stale version strings detected — review and update them." >&2
    exit_code=1
  else
    echo "  ✓ No stale version strings found."
  fi
  echo ""

  # Step 3 — skill count verification
  echo "Skill count check:"

  # Actual count: directories directly under skills/
  local actual_count
  actual_count=$(ls -d "$REPO_ROOT/skills"/*/ 2>/dev/null | wc -l | tr -d ' ')
  echo "  Actual skills/ directories: $actual_count"

  local count_ok=1  # assume OK; flip to 0 on any mismatch

  # Check .claude-plugin/plugin.json description
  local claude_desc
  claude_desc=$(python3 -c "import json; print(json.load(open('$REPO_ROOT/.claude-plugin/plugin.json'))['description'])")
  local claude_count
  claude_count=$(echo "$claude_desc" | grep -oE '[0-9]+ skills?' | grep -oE '[0-9]+' | head -1 || echo "")
  if [[ -n "$claude_count" ]]; then
    if [[ "$claude_count" == "$actual_count" ]]; then
      echo "  .claude-plugin/plugin.json description: $claude_count skills ✓"
    else
      echo "  .claude-plugin/plugin.json description: $claude_count skills ✗ (actual: $actual_count)" >&2
      count_ok=0
    fi
  else
    echo "  .claude-plugin/plugin.json: no 'N skills' phrase found in description"
  fi

  # Check .codex-plugin/plugin.json description
  local codex_desc
  codex_desc=$(python3 -c "import json; print(json.load(open('$REPO_ROOT/.codex-plugin/plugin.json'))['description'])")
  local codex_count
  codex_count=$(echo "$codex_desc" | grep -oE '[0-9]+ skills?' | grep -oE '[0-9]+' | head -1 || echo "")
  if [[ -n "$codex_count" ]]; then
    if [[ "$codex_count" == "$actual_count" ]]; then
      echo "  .codex-plugin/plugin.json description:  $codex_count skills ✓"
    else
      echo "  .codex-plugin/plugin.json description:  $codex_count skills ✗ (actual: $actual_count)" >&2
      count_ok=0
    fi
  else
    echo "  .codex-plugin/plugin.json: no 'N skills' phrase found in description"
  fi

  # Check README.md
  local readme_count
  readme_count=$(grep -oE '[0-9]+ skills?' "$REPO_ROOT/README.md" | grep -oE '[0-9]+' | head -1 || echo "")
  if [[ -n "$readme_count" ]]; then
    if [[ "$readme_count" == "$actual_count" ]]; then
      echo "  README.md:                               $readme_count skills ✓"
    else
      echo "  README.md:                               $readme_count skills ✗ (actual: $actual_count)" >&2
      count_ok=0
    fi
  else
    echo "  README.md: no 'N skills' phrase found"
  fi

  if [[ $count_ok -eq 0 ]]; then
    echo "" >&2
    echo "  ✗ Skill count mismatch — update the descriptions/README to match actual count ($actual_count)." >&2
    exit_code=1
  else
    echo "  ✓ Skill count consistent across all sources."
  fi
  echo ""

  # Step 4 — description validation (Cowork-forbidden content: < > and URLs)
  if ! cmd_validate; then
    exit_code=1
  fi

  return $exit_code
}

# ── MODE: --validate ──────────────────────────────────────────────────────────
# Scan every description field across the repo for Cowork-forbidden content.
# Cowork's plugin validator silently rejects an upload if any "description"
# contains '<' or '>' (HTML-sanitized away) or a URL (http:// or https://).
# This catches those BEFORE upload. Read-only; exits 1 if any are found.
#
# Scans:
#   1. Every plugin.json / marketplace.json (except dist/, .git/, node_modules/):
#        - top-level "description"
#        - plugins[].description  (marketplace.json shape; handled if present)
#   2. Every skills/*/SKILL.md frontmatter "description:" line
cmd_validate() {
  echo "Description validation (Cowork-forbidden content: < > and URLs):"

  # Gather every description (STATUS<TAB>...fields) via python3, then flag.
  # os.walk discovers plugin.json / marketplace.json anywhere in the repo, so a
  # marketplace.json is picked up automatically when it appears; SKILL.md
  # frontmatter descriptions are parsed in python too.
  local report
  report=$(
    python3 - "$REPO_ROOT" <<'PYEOF'
import sys, os, json, glob

repo_root = sys.argv[1]
forbidden = ['<', '>', 'http://', 'https://']
prune = {'dist', '.git', 'node_modules'}

# (relative_path, label, value) tuples to check
descriptions = []

# 1. JSON manifests anywhere in the repo (except dist/, .git/, node_modules/)
for dirpath, dirnames, filenames in os.walk(repo_root):
    # prune excluded directories in-place so os.walk does not descend into them
    dirnames[:] = [d for d in dirnames if d not in prune]
    for fname in filenames:
        if fname not in ('plugin.json', 'marketplace.json'):
            continue
        abs_path = os.path.join(dirpath, fname)
        rel = os.path.relpath(abs_path, repo_root)
        try:
            with open(abs_path) as f:
                data = json.load(f)
        except (OSError, ValueError):
            continue
        if isinstance(data, dict):
            if isinstance(data.get('description'), str):
                descriptions.append((rel, 'description', data['description']))
            # marketplace.json shape: a "plugins" array of objects
            plugins = data.get('plugins')
            if isinstance(plugins, list):
                for i, plug in enumerate(plugins):
                    if isinstance(plug, dict) and isinstance(plug.get('description'), str):
                        descriptions.append((rel, 'plugins[%d].description' % i, plug['description']))

# 2. skills/*/SKILL.md frontmatter description: line
for skill_md in sorted(glob.glob(os.path.join(repo_root, 'skills', '*', 'SKILL.md'))):
    rel = os.path.relpath(skill_md, repo_root)
    try:
        with open(skill_md) as f:
            lines = f.readlines()
    except OSError:
        continue
    # Frontmatter is the leading '---' fenced block
    if not lines or lines[0].strip() != '---':
        continue
    for line in lines[1:]:
        if line.strip() == '---':
            break
        if line.startswith('description:'):
            value = line[len('description:'):].strip()
            descriptions.append((rel, 'description', value))
            break

# Flag forbidden content; emit "STATUS\tpath\tlabel\ttoken\tvalue" rows
fail = False
for rel, label, value in descriptions:
    for tok in forbidden:
        if tok in value:
            fail = True
            print('FAIL\t%s\t%s\t%s\t%s' % (rel, label, tok, value))

print('TOTAL\t%d' % len(descriptions))
sys.exit(1 if fail else 0)
PYEOF
  ) || true

  local validate_fail=0
  local total=0
  while IFS=$'\t' read -r status f1 f2 f3 f4; do
    case "$status" in
      FAIL)
        # f1=path f2=label f3=token f4=value
        local snippet="$f4"
        if [[ ${#snippet} -gt 80 ]]; then
          snippet="${snippet:0:77}..."
        fi
        echo "  ✗ $f1 $f2 contains '$f3': \"$snippet\"" >&2
        validate_fail=1
        ;;
      TOTAL)
        total="$f1"
        ;;
    esac
  done <<< "$report"

  if [[ $validate_fail -eq 0 ]]; then
    echo "  ✓ No forbidden content found in $total descriptions."
  else
    echo "" >&2
    echo "  ✗ Forbidden content in descriptions — Cowork will silently reject this upload." >&2
  fi

  return $validate_fail
}

# ── MODE: <new-version> ───────────────────────────────────────────────────────
cmd_bump() {
  local new_version="$1"
  validate_semver "$new_version"

  echo "Bumping version to $new_version:"
  while IFS=$'\t' read -r rel_path field; do
    local abs_path="$REPO_ROOT/$rel_path"
    if [[ ! -f "$abs_path" ]]; then
      echo "  ERROR: file not found: $rel_path" >&2
      exit 1
    fi
    local old_ver
    old_ver=$(py_get_version "$abs_path" "$field")
    py_set_version "$abs_path" "$field" "$new_version"
    echo "  $rel_path  $old_ver → $new_version"
  done < <(py_list_files)

  echo ""
  echo "  ✓ Done. Commit the changes and tag: git tag v${new_version}"
}

# ── Entry point ───────────────────────────────────────────────────────────────
if [[ $# -eq 0 ]]; then
  echo "Usage:"
  echo "  bump-version.sh <new-version>   — bump version in all declared files"
  echo "  bump-version.sh --check         — verify all files agree on version"
  echo "  bump-version.sh --audit         — --check + stale-string grep + skill count + description validation"
  echo "  bump-version.sh --validate      — scan descriptions for Cowork-forbidden content (< > and URLs)"
  exit 0
fi

case "$1" in
  --check)     cmd_check     ;;
  --audit)     cmd_audit     ;;
  --validate)  cmd_validate  ;;
  --help|-h)
    echo "Usage:"
    echo "  bump-version.sh <new-version>   — bump version in all declared files"
    echo "  bump-version.sh --check         — verify all files agree on version"
    echo "  bump-version.sh --audit         — --check + stale-string grep + skill count + description validation"
    echo "  bump-version.sh --validate      — scan descriptions for Cowork-forbidden content (< > and URLs)"
    ;;
  -*)
    echo "ERROR: unknown flag '$1'" >&2
    exit 1
    ;;
  *)
    cmd_bump "$1"
    ;;
esac
