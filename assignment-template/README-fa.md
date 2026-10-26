# قالب فارسی تمرین‌های دانشگاهی

قالب A4 با XePersian، فونت فارسی Vazirmatn، فونت لاتین Lora و کدهای چپ‌به‌راست با JetBrains Mono. صفحهٔ عنوان، فرمول و اثبات، نمودار برداری، کد با انتخاب زبان و تم، و بلوک‌دیاگرام آماده‌اند.

نسخهٔ خواناترِ راست‌به‌چپ در **[README.html](README.html)** است؛ آن را مستقیماً با مرورگر باز کنید. همهٔ استایل‌ها داخل همان HTML هستند و برای خواندن راهنما به اینترنت نیازی نیست. Markdown منبع قابل ویرایش راهنما باقی می‌ماند.

## شروع سریع

1. کل پوشهٔ قالب را برای تمرین جدید کپی کنید.
2. مشخصات را در `metadata.tex`، رنگ و فونت‌ها را در `settings.tex` و صورت سؤال و پاسخ‌ها را در `main.tex` تغییر دهید.
3. ‏`main.tex` را در TeXstudio باز کنید و **F5** بزنید؛ یا `build.cmd` را اجرا کنید.

در همین سیستم، بسته‌های مورد نیاز و فونت‌ها آماده‌اند و کپی پوشه به محل دیگر نیاز به نصب مجدد ندارد. PDFها و همهٔ فایل‌های کامپایل در تنها پوشهٔ تولیدی `build/` قرار می‌گیرند. فایل‌های اصلی را خارج از `build/` ویرایش کنید.

## ساختار سادهٔ پوشه

| فایل یا پوشه | کاربرد |
| --- | --- |
| `main.tex` | نقطهٔ شروع پاسخ‌نویسی؛ چهار نمونهٔ کوتاه آماده |
| `metadata.tex` | نام درس، تمرین، دانشجو، استاد درس، دانشگاه و دانشکده |
| `settings.tex` | انتخاب تم سند و تنظیم یکپارچهٔ فونت، اندازه‌ها و فاصله‌ها |
| `example.tex` | نمونهٔ کامل و یکپارچهٔ ریاضی، نمودار، کد و دیاگرام |
| `code-demo.tex` | مقایسهٔ زبان‌ها، تم‌ها و کد درون‌خطی |
| `assignment.sty` | جلد، صفحه‌آرایی و محیط‌های سؤال و پاسخ |
| `assignment-themes.sty` | پالت‌های رنگ سند، نمودارها و کادرها |
| `assignment-fonts.sty` | اعمال تنظیمات مشترک فونت؛ تشخیص فونت‌های محلی یا سیستم |
| `editor-code.sty` | تنظیمات قابل ویرایشِ کدهای بلوکی و درون‌خطی |
| `assets/` | دو لوگوی رسمی و فایل CSV نمودار نمونه |
| `examples/` | فایل‌های کوتاه Python، Java، MATLAB و LaTeX برای درج در سند |
| `tools/` | بررسی وابستگی‌ها، پاک‌سازی، ساخت ZIP، تنظیمات تم و گزارش بررسی |
| `build.cmd`، `build.ps1` | ساخت هر سه PDF با latexmk و XeLaTeX |

`vendor/`، کپی کتابخانه‌های Python و بسته‌های استاندارد LaTeX داخل قالب وجود ندارند. فایل‌های `assignment.sty` و `editor-code.sty` تنظیمات اختصاصی و قابل ویرایش خود قالب هستند.

## انتخاب تم رنگی سند

در `settings.tex` فقط نام تم را عوض کنید:

```latex
\providecommand{\AssignmentTheme}{blue}
```

| نام | ظاهر |
| --- | --- |
| `warm` | قهوه‌ای و کرم؛ همان پیش‌فرض گرم قالب |
| `blue` | آبی سرمه‌ای، آبی میانی و آبی خیلی روشن |
| `green` | سبز جنگلی، سبز میانی و زمینهٔ سبز روشن |
| `plum` | بنفش آلویی و یاسی |
| `teal` | سبزآبی و فیروزه‌ای روشن |

