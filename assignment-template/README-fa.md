# قالب فارسی تمرین‌های دانشگاهی

قالب A4 با XePersian، فونت فارسی Vazirmatn، فونت لاتین Lora و کدهای چپ‌به‌راست با JetBrains Mono. صفحهٔ عنوان، فرمول و اثبات، نمودار برداری، کد با انتخاب زبان و تم، و بلوک‌دیاگرام آماده‌اند.

## شروع سریع

1. کل پوشهٔ قالب را برای تمرین جدید کپی کنید.
2. مشخصات را در `metadata.tex` و صورت سؤال و پاسخ‌ها را در `main.tex` تغییر دهید.
3. ‏`main.tex` را در TeXstudio باز کنید و **F5** بزنید؛ یا `build.cmd` را اجرا کنید.

در همین سیستم، بسته‌های مورد نیاز و فونت‌ها آماده‌اند و کپی پوشه به محل دیگر نیاز به نصب مجدد ندارد. PDFها و همهٔ فایل‌های کامپایل در تنها پوشهٔ تولیدی `build/` قرار می‌گیرند. فایل‌های اصلی را خارج از `build/` ویرایش کنید.

## ساختار سادهٔ پوشه

| فایل یا پوشه | کاربرد |
| --- | --- |
| `main.tex` | نقطهٔ شروع پاسخ‌نویسی؛ چهار نمونهٔ کوتاه آماده |
| `metadata.tex` | نام درس، تمرین، دانشجو، استاد درس، دانشگاه و دانشکده |
| `example.tex` | نمونهٔ کامل و یکپارچهٔ ریاضی، نمودار، کد و دیاگرام |
| `code-demo.tex` | مقایسهٔ زبان‌ها، تم‌ها و کد درون‌خطی |
| `assignment.sty` | جلد، صفحه‌آرایی، رنگ‌ها و کادرهای گرم |
| `editor-code.sty` | تنظیمات قابل ویرایشِ کدهای بلوکی و درون‌خطی |
| `assets/` | دو لوگوی رسمی و فایل CSV نمودار نمونه |
| `examples/` | فایل‌های کوتاه Python، Java، MATLAB و LaTeX برای درج در سند |
| `tools/` | بررسی وابستگی‌ها، پاک‌سازی، ساخت ZIP، تنظیمات تم و گزارش بررسی |
| `build.cmd`، `build.ps1` | ساخت هر سه PDF با latexmk و XeLaTeX |

`vendor/`، کپی کتابخانه‌های Python و بسته‌های استاندارد LaTeX داخل قالب وجود ندارند. فایل‌های `assignment.sty` و `editor-code.sty` تنظیمات اختصاصی و قابل ویرایش خود قالب هستند.

## TeXstudio

هر سه سند اصلی در چند خط اول، فرمان کامپایل و نمایش PDF خود را دارند. فرمان کامپایل از **latexmk و XeLaTeX نصب‌شدهٔ سیستم** استفاده می‌کند، پوشهٔ `build/` را خودکار می‌سازد و ارجاع‌ها را تا تثبیت شماره‌ها تکرار می‌کند. مسیر نمایشگر داخلی هم صریحاً به PDF همان سند در `build/` اشاره می‌کند؛ به تغییر سراسری مسیر جست‌وجوی PDF نیاز نیست.

- برای پاسخ‌نویسی، `main.tex` را باز کنید؛ **F6** کامپایل و **F5** کامپایل و نمایش است.
- برای نمونهٔ کامل و گالری، فایل مربوط را باز کنید. اگر قبلاً یک Root Document ثابت انتخاب کرده‌اید، از `Options > Root Document` آن را آزاد کنید یا سند مورد نظر را انتخاب کنید.
- هنگام ویرایش `metadata.tex`، کامپایل به `main.tex` ارجاع داده می‌شود.
- فایل‌ها UTF-8 هستند. موتور سند XeLaTeX است و `shell-escape` برای هایلایت فعال می‌شود.
- پس از نصب اولیهٔ بسته‌های Python و تغییر PATH، TeXstudio را دوباره باز کنید تا مسیر فرمان‌های تازه را ببیند.
- اگر TeXstudio برای فرمان‌های معرفی‌شده در سند اجازه خواست، زنجیرهٔ کامپایل و نمایش، فرمان `latexmk` و مسیر PDF ابتدای همان سند را بررسی و برای این پروژه تأیید کنید.

