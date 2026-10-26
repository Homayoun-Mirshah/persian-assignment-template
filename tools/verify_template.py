"""Compile real document palettes and font overrides in isolated work folders."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assignment-template'
WORK = ROOT / 'tmp' / 'template-checks'
REPORT = ROOT / 'output' / 'qa' / 'template-check.json'


def check_case(name, overrides):
    project = WORK / name
    project.mkdir(parents=True, exist_ok=True)
    for source in SOURCE.rglob('*'):
        relative = source.relative_to(SOURCE)
        if any(p in {'build', 'tmp', '__pycache__'} or p.startswith(('.venv', '_minted')) or p.endswith('.egg-info') for p in relative.parts):
            continue
        if source.is_file():
            destination = project / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    base_document = 'example.tex' if name == 'unicode-math' else 'main.tex'
    text = (project / base_document).read_text(encoding='utf-8')
    definitions = '\n'.join('\\def\\' + key + '{' + value + '}' for key, value in overrides.items())
    text = text.replace(r'\input{settings}', definitions + '\n' + r'\input{settings}', 1)
    text = text.replace(r'\MakeAssignmentTitle', r'''\MakeAssignmentTitle
\begin{notebox}[آزمون رنگ و جهت متن]
  این کادر، تم سند و شکل درست متن فارسی را نشان می‌دهد؛ رابطهٔ \(x+y=3\) و کد \codeinline{file_name.py} هم در همین سطر قرار دارند.
\end{notebox}''', 1)
    (project / 'main.tex').write_text(text, encoding='utf-8')
    temp = project / 'tmp'
    temp.mkdir(exist_ok=True)
    env = dict(os.environ, TEMP=str(temp), TMP=str(temp), LC_ALL='C', LANG='C')
    arguments = ['latexmk', '-xelatex', '-shell-escape', '-synctex=1', '-interaction=nonstopmode',
                 '-file-line-error', '-halt-on-error', '-outdir=build', 'main.tex']
    print(f'Started {name}', flush=True)
    with (project / 'console.txt').open('w', encoding='utf-8') as stream:
        result = subprocess.run(arguments, cwd=project, env=env, stdout=stream, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f'{name} failed; inspect {project / "console.txt"}')
    log = (project / 'build/main.log').read_text(encoding='utf-8', errors='replace')
    issues = [line for line in log.splitlines() if re.search(r'Overfull|Missing character|LaTeX Warning:|Package .* Warning:|^!', line)]
    if issues:
        raise RuntimeError(f'{name}: {issues}')
    info = subprocess.run(['pdfinfo', str(project / 'build/main.pdf')], check=True, capture_output=True, text=True).stdout
    pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M)[1])
    font_info = subprocess.run(['pdffonts', str(project / 'build/main.pdf')], check=True, capture_output=True, text=True).stdout
    if any(line.split()[-5] != 'yes' for line in font_info.splitlines()[2:] if line.strip()):
        raise RuntimeError(f'Unembedded font in {name}')
    if name == 'font-overrides' and 'size12.clo' not in log:
        raise RuntimeError('The configured base size was not applied')
    if name == 'unicode-math' and 'unicode-math.sty' not in log:
        raise RuntimeError('The configured math font was not applied')
    print(f'Passed {name}: {pages} pages', flush=True)
    return {'name': name, 'pages': pages, 'pdf': str(project / 'build/main.pdf'), 'overrides': overrides, 'warnings': issues}


def main():
    cases = {theme: {'AssignmentTheme': theme} for theme in ('warm', 'blue', 'green', 'plum', 'teal')}
    cases['font-overrides'] = {
        'AssignmentTheme': 'blue', 'AssignmentBaseSize': '12pt',
        'AssignmentLatinFont': 'TeX Gyre Pagella', 'AssignmentCodeFont': 'Consolas',
        'AssignmentCodeScale': '1', 'AssignmentCodeSize': r'\footnotesize',
        'AssignmentLineSpacing': '1.35', 'AssignmentTitleSize': '30',
    }
    cases['unicode-math'] = {'AssignmentTheme': 'green', 'AssignmentMathFont': 'Latin Modern Math'}
    results = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(check_case, name, overrides) for name, overrides in cases.items()]
        for future in as_completed(futures):
            results.append(future.result())
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(sorted(results, key=lambda item: item['name']), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'All {len(results)} cases passed: {REPORT}')


if __name__ == '__main__':
    main()