انتخاب تم روی جلد، لینک‌ها، کادر سؤال، نتیجه و نکته، نمودار و بلوک‌دیاگرام اعمال می‌شود. زمینهٔ صفحه سفید می‌ماند و کادرها حاشیه و سایهٔ ملایم دارند. تم سند روی رنگ کدبلاک‌ها یا کادر خاکستریِ کد درون‌خطی اثری ندارد.

برای اینکه دو فایل در یک پوشه تم متفاوت داشته باشند، پیش از `\input{settings}` در همان فایل مقدار دلخواه را تعریف کنید. این روش برای همهٔ تنظیمات زیر هم کار می‌کند:

```latex
\def\AssignmentTheme{green}
\input{settings}
\documentclass[\AssignmentBaseSize,a4paper]{article}
\usepackage{assignment}
\input{metadata}
```

تعریف‌های `settings.tex` با `\providecommand` نوشته شده‌اند؛ بنابراین مقدارِ از قبل تعیین‌شدهٔ همان سند را بازنویسی نمی‌کنند. برای یک تمرین تازه که پوشهٔ جداگانه دارد، ویرایش خودِ `settings.tex` ساده‌تر است. پالت‌های رنگ در `assignment-themes.sty` قابل ویرایش‌اند؛ لوگوها رنگ اصلی خود را حفظ می‌کنند.

## تنظیم یکپارچهٔ فونت و اندازه

تمام انتخاب‌های روزمره در `settings.tex` هستند. اندازهٔ پایهٔ `article` یکی از `10pt`، `11pt` یا `12pt` است؛ با تغییرش، اندازه‌های نسبی مثل `\small` و اندازهٔ معمول فرمول‌ها هم متناسب تغییر می‌کنند. نمونه:

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

**خط‌های موجود را ویرایش کنید؛ تعریف تکراری با `providecommand` اضافه نکنید.** برای فونت فارسی دیگر، نام خانوادهٔ معمولی و ضخیم را با هم تغییر دهید. فونت انتخابی باید در سیستم نصب باشد یا طبق تنظیمات فونت محلی در دسترس باشد.

| تنظیم | کاربرد |
| --- | --- |
| `AssignmentBaseSize` | اندازهٔ پایهٔ متن و ریاضی |
| `AssignmentPersianFont` و `AssignmentPersianBoldFont` | خانوادهٔ متن فارسی و حالت ضخیم آن |
| `AssignmentLatinFont` و `AssignmentLatinScale` | فونت متن لاتین و ضریب اندازهٔ آن |
| `AssignmentLineSpacing` و `AssignmentParagraphSkip` | فاصلهٔ سطرها و پاراگراف‌ها |
| `AssignmentCodeFont` و `AssignmentCodeScale` | فونت مشترک کد بلوکی و درون‌خطی و ضریب اندازه |
| `AssignmentCodeSize` و `AssignmentCodeLineSpacing` | اندازه و فاصلهٔ سطر کدبلاک |
| `AssignmentInlineCodeSize` | مقدار خالی: هم‌اندازه با متن اطراف؛ یا مثلاً `\small` |
| `AssignmentCodeToolbarSize` و `AssignmentCodeNumberSize` | اندازهٔ نوار عنوان و شمارهٔ خط کد |
| `AssignmentTitleSize` و `AssignmentCourseSize` | اندازهٔ عددی بر حسب pt برای عنوان جلد و نام درس |
| `AssignmentStudentSize` و `AssignmentInstructorSize` | اندازهٔ عددی نام دانشجو و استاد روی جلد |
| `AssignmentHeaderSize` و `AssignmentFooterSize` | اندازهٔ سرصفحه و پاصفحه |
| `AssignmentCaptionSize` و `AssignmentDiagramSize` | اندازهٔ شرح شکل، برچسب نمودار و متن دیاگرام |
| `AssignmentPersianItalicSlant` | کجیِ ایتالیک متن فارسی؛ مستقل از فونت ریاضی |