این تنظیم‌ها از [magic commentهای رسمی TeXstudio](https://texstudio-org.github.io/advanced.html#advanced-header-usage) و [قواعد مسیرهای فرمان و نمایشگر](https://texstudio-org.github.io/configuration.html#command-syntax-in-detail) استفاده می‌کنند. استفاده از فایل batch یا محیط مجازی محلی برای TeXstudio لازم نیست.

از ترمینال، در پوشهٔ قالب:

```powershell
.\build.cmd
.\build.cmd -Target main
.\build.cmd -Target example
.\build.cmd -Target code-demo
```

خروجی‌ها به‌ترتیب `build/main.pdf`، `build/example.pdf` و `build/code-demo.pdf` هستند. این‌ها همان PDFهایی هستند که TeXstudio نمایش می‌دهد.

## بسته‌های نصب‌شده و انتقال

روی سیستم بررسی‌شده، TeX Live 2025 و Python 3.14 استفاده شده‌اند. نسخه‌های سازگار زیر خارج از پوشهٔ تمرین در دسترس‌اند:

| بخش | نسخه و محل |
| --- | --- |
| LaTeX | minted 3.8.0، fvextra 1.14.0، latex2pydata 0.7.0 در درخت مشترک `TEXMFLOCAL` |
| بسته‌های دیگر | XePersian، TikZ/PGFPlots، tcolorbox، latexmk و بسته‌های معمول از TeX Live |
| Python | latexminted 0.7.1، Pygments 2.19.2، latex2pydata 0.5.0 و latexrestricted 0.6.2 در نصب Python |
| تم‌ها | افزونهٔ اختصاصی `assignment-editorstyles` نسخهٔ 1.1.0 در Python |
| فونت‌ها | Vazirmatn، Lora و JetBrains Mono از نصب سیستم |

`TEXMFLOCAL` محل استاندارد افزودن بسته‌های مشترک به TeX Live است. فایل‌های اصلی TeX Live 2025 دستکاری نشده‌اند؛ بسته‌های جدیدتر در این درخت بر نسخه‌های قدیمی اولویت دارند. چون این نصبِ افزوده مستقل از فهرست tlmgr است، محل فایل واقعی را با `kpsewhich minted.sty` بررسی کنید. [راهنمای رسمی نصب بسته‌ها در TEXMFLOCAL](https://tug.org/texlive/doc/texlive-en/texlive-en.html)

برای انتقال به **پوشه‌ای دیگر روی همین سیستم**، فقط کل قالب را کپی کنید. برای **کامپیوتری دیگر**، یک‌بار TeX و Python و فونت‌ها و نسخه‌های سازگار بسته‌ها را نصب کنید. در یک TeX Live به‌روز، بسته‌های LaTeX با tlmgr نصب یا به‌روز می‌شوند؛ در نسخهٔ قدیمی، بسته‌های سازگار CTAN را در `TEXMFLOCAL/tex/latex/<package>/` و منابعشان را در `TEXMFLOCAL/source/latex/<package>/` قرار دهید و `mktexlsr` را اجرا کنید. نسخه‌های لازم و منابع رسمی در `tools/SOURCES.md` آمده‌اند.

وابستگی‌های Python و تم اختصاصی یک‌بار با Python مورد استفادهٔ TeX نصب می‌شوند:

```powershell
python -m pip install -r tools/requirements.txt ./tools/themes
python tools/project.py check
```

مسیر `Scripts` همین Python باید در PATH باشد تا فرمان `latexminted` از TeX قابل اجرا باشد؛ روی سیستم حاضر تنظیم شده است. هنگام ساخت PDF هیچ دانلود یا نصب pip انجام نمی‌شود. مجوزها و منابع لوگوها و پالت‌ها در `tools/SOURCES.md` ثبت شده‌اند.

## سؤال، پاسخ و نتیجه

```latex
\begin{problem}[۲۰ نمره]{عنوان سؤال}\label{prob:one}
  صورت سؤال و فرض‌های مسئله.
\end{problem}
\begin{solution}
  \Part{بخش اول}
  مراحل حل.
  \begin{answerbox}
    پاسخ نهایی همراه واحد و شرایط اعتبار.
  \end{answerbox}
\end{solution}
\begin{notebox}[نکته]
  توضیح تکمیلی.
\end{notebox}
```

شمارهٔ تمرین‌ها خودکار است؛ برای شروع از ۵، پیش از سؤال اول `\setcounter{problem}{4}` را قرار دهید. کادرها در صفحهٔ بعد قابل ادامه‌اند. جلد شماره ندارد و صفحات متن از ۱ شمرده می‌شوند. فهرست اختیاری با `\tableofcontents` پس از جلد اضافه می‌شود.

## ریاضی، نمودار و دیاگرام

محیط‌های `equation`، `align`، `cases`، `bmatrix`، `theorem`، `lemma`، `definition` و `proof` آماده‌اند. برای ارجاع چپ‌به‌راست از `\eqnref{eq:name}` استفاده کنید. شمارهٔ رابطه از شمارهٔ تمرین پیروی می‌کند. اعداد ریاضی لاتین‌اند.

```latex
\begin{equation}\label{eq:sample}
  \mat{A}\vect{x}=\vect{b},\qquad
  \norm{\vect{x}}_2=\sqrt{13}.
\end{equation}
طبق رابطهٔ \eqnref{eq:sample}، ...
```

فرمان‌های `\R`، `\N`، `\E`، `\vect`، `\mat`، `\dd`، `\abs`، `\norm`، `\inner`، `\argmin` و `\argmax` وجود دارند. صورت ستاره‌دار `\norm*{...}` اندازهٔ علامت‌ها را خودکار می‌کند.

نمودارها با PGFPlots و دیاگرام‌ها با TikZ ساخته می‌شوند. نمونهٔ کامل در `example.tex` قرار دارد؛ دادهٔ نمودار در `assets/convergence.csv` است. محیط‌های `plotarea` و `diagramarea` جهت مختصات را چپ‌به‌راست نگه می‌دارند؛ برچسب فارسی داخلشان با `\rl{...}` نوشته می‌شود. سبک‌های `assignment axis`، `assignment block`، `assignment io`، `assignment decision`، `assignment sum` و `assignment arrow` آماده‌اند.

## کدهای بلوکی

```latex
\begin{codeblock}[theme=vscode-dark]{Python}{عنوان فارسی کد}
def square(x):
    return x ** 2
\end{codeblock}

\CodeFile{Python}{عنوان کد}{examples/gradient_descent.py}
```

نام زبان صریح است و از aliasهای Pygments می‌آید؛ مانند `Python`، `Java`، `MATLAB`، `C++`، `JavaScript`، `SQL` یا `bash`. انتخاب زبان و تم مستقل است. هایلایت واژگانی است و تحلیل معنایی IDE را اجرا نمی‌کند.

تم‌های `darcula`، `intellij-light`، `vscode-dark` و `matlab-light` آماده‌اند؛ `pycharm-darcula` و `pycharm-light` نیز نام‌های جایگزین‌اند. پیش‌فرض عمومی Darcula و پیش‌فرض MATLAB روشن است. در `metadata.tex`:

```latex
\SetCodeDefaultTheme{darcula}
\SetCodeLanguageTheme{Python}{vscode-dark}
\SetCodeLanguageTheme{MATLAB}{matlab-light}
```

انتخاب `theme` برای هر بلوک اولویت دارد. گزینه‌های `firstline`، `lastline`، `firstnumber`، `numbers=none` و `fontsize` نیز پشتیبانی می‌شوند. گزینه‌های دیگر minted داخل `minted={...}` قرار می‌گیرند. کدهای بلند در صفحات بعد ادامه دارند.

## کد درون‌خطی

برای نام فایل، متغیر یا قطعهٔ کوتاه کد از `\codeinline` استفاده کنید. متن داخل یک کادر جمع‌وجور با زمینهٔ خاکستری خیلی روشن، حاشیهٔ ظریف و گوشه‌های نرم می‌نشیند. فونت JetBrains Mono همان فونت کدبلاک‌هاست؛ جهت کد چپ‌به‌راست و رنگ تمام نویسه‌ها یکسان است. انتخاب زبان یا تم برای کد درون‌خطی لازم نیست.

```latex
فایل \codeinline{file_name.py} و متغیر \codeinline{sample_count}.
تابع \codeinline{len(values)} تعداد عضوها را می‌دهد.
محاسبهٔ \codeinline{Math.sqrt(4.0)} در همین سطر قرار می‌گیرد.
```

برای نویسه‌های ویژه هم می‌توانید کد را میان دو جداکنندهٔ یکسان قرار دهید؛ `%`، `#`، `_` و بک‌اسلش به‌صورت مستقیم خوانده می‌شوند:

```latex
\codeinline|a_b = 50% + #x|
\codeinline|A \ b|
```

اگر کد خودش `|` دارد، جداکنندهٔ دیگری مثل `!` انتخاب کنید. از این فرمان برای قطعه‌های کوتاه در متن عادی استفاده کنید؛ قطعهٔ کد داخل کادر در چند خط شکسته نمی‌شود. متن فارسی را بیرون کد بنویسید. فرمان قدیمی `\CodeInline` برای سازگاری پذیرفته می‌شود و همین ظاهر خنثی را دارد؛ زبان و تم قبلی بر ظاهر inline اثری ندارند.

رنگ‌های `ECInlineBackground`، `ECInlineBorder` و `ECInlineForeground` و سبک `editor inline` در `editor-code.sty` فقط ظاهر درون‌خطی را کنترل می‌کنند. رنگ‌بندی کدبلاک‌ها مستقل است.

## شخصی‌سازی و نگهداری

- نام دانشگاه و دانشکده زیر لوگوها از `metadata.tex` خوانده می‌شود؛ برچسب استاد، «استاد درس» است.
- رنگ‌های سند و کادرهای گرم، حاشیه‌ها و سایه در `assignment.sty` قرار دارند؛ با حذف `drop fuzzy shadow` سایه برداشته می‌شود.
- رنگ و قاب کدها در `editor-code.sty` مستقل‌اند. پالت‌های Pygments در `tools/themes/assignment_editorstyles.py` قابل ویرایش‌اند. پس از تغییر پالت، `python tools/project.py install-themes` را اجرا کنید و cache قبلی را با فرمان پاک‌سازی زیر حذف کنید.
- بسته‌های اضافی LaTeX باید در `assignment.sty`، پیش از XePersian بارگذاری شوند.

```powershell
python tools/project.py check
python tools/project.py clean
python tools/project.py package
```

پاک‌سازی فقط فایل‌ها و پوشه‌های تولیدی پروژه را حذف می‌کند؛ ابتدا PDF مورد نیاز را از `build/` به محل تحویل خود کپی کنید. ZIP فقط منابع و تنظیمات را شامل می‌شود و `build/`، فونت، محیط مجازی یا کپی بسته‌های نصب‌شده در آن قرار نمی‌گیرند. نتیجهٔ بررسی نسخهٔ حاضر در `tools/VALIDATION.md` ثبت می‌شود.
