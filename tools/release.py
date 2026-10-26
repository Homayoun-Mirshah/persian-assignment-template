"""Build the lightweight ZIP and a dependency-inclusive Windows sibling."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from urllib.request import urlopen, Request
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assignment-template'
BUNDLED = ROOT / 'assignment-template-bundled'
OUTPUT = ROOT / 'output'
CACHE = OUTPUT / 'dependencies'
TEMP = ROOT / 'tmp' / 'release'
OMIT_DIRS = {'build', 'tmp', '__pycache__'}
FONT_NAMES = (
    'Vazirmatn-VariableFont_wght.ttf', 'Vazirmatn-Bold.ttf',
    'Lora-Regular.ttf', 'Lora-Bold.ttf', 'Lora-Italic.ttf', 'Lora-BoldItalic.ttf',
    'JetBrainsMono-Regular.otf', 'JetBrainsMono-Bold.otf',
    'JetBrainsMono-Italic.otf', 'JetBrainsMono-BoldItalic.otf',
)
LICENSES = {
    'fonts/Vazirmatn-OFL.txt': 'https://raw.githubusercontent.com/rastikerdar/vazirmatn/master/OFL.txt',
    'fonts/Lora-OFL.txt': 'https://raw.githubusercontent.com/google/fonts/main/ofl/lora/OFL.txt',
    'fonts/JetBrainsMono-OFL.txt': 'https://raw.githubusercontent.com/JetBrains/JetBrainsMono/master/OFL.txt',
    'texmf/LPPL-1.3c.txt': 'https://www.latex-project.org/lppl/lppl-1-3c.txt',
}


def run(*arguments, cwd=ROOT, env=None):
    print('+', ' '.join(str(x) for x in arguments), flush=True)
    subprocess.run([str(x) for x in arguments], cwd=cwd, env=env, check=True)


def safe_remove(path: Path):
    resolved = path.resolve()
    if resolved in {ROOT, SOURCE} or not resolved.is_relative_to(ROOT):
        raise RuntimeError(f'Refusing to remove {resolved}')
    if path.exists():
        shutil.rmtree(path)


def omitted(path: Path, root: Path):
    parts = path.relative_to(root).parts
    return any(p in OMIT_DIRS or p.startswith(('.venv', '_minted')) or p.endswith('.egg-info') for p in parts)


def source_files():
    return sorted(p for p in SOURCE.rglob('*') if p.is_file()
                  and not omitted(p, SOURCE) and p.suffix not in {'.pyc', '.pyo', '.bak', '.tmp'})


def download(url: str, destination: Path):
    if destination.exists():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={'User-Agent': 'PersianAssignmentTemplate/1.0'})
    with urlopen(request, timeout=60) as response:
        content = response.read()
    if len(content) < 200:
        raise RuntimeError(f'Unexpectedly short license response: {url}')
    destination.write_bytes(content)


def kpsewhich(name: str):
    result = subprocess.run(['kpsewhich', name], check=True, capture_output=True, text=True)
    path = Path(result.stdout.strip())
    if not path.is_file():
        raise FileNotFoundError(name)
    return path


def find_font(name: str):
    try:
        return kpsewhich(name)
    except (subprocess.CalledProcessError, FileNotFoundError):
        paths = [Path.home() / 'AppData/Local/Microsoft/Windows/Fonts' / name,
                 Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts' / name]
        for path in paths:
            if path.is_file():
                return path
    raise FileNotFoundError(f'Install the font first: {name}')


def prepare_wheels(python: Path, env: dict):
    wheels = CACHE / 'wheelhouse'
    wheels.mkdir(parents=True, exist_ok=True)
    run(python, '-m', 'pip', 'download', '--no-cache-dir', '--only-binary=:all:',
        '--dest', wheels, '-r', SOURCE / 'tools/requirements.txt',
        '-r', SOURCE / 'tools/requirements-docs.txt', env=env)
    theme_source = TEMP / 'theme-source'
    safe_remove(theme_source)
    shutil.copytree(SOURCE / 'tools/themes', theme_source,
                    ignore=shutil.ignore_patterns('__pycache__', '*.egg-info', 'build'))
    run(python, '-m', 'pip', 'wheel', '--no-cache-dir', '--no-deps',
        '--wheel-dir', wheels, theme_source, env=env)
    return wheels


def copy_payload(wheels: Path):
    safe_remove(BUNDLED)
    BUNDLED.mkdir()
    files = source_files()
    for path in files:
        destination = BUNDLED / path.relative_to(SOURCE)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
    for name in FONT_NAMES:
        destination = BUNDLED / 'fonts' / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(find_font(name), destination)
    for relative, url in LICENSES.items():
        cached = CACHE / relative
        download(url, cached)
        destination = BUNDLED / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(cached, destination)
    for name in ('minted', 'fvextra', 'latex2pydata'):
        style = kpsewhich(name + '.sty')
        destination = BUNDLED / 'texmf/tex/latex' / name / style.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(style, destination)
        source = kpsewhich(name + '.dtx')
        destination = BUNDLED / 'texmf/source/latex' / name / source.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    shutil.copytree(wheels, BUNDLED / 'wheelhouse')
    for name in ('setup.cmd', 'setup.ps1'):
        shutil.copy2(ROOT / 'tools/bundle' / name, BUNDLED / name)
    (BUNDLED / 'tools/bin').mkdir()
    shutil.copy2(ROOT / 'tools/bundle/latexminted.cmd', BUNDLED / 'tools/bin/latexminted.cmd')
    for path in files:
        if path.read_bytes() != (BUNDLED / path.relative_to(SOURCE)).read_bytes():
            raise RuntimeError(f'Source/bundled mismatch: {path}')
    print(f'Synchronized {len(files)} canonical source files.', flush=True)


def refresh_sources():
    """Update the generated sibling after documentation-only maintenance."""
    manifest_path = BUNDLED / 'DEPENDENCIES.json'
    if not manifest_path.is_file():
        raise RuntimeError('Build the complete bundled sibling before refreshing sources.')
    previous = json.loads(manifest_path.read_text(encoding='utf-8')).get('canonical_sources', [])
    files = source_files()
    current = {p.relative_to(SOURCE).as_posix() for p in files}
    for name in previous:
        if name not in current:
            target = (BUNDLED / name).resolve()
            if not target.is_relative_to(BUNDLED) or target == BUNDLED:
                raise RuntimeError(f'Invalid previous source path: {name}')
            target.unlink(missing_ok=True)
    for path in files:
        destination = BUNDLED / path.relative_to(SOURCE)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
    # Refresh maintained launcher sources as well, without recreating a ready venv.
    for name in ('setup.cmd', 'setup.ps1'):
        shutil.copy2(ROOT / 'tools/bundle' / name, BUNDLED / name)
    shutil.copy2(ROOT / 'tools/bundle/latexminted.cmd', BUNDLED / 'tools/bin/latexminted.cmd')
    write_manifest()


def write_manifest():
    payload = {}
    for path in sorted(BUNDLED.rglob('*')):
        if not path.is_file() or path.name == 'DEPENDENCIES.json' or omitted(path, BUNDLED):
            continue
        payload[path.relative_to(BUNDLED).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest = {
        'format': 1,
        'description': 'Source and offline dependency payload; .venv is recreatable and excluded from this payload manifest.',
        'requires': ['Windows', 'Python >= 3.9 with venv', 'TeX Live with XeLaTeX, latexmk and standard packages'],
        'font_families': ['Vazirmatn', 'Lora', 'JetBrains Mono'],
        'canonical_sources': [p.relative_to(SOURCE).as_posix() for p in source_files()],
        'license_sources': LICENSES,
        'sha256': payload,
    }
    (BUNDLED / 'DEPENDENCIES.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def package_tree(root: Path, target: Path, include_venv: bool):
    paths = []
    for path in sorted(root.rglob('*')):
        if not path.is_file():
            continue
        parts = path.relative_to(root).parts
        if any(x in OMIT_DIRS or x.startswith('_minted') or x.endswith('.egg-info') for x in parts):
            continue
        if not include_venv and any(x.startswith('.venv') for x in parts):
            continue
        if path.suffix in {'.pyc', '.pyo', '.bak', '.tmp'}:
            continue
        paths.append(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(target, 'w', compression=ZIP_DEFLATED, compresslevel=6) as archive:
        for path in paths:
            archive.write(path, root.name + '/' + path.relative_to(root).as_posix())
    with ZipFile(target) as archive:
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f'ZIP CRC failed: {bad}')
        if len(archive.namelist()) != len(paths):
            raise RuntimeError('Unexpected archive count')
        for path in paths:
            archived = archive.read(root.name + '/' + path.relative_to(root).as_posix())
            if hashlib.sha256(archived).digest() != hashlib.sha256(path.read_bytes()).digest():
                raise RuntimeError(f'ZIP/source mismatch: {path}')
    print(f'Verified {target}: {len(paths)} files, {target.stat().st_size:,} bytes.', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--python', type=Path, default=Path(getattr(sys, '_base_executable', sys.executable)),
                        help='Installed base Python used to create the bundled venv.')
    parser.add_argument('--reuse-wheels', action='store_true', help='Use an already prepared offline wheelhouse.')
    parser.add_argument('--package-only', action='store_true', help='Repackage verified existing folders without rebuilding dependency payloads.')
    parser.add_argument('--refresh-source', action='store_true', help='Refresh canonical sources and launchers in an existing bundled sibling, retaining its ready venv.')
    args = parser.parse_args()
    TEMP.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TEMP=str(TEMP), TMP=str(TEMP), PIP_DISABLE_PIP_VERSION_CHECK='1')
    if args.refresh_source:
        refresh_sources()
    elif not args.package_only:
        wheels = CACHE / 'wheelhouse' if args.reuse_wheels else prepare_wheels(args.python, env)
        if not wheels.is_dir() or not list(wheels.glob('*.whl')):
            raise RuntimeError('No cached wheels; run without --reuse-wheels first.')
        copy_payload(wheels)
        run('powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
            BUNDLED / 'setup.ps1', '-Python', args.python, env=env)
        write_manifest()
    # Reconfirm every canonical file before producing either archive.
    for path in source_files():
        if path.read_bytes() != (BUNDLED / path.relative_to(SOURCE)).read_bytes():
            raise RuntimeError(f'Bundled source is stale: {path}. Rebuild the sibling first.')
    package_tree(SOURCE, OUTPUT / 'zip/persian-assignment-template.zip', False)
    package_tree(BUNDLED, OUTPUT / 'zip/persian-assignment-template-bundled.zip', True)


if __name__ == '__main__':
    main()
