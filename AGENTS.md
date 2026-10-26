# Project workflow

- `assignment-template/` is the editable source of truth. Read its README before changing the template.
- Keep user-facing Persian documentation clear and correctly rendered right to left. Regenerate the HTML README whenever its Markdown source changes.
- Keep document palettes independent of code-block themes and neutral inline-code styling.
- Keep font and per-document appearance choices in `settings.tex`; preserve default mathematical typography unless explicitly configured otherwise.
- `assignment-template-bundled/` and `output/` are generated deliverables. Rebuild them from the canonical source; do not hand-edit generated copies.
- Preserve `references/`; these are the user's historical reference files.
- Verify meaningful template changes with XeLaTeX/latexmk, inspect relevant PDF pages, and check a fresh extracted package before delivery.
- Never commit build caches, virtual environments, downloaded dependency payloads, credentials, or local reference archives.
- The user requests Git history for significant changes: make focused commits after each coherent, verified change. Use a feature branch for experimental or extended work; do not rewrite published or user-authored history, and do not force-push.
- This repository is public. Keep sample metadata generic; preserve personal defaults only in ignored local references.
