"""Build the self-contained English HTML guide from README.md."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

CSS = r"""
:root{color-scheme:light;--ink:#302b28;--muted:#746a62;--accent:#8b4528;--line:#e5d7cc;--paper:#fff;--wash:#f7f3ef;--radius:16px}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:28px}body{margin:0;background:var(--wash);color:var(--ink);font:16px/1.65 system-ui,'Segoe UI',sans-serif}
a{color:#854025;text-decoration-thickness:1px;text-underline-offset:4px}a:hover{color:#4e2415}button{font:inherit;cursor:pointer}code,pre,kbd{font-family:'JetBrains Mono',Consolas,monospace}
.hero{background:#302b28;color:#fff8f0;padding:32px max(28px,calc((100vw - 1200px)/2));border-bottom:5px solid #c58b59}.hero h1{font-size:clamp(27px,4.2vw,41px);margin:0;line-height:1.4}
.layout{max-width:1260px;margin:30px auto;display:grid;grid-template-columns:260px minmax(0,1fr);gap:24px;padding:0 24px;align-items:start}.sidebar{position:sticky;top:22px;background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);padding:20px;font-size:13px;max-height:calc(100vh - 44px);overflow:auto}.sidebar h2{font-size:15px;margin:0 0 12px}.sidebar ul{list-style:none;padding:0;margin:0}.sidebar li{margin:7px 0}.sidebar a{display:block;text-decoration:none;color:#62574e}.sidebar a:hover{color:var(--accent)}.sidebar>p{padding-top:16px;border-top:1px solid var(--line);font-size:12px}
main{min-width:0;background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);padding:30px 36px;box-shadow:0 8px 30px #302b2808}article>h1{display:none}h2{font-size:23px;margin:36px 0 13px;padding-bottom:10px;border-bottom:1px solid var(--line)}h3{font-size:18px;margin-top:28px}p{margin:14px 0}li{margin:5px 0}ul,ol{padding-inline-start:25px;padding-inline-end:0}strong{font-weight:700}
code{direction:ltr;unicode-bidi:isolate;display:inline-block;font-size:.86em;background:#f0f1f2;border:1px solid #e3e5e7;border-radius:5px;padding:0 .32em;line-height:1.7;overflow-wrap:anywhere}pre{position:relative;direction:ltr;text-align:left;unicode-bidi:isolate;background:#262829;color:#e8ebee;border-radius:12px;padding:22px 18px;margin:18px 0;overflow:auto;font-size:13px;line-height:1.8;tab-size:4}pre code{display:block;font-size:inherit;background:none;border:0;color:inherit;padding:0;white-space:pre;overflow-wrap:normal;line-height:inherit}.copy{position:absolute;right:8px;top:7px;background:#3b3e40;color:#f8f8f8;border:1px solid #5b6063;border-radius:5px;font-size:11px;padding:1px 8px}
.table-scroll{overflow-x:auto;border:1px solid var(--line);border-radius:10px;margin:18px 0}table{border-collapse:collapse;width:100%;min-width:460px;font-size:14px}th{background:#f5ece4;color:#5b3b29;text-align:start;font-weight:700}th,td{padding:12px 15px;border-bottom:1px solid #ece4de;vertical-align:top}tr:last-child td{border-bottom:0}tr:nth-child(even) td{background:#fcfaf8}blockquote{border-inline-start:4px solid #c58b59;margin:18px 0;padding:1px 20px;background:#fff7ef}
.theme-lab{border:1px solid var(--line);background:#fcfaf8;border-radius:14px;padding:20px;margin:24px 0}.theme-buttons{display:flex;flex-wrap:wrap;gap:8px}.theme-button{border:1px solid #d8d0c9;background:#fff;border-radius:9px;padding:8px 11px;display:flex;align-items:center;gap:7px;font-size:13px}.theme-button[aria-pressed=true]{outline:2px solid var(--ink);outline-offset:1px}.swatch{width:17px;height:17px;background:var(--swatch);border-radius:50%;display:inline-block}.preview{margin:20px 0 0;--title:#8b4528;--border:#b57448;--back:#fff5e7;--result:#f8e0b9;--note:#e4be95;--ink:#302b28;--shadow:#b6a493;color:var(--ink)}.preview-question{border:1px solid var(--border);border-radius:9px;overflow:hidden;box-shadow:3px 4px 7px color-mix(in srgb,var(--shadow) 50%,transparent)}.preview-title{background:var(--title);color:white;padding:7px 13px;font-size:14px;font-weight:700}.preview-body{background:var(--back);padding:12px 14px;font-size:14px}.preview-answer{background:var(--result);border-inline-start:3px solid var(--title);border-radius:6px;padding:8px 13px;margin-top:12px;font-size:14px}.preview-note{background:var(--note);padding:6px 12px;margin-top:10px;font-size:12px;border-radius:5px}
@media(max-width:900px){.layout{grid-template-columns:1fr;max-width:850px}.sidebar{position:static;max-height:none}.sidebar .toc ul{display:flex;gap:6px 16px;flex-wrap:wrap}.sidebar li{margin:0}.sidebar>p{display:none}main{padding:24px}.hero{padding:32px 24px}.hero h1{font-size:29px}}@media(max-width:520px){body{font-size:15px}.layout{padding:0 10px;gap:14px;margin:14px auto}main{padding:20px 16px}.sidebar{padding:14px}h2{font-size:21px}.theme-lab{padding:14px}.theme-button{padding:7px 9px}pre{font-size:12px}.hero{padding:28px 18px}}@media print{body{background:white;font-size:11pt}.hero{background:white;color:black;border-bottom:2px solid #888;padding:12px}.sidebar,.theme-lab,.copy{display:none}.layout{display:block;padding:0;margin:0}main{border:0;box-shadow:none;padding:0}pre{white-space:pre-wrap;background:#f5f5f5;color:black}h2{break-after:avoid}.table-scroll{overflow:visible}table{min-width:0}a{color:inherit}}
"""

LAB = r"""
<section class="theme-lab" aria-label="Document palette preview">
  <div class="theme-buttons" role="group" aria-label="Document palette">
    <button class="theme-button" data-theme="warm" aria-pressed="true"><span class="swatch" style="--swatch:#8b4528"></span>warm</button>
    <button class="theme-button" data-theme="blue" aria-pressed="false"><span class="swatch" style="--swatch:#244f7a"></span>blue</button>
    <button class="theme-button" data-theme="green" aria-pressed="false"><span class="swatch" style="--swatch:#315f42"></span>green</button>
    <button class="theme-button" data-theme="plum" aria-pressed="false"><span class="swatch" style="--swatch:#6b3d6c"></span>plum</button>
    <button class="theme-button" data-theme="teal" aria-pressed="false"><span class="swatch" style="--swatch:#245d60"></span>teal</button>
  </div>
  <div class="preview" id="theme-preview">
    <div class="preview-question"><div class="preview-title">Question 1</div><div class="preview-body">Find the derivative of f(x) = x².</div></div>
    <div class="preview-answer">Answer: f′(x) = 2x</div>
    <div class="preview-note">Note: code colors are independent of the document palette.</div>
  </div>
</section>
"""

JS = r"""
const palettes={warm:['#8b4528','#b57448','#fff5e7','#f8e0b9','#e4be95','#302b28','#b6a493'],blue:['#244f7a','#6b9fc9','#edf5fd','#d4e8fa','#bcd7ee','#202f40','#9cafc2'],green:['#315f42','#73a47d','#eff7ec','#d9ebcf','#bcd7b3','#24362e','#a0b3a0'],plum:['#6b3d6c','#ab7ab0','#f8edf8','#ead4ed','#d8b8dd','#382c3c','#b3a1b7'],teal:['#245d60','#69a7a8','#edf8f6','#cfeae5','#b2d7d1','#233839','#9db7b3']};
document.querySelectorAll('[data-theme]').forEach(button=>button.addEventListener('click',()=>{const id=button.dataset.theme;const keys=['title','border','back','result','note','ink','shadow'];keys.forEach((key,i)=>document.getElementById('theme-preview').style.setProperty('--'+key,palettes[id][i]));document.querySelectorAll('[data-theme]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));document.getElementById('theme-setting').textContent='\\providecommand{\\AssignmentTheme}{'+id+'}';}));
document.querySelectorAll('pre').forEach(pre=>{const button=document.createElement('button');button.type='button';button.className='copy';button.textContent='Copy';button.setAttribute('aria-label','Copy code');button.addEventListener('click',async()=>{const value=pre.querySelector('code').textContent;try{if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(value);}else{const area=document.createElement('textarea');area.value=value;area.style.position='fixed';area.style.opacity='0';document.body.append(area);area.select();const ok=document.execCommand('copy');area.remove();if(!ok)throw new Error('copy');}button.textContent='Copied';}catch{const selection=window.getSelection();const range=document.createRange();range.selectNodeContents(pre.querySelector('code'));selection.removeAllRanges();selection.addRange(range);button.textContent='Ctrl+C';}setTimeout(()=>button.textContent='Copy',1800);});pre.append(button);});
"""


def render():
    try:
        import markdown
        from markdown.extensions.toc import slugify_unicode
    except ImportError:
        sys.exit('Install documentation tooling: python -m pip install -r tools/requirements-docs.txt')
    source = (ROOT / 'README.md').read_text(encoding='utf-8')
    md = markdown.Markdown(
        extensions=['fenced_code', 'tables', 'toc', 'sane_lists'],
        extension_configs={'toc': {'slugify': slugify_unicode, 'toc_depth': '2-3'}},
    )
    body = md.convert(source)
    body = re.sub(r'(<table>.*?</table>)', r'<div class="table-scroll">\1</div>', body, flags=re.S)
    body = body.replace('<h2 id="appearance">Appearance</h2>', '<h2 id="appearance">Appearance</h2>' + LAB)
    body = body.replace('<code class="language-latex">\\providecommand{\\AssignmentTheme}{warm}',
                        '<code id="theme-setting" class="language-latex">\\providecommand{\\AssignmentTheme}{warm}', 1)
    page = f'''<!doctype html>
<html lang="en" dir="ltr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="A Persian assignment template with XePersian, math, plots, code, and diagrams.">
<title>Persian assignment template</title><style>{CSS}</style></head>
<body><header class="hero"><h1>Persian assignment template</h1></header>
<div class="layout"><aside class="sidebar"><h2>Contents</h2>{md.toc}<p><a href="README.md">Markdown version</a></p></aside>
<main><article>{body}</article></main></div>
<script>{JS}</script></body></html>'''
    output = ROOT / 'README.html'
    with output.open('w', encoding='utf-8', newline='\n') as stream:
        stream.write(page)
    print(f'Created {output} ({len(page.encode("utf-8")):,} bytes)')


if __name__ == '__main__':
    render()
