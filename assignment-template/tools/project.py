"""Check installed dependencies, clean generated files, or package this project."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = {
    'main.tex', 'metadata.tex', 'example.tex', 'code-demo.tex',
    'assignment.sty', 'editor-code.sty', 'assignment-fonts.sty',
    'assignment-themes.sty', 'settings.tex', 'README.md', 'README.html',
    'build.cmd', 'build.ps1', '.latexmkrc', '.gitignore',
}
FOLDERS = {'assets', 'examples', 'tools'}
GENERATED = {'build', 'tmp', '__pycache__', '.venv', '_minted'}
CLEAN_DIRECTORIES = {'build', 'tmp', '__pycache__', '_minted'}


def command(name, *arguments):
    environment = dict(os.environ)
    local_tex = ROOT / 'texmf/tex/latex'
    if local_tex.is_dir():
        environment['TEXINPUTS'] = local_tex.as_posix() + '//' + os.pathsep + environment.get('TEXINPUTS', '') + os.pathsep
    if name == 'latexminted':
        # Query the very Python environment whose packages are checked below.
        invocation = [sys.executable, '-c', 'from latexminted.cmdline import main; main()', *arguments]
    else:
        executable = shutil.which(name)
        if not executable:
            raise RuntimeError(f'{name} is not on PATH.')
        invocation = [executable, *arguments]
    result = subprocess.run(invocation, cwd=ROOT, env=environment, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def check():
    from importlib.metadata import version
    from pygments.styles import get_style_by_name
    for package in ('latexminted', 'Pygments', 'latex2pydata', 'latexrestricted', 'assignment-editorstyles'):
        print(package, version(package))
    for style in ('assignment-darcula', 'assignment-intellij', 'assignment-vscode-dark', 'assignment-matlab'):
        get_style_by_name(style)
    for name, minimum in (('minted', '3.8.0'), ('fvextra', '1.14.0'), ('latex2pydata', '0.7.0')):
        filename = Path(command('kpsewhich', name + '.sty'))
        local_texmf = ROOT / 'texmf'
        if filename.is_relative_to(ROOT) and not filename.is_relative_to(local_texmf):
            raise RuntimeError(f'{name} resolves outside the bundled texmf tree: {filename}')
        content = filename.read_text(encoding='utf-8', errors='replace')
        pattern = r'\\ProvidesPackage\{' + name + r'\}.*?\bv([0-9.]+)'
        found = re.search(pattern, content, re.S)
        if not found or tuple(map(int, found[1].split('.'))) < tuple(map(int, minimum.split('.'))):
            raise RuntimeError(f'{name} >= {minimum} is required: {filename}')
        print(name, found[1], filename)
    print(command('latexminted', '--version').splitlines()[0])
    print(command('latexmk', '-v').splitlines()[0])
    print('Python/TeX dependencies and all four code themes are ready.')


def generated(path):
    return any(part in GENERATED or part.endswith('.egg-info') for part in path.relative_to(ROOT).parts)


def clean():
    directories = [p for p in ROOT.rglob('*') if p.is_dir() and
                   not any(part.startswith('.venv') for part in p.relative_to(ROOT).parts) and
                   (p.name in CLEAN_DIRECTORIES or p.name.startswith('_minted') or p.name.endswith('.egg-info'))]
    for path in sorted(directories, key=lambda p: len(p.parts)):
        if path.exists():
            resolved = path.resolve()
            if not resolved.is_relative_to(ROOT) or resolved == ROOT:
                raise RuntimeError(f'Cleanup outside project: {resolved}')
            shutil.rmtree(resolved)
    for document in ('main', 'example', 'code-demo'):
        for suffix in ('pdf','aux','log','out','toc','lof','lot','fls','fdb_latexmk','synctex.gz','xdv'):
            (ROOT / f'{document}.{suffix}').unlink(missing_ok=True)
    print('Generated files removed; editable sources retained.')


def package(target, extract_to):
    names = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
                   if p.is_file() and not generated(p)
                   and (p.relative_to(ROOT).parts[0] in FOLDERS or p.name in ROOT_FILES)
                   and p.suffix.lower() not in {'.pyc','.pyo','.bak','.tmp'})
    assert ROOT_FILES.issubset(names)
    target.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(target, 'w', compression=ZIP_DEFLATED) as archive:
        for name in names:
            archive.write(ROOT / name, 'persian-assignment-template/' + name)
    with ZipFile(target) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(names)
        for name in names:
            original = (ROOT / name).read_bytes()
            assert hashlib.sha256(original).digest() == hashlib.sha256(archive.read('persian-assignment-template/' + name)).digest()
    print(f'{target}: {len(names)} files, {target.stat().st_size} bytes; CRC and SHA-256 verified.')
    if extract_to:
        extract_to.mkdir(parents=True, exist_ok=False)
        with ZipFile(target) as archive:
            archive.extractall(extract_to)
        print(f'Fresh copy: {extract_to / "persian-assignment-template"}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('check', 'clean', 'package', 'install-themes'))
    parser.add_argument('--output', type=Path, default=ROOT.parent/'output/zip/persian-assignment-template.zip')
    parser.add_argument('--extract-to', type=Path)
    arguments = parser.parse_args()
    bundled_python = ROOT / '.venv/Scripts/python.exe'
    if (arguments.action in {'check', 'install-themes'} and bundled_python.is_file()
            and Path(sys.executable).resolve() != bundled_python.resolve()):
        raise SystemExit(subprocess.run([str(bundled_python), str(Path(__file__).resolve()), *sys.argv[1:]]).returncode)
    if arguments.action == 'check':
        check()
    elif arguments.action == 'clean':
        clean()
    elif arguments.action == 'install-themes':
        extra = ['--no-index', '--no-build-isolation'] if (ROOT/'wheelhouse').is_dir() else []
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-cache-dir', '--no-deps', *extra, str(ROOT/'tools/themes')], check=True)
    else:
        package(arguments.output, arguments.extract_to)
