"""Extract the bundled ZIP, rebuild its venv offline, and compile all documents."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'output/zip/persian-assignment-template-bundled.zip'
REPORT = ROOT / 'output/qa/bundle-relocation.json'


def main():
    destination = Path(tempfile.mkdtemp(prefix='bundled copy with spaces ', dir=ROOT / 'tmp'))
    with ZipFile(ARCHIVE) as archive:
        if archive.testzip():
            raise RuntimeError('Invalid archive')
        archive.extractall(destination)
    project = destination / 'assignment-template-bundled'
    manifest = json.loads((project / 'DEPENDENCIES.json').read_text(encoding='utf-8'))
    for name, digest in manifest['sha256'].items():
        if hashlib.sha256((project / name).read_bytes()).hexdigest() != digest:
            raise RuntimeError(f'Manifest mismatch: {name}')
    venv = (project / '.venv').resolve()
    if not venv.is_relative_to((ROOT / 'tmp').resolve()) or venv.name != '.venv':
        raise RuntimeError('Unsafe disposable venv path')
    python_candidates = [Path(getattr(sys, '_base_executable', sys.executable)),
                         Path.home() / 'AppData/Local/Python/pythoncore-3.14-64/python.exe']
    python = next((p for p in python_candidates if p.is_file() and 'codex-runtimes' not in str(p)), None)
    if python is None:
        raise RuntimeError('An installed base Python is needed for this Windows integration check')
    windows = Path(os.environ.get('WINDIR', 'C:/Windows'))
    tex_bin = Path(shutil.which('xelatex')).parent
    environment = dict(os.environ,
                       PATH=os.pathsep.join(map(str, [tex_bin, windows / 'System32', windows,
                                                       windows / 'System32/WindowsPowerShell/v1.0'])),
                       PIP_NO_INDEX='1', PIP_DISABLE_PIP_VERSION_CHECK='1', LC_ALL='C', LANG='C',
                       TEMP=str(project / 'tmp'), TMP=str(project / 'tmp'))
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    transcript = REPORT.with_suffix('.txt')
    with transcript.open('w', encoding='utf-8') as stream:
        # Verify the actual shipped environment before testing reconstruction.
        # Moving a venv between machines may require setup; on this machine its
        # base Python is present, so the copied environment must work directly.
        shipped = [str(venv / 'Scripts/python.exe'), '-c',
                   'import latexminted,markdown,setuptools,wheel; import pip._internal.operations.build.wheel; from pygments.styles import get_style_by_name; get_style_by_name("assignment-darcula")']
        stream.write('+ shipped venv readiness probe\n')
        stream.flush()
        probe = subprocess.run(shipped, cwd=project, env=environment, stdout=stream, stderr=subprocess.STDOUT)
        if probe.returncode:
            raise RuntimeError(f'Shipped venv is incomplete; see {transcript}')
        # Force a genuine offline reconstruction as a second, independent check.
        shutil.rmtree(venv)
        for command in (
            ['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(project / 'setup.ps1'), '-Python', str(python)],
            ['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(project / 'build.ps1'), '-Target', 'all'],
            [str(project / '.venv/Scripts/python.exe'), str(project / 'tools/project.py'), 'check'],
            [str(project / '.venv/Scripts/python.exe'), str(project / 'tools/project.py'), 'install-themes'],
            [str(project / '.venv/Scripts/python.exe'), str(project / 'tools/render_readme.py')],
        ):
            print('Running relocated:', command[0], flush=True)
            stream.write('+ ' + ' '.join(command) + '\n')
            stream.flush()
            result = subprocess.run(command, cwd=project, env=environment, stdout=stream, stderr=subprocess.STDOUT)
            if result.returncode:
                raise RuntimeError(f'Relocation check failed ({result.returncode}); see {transcript}')
    outputs = {}
    for name in ('main', 'example', 'code-demo'):
        pdf = project / 'build' / f'{name}.pdf'
        info = subprocess.run(['pdfinfo', str(pdf)], check=True, capture_output=True, text=True).stdout
        pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M)[1])
        log = (project / 'build' / f'{name}.log').read_text(encoding='utf-8', errors='replace')
        issues = [line for line in log.splitlines() if re.search(r'Overfull|Underfull|Missing character|LaTeX Warning:|Package .* Warning:|^!', line)]
        if issues:
            raise RuntimeError(f'{name}: {issues}')
        recorder = (project / 'build' / f'{name}.fls').read_text(encoding='utf-8', errors='replace').replace('\\', '/')
        for package in ('minted', 'fvextra', 'latex2pydata'):
            if f'texmf/tex/latex/{package}/{package}.sty' not in recorder:
                raise RuntimeError(f'{name} did not use local {package}')
        for family in ('Vazirmatn', 'Lora', 'JetBrainsMono'):
            if f'fonts/{family}' not in recorder:
                raise RuntimeError(f'{name} did not record the bundled {family} font')
        font_info = subprocess.run(['pdffonts', str(pdf)], check=True, capture_output=True, text=True).stdout
        if any(line.split()[-5] != 'yes' for line in font_info.splitlines()[2:] if line.strip()):
            raise RuntimeError(f'Unembedded font in {name}')
        outputs[name] = {'pages': pages, 'pdf': str(pdf), 'warnings': issues}
    result = {'archive': str(ARCHIVE), 'archive_sha256': hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
              'project': str(project), 'shipped_venv_ready': True, 'offline_recreation': True,
              'system_python_scripts_excluded_from_path': True,
              'local_fonts_and_tex_packages_verified': True, 'outputs': outputs}
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
