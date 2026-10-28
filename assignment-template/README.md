# Persian assignment template

An A4 XeLaTeX/XePersian template for Persian university assignments. It includes
a title page, question and solution boxes, math and proofs, PGFPlots charts,
highlighted code, and TikZ block diagrams.

## Quick start

1. Copy the whole template folder for each new assignment.
2. Set course, student, instructor, and logo details in `metadata.tex`.
3. Choose colors and fonts in `settings.tex`, then write in `main.tex`.
4. Open `main.tex` in TeXstudio and press F5, or run:

```powershell
.\build.cmd -Target main
```

The PDF is saved to `build/main.pdf`. Run `build.cmd` without a target to compile
all three documents. In TeXstudio, F6 compiles the current document and F5 also
opens its PDF. On first use, TeXstudio may ask you to approve the compile command
stored at the top of the file.

## Requirements

- TeX Live with XeLaTeX, latexmk, XePersian, TikZ/PGFPlots, and tcolorbox.
  The code module needs minted 3.8.0 or later, fvextra 1.14.0 or later, and the
  LaTeX package latex2pydata 0.7.0 or later.
- Python with the packages in `tools/requirements.txt` and the included code themes.
- The default fonts: Vazirmatn, Lora, and JetBrains Mono.

For the lightweight edition, install the Python dependencies once:

```powershell
python -m pip install -r tools/requirements.txt ./tools/themes
python tools/project.py check
```

The Python `Scripts` directory must be on PATH so TeX can find `latexminted`.
Restart TeXstudio after changing PATH. The template enables `shell-escape` for
code highlighting and uses XeLaTeX. Package sources and licenses are listed in
[tools/SOURCES.md](tools/SOURCES.md).

The bundled Windows edition includes the default fonts, Python packages, and
the three supplementary LaTeX packages. Run `setup.cmd` once after copying or
extracting it. Setup works offline using the included files; TeX Live and base
Python are still required.

## Files

| File | Purpose |
| --- | --- |
| `main.tex` | Starting point for an assignment |
| `metadata.tex` | Course, assignment, student, instructor, and title-page details |
| `settings.tex` | Document colors, fonts, sizes, and spacing |
| `example.tex` | Complete examples of math, plots, code, and diagrams |
| `code-demo.tex` | Code languages, themes, and inline-code examples |
| `assets/` and `examples/` | Logos, plot data, and external code samples |
| `build/` | Generated PDFs and compilation files |

## Appearance

Choose a document palette in `settings.tex`:

```latex
\providecommand{\AssignmentTheme}{warm}
```

Available palettes are `warm` (brown and cream, the default), `blue`, `green`,
`plum`, and `teal`. They apply to the title page, links, boxes, plots, and diagrams.
The page stays white. Code-block themes and neutral gray inline code have
separate colors.

Edit the existing font and size settings in the same file:

```latex
\providecommand{\AssignmentBaseSize}{12pt}
\providecommand{\AssignmentPersianFont}{Vazirmatn}
\providecommand{\AssignmentPersianBoldFont}{Vazirmatn Bold}
\providecommand{\AssignmentLatinFont}{Lora}
\providecommand{\AssignmentCodeFont}{JetBrains Mono}
\providecommand{\AssignmentLineSpacing}{1.3}
\providecommand{\AssignmentCodeScale}{.88}
\providecommand{\AssignmentCodeSize}{\footnotesize}
```

Base sizes are `10pt`, `11pt`, and `12pt`. Change both Persian font names when
switching families. Title, caption, header, footer, and code sizes have their own
settings. Edit existing definitions; adding another `\providecommand` for the
same setting will not override it.

Math uses Computer Modern by default. Set `AssignmentMathFont` to an available
OpenType math family, such as `Latin Modern Math`, to use unicode-math.
`AssignmentPersianItalicSlant` affects Persian text only.

The bundled edition reads its default fonts from `fonts/`. Set
`AssignmentFontSource` to `system` to use installed fonts. Other font families
must be available on the system.

To override a setting for one document, define it before loading `settings.tex`:

```latex
\def\AssignmentTheme{green}
\input{settings}
\documentclass[\AssignmentBaseSize,a4paper]{article}
\usepackage{assignment}
\input{metadata}
```

## Questions, math, and figures

Use `problem` for a question and `solution` for its answer. Put final results in
`answerbox` and notes in `notebox`. Question numbers are automatic, and the boxes
can continue across pages.

Standard math and proof environments are available, including `align`, `cases`,
`bmatrix`, `theorem`, and `proof`. Helpers include `\vect`, `\mat`, `\norm`, and
`\inner`; use `\eqnref{eq:name}` for equation references.

Wrap PGFPlots charts in `plotarea` and TikZ diagrams in `diagramarea` to keep
coordinates left to right. Use `\rl{...}` for Persian labels inside them.
See `example.tex` for complete examples and the available diagram styles.

## Code blocks

Set the language for each block and choose a theme when needed:

```latex
\begin{codeblock}[theme=vscode-dark]{Python}{Example}
def square(x):
    return x ** 2
\end{codeblock}

\CodeFile{Python}{Example}{examples/gradient_descent.py}
```

Languages use Pygments aliases, including `Python`, `Java`, `MATLAB`, `C++`,
`JavaScript`, `SQL`, and `bash`. Themes are `darcula`, `intellij-light`,
`vscode-dark`, and `matlab-light`; `pycharm-darcula` and `pycharm-light` are aliases
for the JetBrains themes. Highlighting uses Pygments tokens.

Set defaults with `AssignmentCodeTheme` and `AssignmentMatlabTheme` in
`settings.tex`. To choose a theme for one language, add this after loading the
template, for example in `metadata.tex`:

```latex
\SetCodeDefaultTheme{darcula}
\SetCodeLanguageTheme{Python}{vscode-dark}
\SetCodeLanguageTheme{MATLAB}{matlab-light}
```

A block's `theme` option takes priority. Other options include `firstline`,
`lastline`, `firstnumber`, `numbers=none`, and `fontsize`. Pass additional minted
options through `minted={...}`.

## Inline code

Use `\codeinline` for short snippets in running text:

```latex
\codeinline{file_name.py}
\codeinline{len(values)}
\codeinline|a_b = 50% + #x|
\codeinline|A \ b|
```

Inline code uses the same monospaced font as code blocks, inside a small
light-gray box with rounded corners. It is left to right and has no syntax
highlighting. Use matching delimiters, such as `|` or `!`, for snippets containing
special characters. Keep snippets short; they do not wrap across lines.
