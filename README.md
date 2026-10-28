# Persian assignment template

An A4 XeLaTeX/XePersian template for Persian university assignments, with a title
page, math and proofs, plots, highlighted code, inline code, and block diagrams.

## Get started

1. Copy `assignment-template/` into a folder for your assignment.
2. Edit course and student details in `metadata.tex`, appearance in `settings.tex`,
   and questions and answers in `main.tex`.
3. Open `main.tex` in TeXstudio and press F5, or run `build.cmd -Target main`.
   The PDF appears in `build/main.pdf`.

The template needs TeX Live with XeLaTeX and latexmk, Python, and the default
Vazirmatn, Lora, and JetBrains Mono fonts. See the
[user guide](assignment-template/README.md) for dependency setup and customization.
You can also open [README.html](assignment-template/README.html) locally in a browser.

## Downloads

[Releases](https://github.com/Homayoun-Mirshah/persian-assignment-template/releases)
include sample PDFs and two ZIPs:

- `persian-assignment-template.zip` uses system fonts and dependencies.
- `persian-assignment-template-bundled.zip` includes fonts, Python packages, and
  supplementary LaTeX packages for offline setup on Windows. After extracting it,
  run `setup.cmd` once. TeX Live and a base Python installation are still required.
