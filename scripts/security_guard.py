"""Reject secrets/dumps in source; print file paths and rule names, never content."""
import argparse
from pathlib import Path
import re
import shutil
import subprocess


def violations(name, data):
    path = Path(name)
    findings = []
    if (path.name == '.env' or path.name.startswith('.env.')) and not path.name.endswith('.example'):
        findings.append('environment file')
    if path.suffix.lower() in {'.key', '.pem', '.p12', '.pfx', '.dump', '.backup'}:
        findings.append('private key or database archive')
    if path.name.endswith(('.sql.gz', '.sql.zip')):
        findings.append('database archive')
    if (b'PostgreSQL ' + b'database dump') in data or re.search(rb'COPY public\.\w+ .* FROM stdin;', data):
        findings.append('PostgreSQL dump content')
    if re.search(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', data):
        findings.append('private key content')
    if name.startswith('frontend/') and re.search(rb'["\x27]phone["\x27]\s*:\s*["\x27]\+?\d{7,}', data):
        findings.append('embedded phone record')
    return findings


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--snapshot', type=Path, help='New directory to copy scan candidates into')
    args = parser.parse_args()
    if args.self_test:
        assert violations('backend/.env.prod', b'synthetic')
        assert violations('innocent.txt', b'PostgreSQL ' + b'database dump')
        assert violations('innocent.txt', b'-----BEGIN ' + b'PRIVATE KEY-----')
        assert violations('frontend/sample.js', b'{"phone": "+12025550101"}')
        assert not violations('backend/example.env', b'PASSWORD=replace-me')
        print('Security guard sentinel checks passed.')
        return
    root = Path(__file__).resolve().parents[1]
    names = subprocess.check_output(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=root).decode().split('\0')
    failures = []
    files = []
    for name in sorted(set(filter(None, names))):
        path = root / name
        if not path.exists():  # deletions in the current working tree
            continue
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            failures.append((name, ['unexpected symbolic link']))
            continue
        findings = violations(name, path.read_bytes())
        if findings:
            failures.append((name, findings))
        files.append((name, path))
    for name, findings in failures:
        print(f'{name}: {", ".join(findings)}')
    if failures:
        raise SystemExit(1)
    if args.snapshot:
        args.snapshot.mkdir(parents=True, exist_ok=False)
        for name, path in files:
            destination = args.snapshot / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, destination)
    print(f'Security source guard passed ({len(files)} files).')


if __name__ == '__main__':
    main()
