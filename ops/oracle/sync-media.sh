#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  cat <<'EOF'
Usage: ./ops/oracle/sync-media.sh <source-ssh> <destination-ssh> <cache-directory>

Run from WSL. The command synchronizes production media through a local cache:
  <source-ssh>:/srv/some-people-site/backend/media/
  -> <cache-directory>/
  -> <destination-ssh>:/srv/some-people-site/runtime/media/

SSH aliases or user@host values are accepted. Existing SSH configuration and
agent identities are used; the script never reads or copies private keys.
Files are not deleted from either endpoint.
EOF
}

[[ $# -eq 3 ]] || { usage >&2; exit 2; }

source_ssh="$1"
destination_ssh="$2"
cache_directory="$3"
source_path="/srv/some-people-site/backend/media/"
destination_path="/srv/some-people-site/runtime/media/"

command -v rsync >/dev/null 2>&1 || { echo "rsync is required" >&2; exit 127; }
command -v ssh >/dev/null 2>&1 || { echo "ssh is required" >&2; exit 127; }

mkdir -p "$cache_directory"

ssh -o BatchMode=yes "$source_ssh" "test -d '$source_path'"
ssh -o BatchMode=yes "$destination_ssh" "test -d '$destination_path' && test -w '$destination_path'"

rsync --archive --partial --human-readable --info=progress2 \
  "$source_ssh:$source_path" "$cache_directory/"
rsync --archive --partial --human-readable --info=progress2 \
  "$cache_directory/" "$destination_ssh:$destination_path"

source_count="$(ssh -o BatchMode=yes "$source_ssh" "find '$source_path' -type f -printf . | wc -c")"
cache_count="$(find "$cache_directory" -type f -printf . | wc -c)"
destination_count="$(ssh -o BatchMode=yes "$destination_ssh" "find '$destination_path' -type f -printf . | wc -c")"

source_pending="$(rsync --archive --checksum --dry-run --itemize-changes \
  "$source_ssh:$source_path" "$cache_directory/")"
destination_pending="$(rsync --archive --checksum --dry-run --itemize-changes \
  "$cache_directory/" "$destination_ssh:$destination_path")"

printf 'source_files=%s\ncache_files=%s\ndestination_files=%s\n' \
  "$source_count" "$cache_count" "$destination_count"

[[ -z "$source_pending" && -z "$destination_pending" ]] || {
  echo "Media checksum verification found pending changes; do not proceed with cutover" >&2
  exit 1
}
