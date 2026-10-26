# Persian assignment template

An editable A4 XeLaTeX/XePersian template for Persian university exercises:
math and proofs, plots, language-aware highlighted code, neutral inline code,
and block diagrams.

**راهنمای فارسی و راست‌به‌چپ:**
[assignment-template/README.html](assignment-template/README.html)

Download or clone the repository and open that HTML file locally in a browser.
The source guide is [README-fa.md](assignment-template/README-fa.md).

- Start writing in `assignment-template/main.tex`.
- Edit course/student information in `metadata.tex`.
- Choose one of five document palettes and configure fonts/sizes in `settings.tex`.
- Run `assignment-template/build.cmd` or open a main document in TeXstudio.
- Build the dependency-inclusive sibling with `python tools/release.py`.

`assignment-template/` is the canonical, lightweight source. The generated
`assignment-template-bundled/` additionally contains local fonts, an installed
Python virtual environment, an offline wheelhouse, and compatible supplementary
LaTeX packages. It still uses the system's TeX Live/XeLaTeX and Python installation.
Its `setup.cmd` recreates the virtual environment offline after relocation.

Generated PDFs and ZIP packages are placed in `output/`. Build caches, virtual
environments, dependency downloads, and the user's historical `references/`
are intentionally excluded from Git. See [AGENTS.md](AGENTS.md) for the maintenance
and commit workflow.
