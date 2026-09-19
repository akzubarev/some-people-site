"""Scan the Git index before committing, including partially staged files.

Requires Docker (Gitleaks is pinned); no worktree or untracked data is scanned.
Run manually with `python scripts/secret_scan.py` or through pre-commit.
"""
from pathlib import Path, PurePosixPath
import subprocess
import tempfile

from security_guard import violations


def main():
    root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode().strip()
    entries = subprocess.check_output(['git', 'ls-files', '--stage', '-z'], cwd=root).split(b'\0')
    failures = []
    with tempfile.TemporaryDirectory(prefix='some-people-index-') as directory:
        for entry in filter(None, entries):
            metadata, raw_name = entry.split(b'\t', 1)
            mode, oid, stage = metadata.split()
            name = raw_name.decode('utf-8')
            path = PurePosixPath(name)
            if stage != b'0' or mode not in {b'100644', b'100755'}:
                failures.append((name, ['unmerged or unsupported index entry']))
                continue
            if path.is_absolute() or '..' in path.parts or '\\' in name:
                failures.append((name, ['unsupported path']))
                continue
            data = subprocess.check_output(['git', 'cat-file', 'blob', oid.decode()], cwd=root)
            findings = violations(name, data)
            if findings:
                failures.append((name, findings))
            target = Path(directory).joinpath(*path.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        for name, findings in failures:
            print(f'{name}: {", ".join(findings)}')
        if failures:
            return 1
        try:
            return subprocess.run([
                'docker', 'run', '--rm', '--network=none',
                '-v', f'{Path(directory).resolve().as_posix()}:/source:ro',
                'zricethezav/gitleaks:v8.30.1', 'dir', '/source', '--redact', '--no-banner',
            ], check=False).returncode
        except FileNotFoundError:
            print('Docker is required for the staged secret scan. Start Docker and retry.')
            return 2


if __name__ == '__main__':
    raise SystemExit(main())
