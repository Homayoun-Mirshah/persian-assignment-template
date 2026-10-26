# Sources and installed dependencies

Third-party LaTeX and Python packages are loaded from the system, rather than
redistributed in this project. On the reviewed Windows machine, unmodified
minted 3.8.0, fvextra 1.14.0, and latex2pydata 0.7.0 are registered in
`TEXMFLOCAL`, together with their `.dtx` sources and license notices.
XePersian, TikZ/PGFPlots, tcolorbox, and other standard dependencies come from
TeX Live 2025. Python dependencies are listed in `requirements.txt`.

- [minted](https://ctan.org/pkg/minted), LPPL 1.3c / LPPL 1.3 / BSD 3-Clause.
- [fvextra](https://ctan.org/pkg/fvextra), LPPL 1.3.
- [latex2pydata](https://ctan.org/pkg/latex2pydata), LPPL 1.3c.
- [Pygments](https://pygments.org/), BSD 2-Clause.
- [latexminted](https://github.com/gpoore/minted), LPPL 1.3c.

## Editable theme palettes

`themes/assignment_editorstyles.py` maps standard Pygments token classes to
these primary palette sources. It does not run IDE semantic services.

- [JetBrains Default and Darcula](https://github.com/JetBrains/intellij-community/blob/master/platform/platform-resources/src/DefaultColorSchemesManager.xml).
- [Microsoft Dark+](https://github.com/microsoft/vscode/blob/main/extensions/theme-defaults/themes/dark_plus.json)
  and [Dark](https://github.com/microsoft/vscode/blob/main/extensions/theme-defaults/themes/dark_vs.json).
- [MathWorks light theme settings](https://www.mathworks.com/help/matlab/ref/matlab.colors-settings.html):
  keyword [14,0,255], string [170,4,249], comment [2,128,9].

The PDF toolbar and gutter are a template layout. Darcula line numbers use a
lighter gray for small text. PyCharm aliases reuse the JetBrains palette.
Names identify the appearance; this template is not endorsed by the vendors.

## Original institutional logos

The PNG files were obtained unchanged from the official sites on 2026-10-10.

| Project asset | Original source |
| --- | --- |
| `assets/aut-logo.png` | [Amirkabir University of Technology](https://aut.ac.ir/templates/tmpl_modern01/images/logo_fa.png) |
| `assets/bme-logo.png` | [Biomedical Engineering Faculty](https://bme.aut.ac.ir/files/bme/site/logo_fa.png) |

The university mark is navy and the faculty mark is white with transparent
backgrounds. The template displays the latter on a navy card. These identity
marks remain subject to their owners' rights.