پیش‌فرض `AssignmentMathFont` برابر `default` است: همان Computer Modern ریاضی، بدون کج‌کردن اضافه. اگر فونت OpenType ریاضی دیگری می‌خواهید، مثلاً مقدار `Latin Modern Math` را بگذارید؛ قالب در این حالت `unicode-math` را خودکار بارگذاری می‌کند. فونت منتخب باید در TeX یا سیستم در دسترس باشد. برای بولدِ بردار همچنان `\vect{x}` را به کار ببرید؛ این فرمان با هر دو حالت سازگار است.

در نسخهٔ دارای وابستگی‌ها، فونت‌های پیش‌فرض از `fonts/` خوانده می‌شوند و نصب سراسری لازم ندارند. مقدار `AssignmentFontSource` به‌طور پیش‌فرض `auto` است؛ `system` استفاده از نصب سیستم را اجبار می‌کند. انتخاب یک خانوادهٔ متفاوت، از فونت نصب‌شدهٔ همان خانواده استفاده می‌کند؛ فایل‌های همراه مربوط به Vazirmatn، Lora و JetBrains Mono هستند.

## TeXstudio

هر سه سند اصلی در چند خط اول، فرمان کامپایل و نمایش PDF خود را دارند. فرمان کامپایل از **latexmk و XeLaTeX نصب‌شدهٔ سیستم** استفاده می‌کند، پوشهٔ `build/` را خودکار می‌سازد و ارجاع‌ها را تا تثبیت شماره‌ها تکرار می‌کند. مسیر نمایشگر داخلی هم صریحاً به PDF همان سند در `build/` اشاره می‌کند؛ به تغییر سراسری مسیر جست‌وجوی PDF نیاز نیست.

- برای پاسخ‌نویسی، `main.tex` را باز کنید؛ **F6** کامپایل و **F5** کامپایل و نمایش است.
- برای نمونهٔ کامل و گالری، فایل مربوط را باز کنید. اگر قبلاً یک Root Document ثابت انتخاب کرده‌اید، از `Options > Root Document` آن را آزاد کنید یا سند مورد نظر را انتخاب کنید.
- هنگام ویرایش `metadata.tex`، کامپایل به `main.tex` ارجاع داده می‌شود.
- فایل‌ها UTF-8 هستند. موتور سند XeLaTeX است و `shell-escape` برای هایلایت فعال می‌شود.
- پس از نصب اولیهٔ بسته‌های Python و تغییر PATH، TeXstudio را دوباره باز کنید تا مسیر فرمان‌های تازه را ببیند.
- اگر TeXstudio برای فرمان‌های معرفی‌شده در سند اجازه خواست، زنجیرهٔ کامپایل و نمایش، فرمان `latexmk` و مسیر PDF ابتدای همان سند را بررسی کنید. `Yes to All` همان فرمان مشخص را برای کپی‌های بعدی هم مجاز می‌کند. در صورت انتخاب `Yes`، فایل را ذخیره کنید تا `document-id` اضافه‌شده باقی بماند. فرمان‌های `quick`، `compile` و `view` ممکن است بار اول جداگانه تأیید بخواهند.

