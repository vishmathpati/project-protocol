#!/usr/bin/env bash
# Synchronize plugin manifest versions and run the structural release audit.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="$ROOT/.version-bump.json"

files() {
  python3 - "$CONFIG" <<'PY'
import json, sys
for item in json.load(open(sys.argv[1]))["files"]:
    print(item["path"] + "\t" + item["field"])
PY
}

get() {
  python3 - "$1" "$2" <<'PY'
import json, sys
node=json.load(open(sys.argv[1]))
for part in sys.argv[2].split('.'):
    node=node[int(part)] if isinstance(node,list) else node[part]
print(node)
PY
}

set_version() {
  python3 - "$1" "$2" "$3" <<'PY'
import json, sys
path, field, value=sys.argv[1:]
data=json.load(open(path)); node=data; parts=field.split('.')
for part in parts[:-1]: node=node[int(part)] if isinstance(node,list) else node[part]
if isinstance(node,list): node[int(parts[-1])]=value
else: node[parts[-1]]=value
with open(path,'w') as f: json.dump(data,f,indent=2); f.write('\n')
PY
}

check() {
  local expected="" failed=0 value
  echo "Version check:"
  while IFS=$'\t' read -r path field; do
    [[ -f "$ROOT/$path" ]] || { echo "  missing: $path"; failed=1; continue; }
    value="$(get "$ROOT/$path" "$field")"
    echo "  $path -> $value"
    [[ -z "$expected" ]] && expected="$value"
    [[ "$value" == "$expected" ]] || failed=1
  done < <(files)
  [[ $failed -eq 0 ]] || { echo "Version drift detected." >&2; return 1; }
  echo "  all manifests agree: $expected"
}

bump() {
  local version="$1" old
  [[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+([+-][a-zA-Z0-9._-]+)?$ ]] || { echo "Invalid semver: $version" >&2; exit 1; }
  while IFS=$'\t' read -r path field; do
    old="$(get "$ROOT/$path" "$field")"
    set_version "$ROOT/$path" "$field" "$version"
    echo "$path: $old -> $version"
  done < <(files)
}

case "${1:---help}" in
  --check) check ;;
  --audit) check; python3 "$ROOT/scripts/validate_plugin.py" ;;
  --help|-h) echo "Usage: bump-version.sh <version> | --check | --audit" ;;
  -*) echo "Unknown option: $1" >&2; exit 1 ;;
  *) bump "$1" ;;
esac