این تنظیم‌ها از [magic commentهای رسمی TeXstudio](https://texstudio-org.github.io/advanced.html#advanced-header-usage) و [قواعد مسیرهای فرمان و نمایشگر](https://texstudio-org.github.io/configuration.html#command-syntax-in-detail) استفاده می‌کنند. فایل `.latexmkrc` محیط ساخت را آماده می‌کند؛ در نسخهٔ سبک از نصب سیستم و در نسخهٔ bundled از محیط محلی استفاده می‌شود.

از ترمینال، در پوشهٔ قالب:

```powershell
.\build.cmd
.\build.cmd -Target main
.\build.cmd -Target example
.\build.cmd -Target code-demo
```

خروجی‌ها به‌ترتیب `build/main.pdf`، `build/example.pdf` و `build/code-demo.pdf` هستند. این‌ها همان PDFهایی هستند که TeXstudio نمایش می‌دهد.

## بسته‌های نصب‌شده و انتقال

نسخهٔ سبکِ `assignment-template` از TeX Live و Python و فونت‌های سیستم استفاده می‌کند. روی سیستم بررسی‌شده، TeX Live 2025 و Python 3.14 در دسترس‌اند؛ نسخه‌های مورد نیاز:

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

مسیر `Scripts` همین Python باید در PATH باشد تا فرمان `latexminted` از TeX قابل اجرا باشد. روی Windows، `.latexmkrc` مسیرهای معمول Python نصب‌شدهٔ کاربر را هم بررسی می‌کند. هنگام ساخت عادی PDF دانلود یا نصب pip انجام نمی‌شود. مجوزها و منابع لوگوها و پالت‌ها در `tools/SOURCES.md` ثبت شده‌اند.

## نسخهٔ دارای وابستگی‌ها

پوشهٔ `assignment-template-bundled` کنار نسخهٔ سبک، همان منابع و تنظیمات را دارد و این موارد به آن اضافه شده‌اند:

- فونت‌های Vazirmatn، Lora و JetBrains Mono همراه مجوزهایشان در `fonts/`؛
- محیط مجازی `.venv` با بسته‌های Python و چهار تم اختصاصی نصب‌شده؛
- ابزارهای ساخت HTML راهنما و بازنصب آفلاینِ پالت‌های قابل ویرایش کد؛
- فایل‌های wheel برای نصب دوبارهٔ کاملاً آفلاین در `wheelhouse/`؛
- نسخه‌های سازگار minted، fvextra و latex2pydata همراه منابع و مجوزها در `texmf/`؛
- `setup.cmd` و `setup.ps1` برای آماده‌سازی یا بازسازی محیط پس از انتقال.

این نسخه همچنان به نصب TeX Live، XeLaTeX/latexmk و Python نیاز دارد؛ کپی کامل توزیع TeX یا نصب‌کنندهٔ Python نیست. بستهٔ آماده برای Windows است؛ wheelهای فعلی Python مستقل از پلتفرم‌اند، اما راه‌اندازهای Windows برای سیستم‌عامل دیگر باید معادل‌سازی شوند.

پس از کپی یا استخراج کل پوشه، یک‌بار `setup.cmd` را اجرا کنید و سپس `main.tex` را در TeXstudio باز کنید یا `build.cmd` را بزنید. راه‌انداز از فایل‌های همراه استفاده می‌کند و اینترنت لازم ندارد. برای انتخاب Python مشخص:

```powershell
.\setup.cmd -Python "C:\path\to\python.exe"
.\build.cmd -Target main
```

venv در Python به مسیر نصب پایه وابسته است و به‌خودی‌خود بستهٔ قابل انتقال محسوب نمی‌شود؛ به همین دلیل wheelها و راه‌انداز بازسازی هم همراه‌اند. اگر محیط محلی پس از جابه‌جایی قابل اجرا نباشد، wrapper کدها هم تلاش می‌کند آن را یک‌بار به‌صورت آفلاین آماده کند. [توضیح رسمی Python دربارهٔ انتقال venv](https://docs.python.org/3/library/venv.html)

پوشهٔ `build/` برای خروجی و cache است. نگه‌داشتنش حین ویرایش باعث می‌شود `latexmk` ساخت بدون تغییر را تکرار نکند. پیام‌های `Using bibtex` و بازگردانی code page ویندوز به‌تنهایی خطا نیستند؛ معیار موفقیت، کد خروج و پایان عادی فرایند است.

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

تم‌های `darcula`، `intellij-light`، `vscode-dark` و `matlab-light` آماده‌اند؛ `pycharm-darcula` و `pycharm-light` نیز نام‌های جایگزین‌اند. پیش‌فرض عمومی Darcula و پیش‌فرض MATLAB روشن است. برای پیش‌فرض‌ها در `settings.tex`:

```latex
\providecommand{\AssignmentCodeTheme}{darcula}
\providecommand{\AssignmentMatlabTheme}{matlab-light}
```

برای استثنای یک زبان یا یک سند، پس از بارگذاری قالب مثلاً در `metadata.tex`:

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
- انتخاب تم و فونت فقط در `settings.tex` است. پالت‌های رنگ در `assignment-themes.sty` و صفحه‌آرایی و سایه در `assignment.sty` قرار دارند؛ با حذف `drop fuzzy shadow` سایه برداشته می‌شود.
- رنگ و قاب کدها در `editor-code.sty` مستقل‌اند. پالت‌های Pygments در `tools/themes/assignment_editorstyles.py` قابل ویرایش‌اند. پس از تغییر پالت، `python tools/project.py install-themes` را اجرا کنید و cache قبلی را با فرمان پاک‌سازی زیر حذف کنید.
- بسته‌های اضافی LaTeX باید در `assignment.sty`، پیش از XePersian بارگذاری شوند.

```powershell
python tools/project.py check
python tools/project.py clean
python tools/project.py package
```

پاک‌سازی عادی فقط خروجی و cache ساخت را حذف می‌کند و محیط Python آمادهٔ bundled را نگه می‌دارد؛ ابتدا PDF مورد نیاز را از `build/` به محل تحویل خود کپی کنید. فرمان package نسخهٔ سبک، منابع و تنظیمات را بدون build یا وابستگی‌های سیستم بسته‌بندی می‌کند. برای ساخت نسخهٔ همراه وابستگی‌ها از ابزار انتشار در ریشهٔ مخزن استفاده می‌شود. نتیجهٔ بررسی نسخهٔ حاضر در `tools/VALIDATION.md` ثبت می‌شود.

## نگهداری README و گیت

پس از ویرایش این Markdown، نسخهٔ HTML را دوباره بسازید:

```powershell
python -m pip install -r tools/requirements-docs.txt
python tools/render_readme.py
```

در مخزن اصلی، `assignment-template/` منبع اصلی است و پوشهٔ bundled و ZIPها از آن تولید می‌شوند. فایل‌های ساخت، محیط مجازی، آرشیوهای قدیمی و وابستگی‌های دانلودشده وارد گیت نمی‌شوند. تغییرهای قابل توجه با کامیت مستقل ثبت می‌شوند؛ کارهای گسترده در شاخهٔ جدا انجام و پس از بررسی به شاخهٔ اصلی منتقل می‌شوند. فرمان ساخت بسته‌ها از ریشهٔ مخزن:

```powershell
python tools/release.py
```

این فرمان نسخهٔ سبک، پوشهٔ bundled، محیط آماده و ZIPهای متناظر را می‌سازد و سازگاری محتوای آرشیوها را بررسی می‌کند. تولید اولین wheelhouse به اینترنت نیاز دارد؛ استفاده و بازسازی محیطِ بستهٔ آماده آفلاین است.

در نسخهٔ bundled برای ساخت دوبارهٔ HTML می‌توانید از `.\.venv\Scripts\python.exe tools/render_readme.py` استفاده کنید. فرمان‌های `check` و `install-themes` نیز محیط محلیِ آماده را خودکار انتخاب می‌کنند. پس از تغییرِ فقط مستندات یا منابع قالب در مخزن، `python tools/release.py --refresh-source` نسخهٔ bundled و ZIPها را بدون نصب دوبارهٔ محیط موجود همگام می‌کند؛ برای تغییر وابستگی‌ها، ساخت کامل را اجرا کنید.
