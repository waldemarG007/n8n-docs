import os
import subprocess
from pathlib import Path
from datetime import datetime

SITE_DIR = Path('site')
TOC_HTML = Path('toc.html')
OUTPUT_PDF = Path('docs-n8n-full.pdf')
WKHTMLTOPDF = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
PAGE_SIZE = 'A4'
MARGIN_TOP = '10mm'
MARGIN_BOTTOM = '10mm'

# 1. Сканируем все index.html (можно поменять на *.html)
html_files = sorted([f for f in SITE_DIR.rglob('index.html')])
if not html_files:
    print('No HTML files found to export.')
    exit(1)

# 2. Проверка, нужно пересоздавать? Сравниваем даты
rebuild = False
if not OUTPUT_PDF.exists() or not TOC_HTML.exists():
    rebuild = True
else:
    pdf_mtime = OUTPUT_PDF.stat().st_mtime
    for html in html_files:
        if os.path.getmtime(html) > pdf_mtime:
            rebuild = True
            break

if not rebuild:
    print(f'{OUTPUT_PDF} is already up to date. Skipping rebuild.')
    exit(0)

# 3. Формируем TOC-файл (главная страница с ссылками)
toc_lines = [
    "<html><head><meta charset='utf-8'><style>body{font-family:sans-serif;margin:40px;}li{margin-bottom:5px}</style><title>n8n Documentation PDF</title></head><body>",
    f'<h1>n8n Full Documentation (PDF Export)</h1>',
    f'<p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>',
    '<ol>'
]
for html_file in html_files:
    # Превращаем абсолютный путь в относительный и читабельный заголовок
    rel = html_file.relative_to(SITE_DIR)
    title = rel.parent.as_posix().replace('-', ' ').title() or "Home"
    toc_lines.append(f'<li><a href="{html_file.as_posix()}">{title}</a></li>')
    # Вставляем и содержимое каждой страницы (inline)
    try:
        with open(html_file, encoding="utf-8") as f:
            html_content = f.read()
        toc_lines.append('<hr>')
        toc_lines.append(f'<h2>{title}</h2>')
        toc_lines.append(html_content)
    except Exception as e:
        toc_lines.append(f'<div style="color:red">Ошибка открытия {html_file}: {e}</div>')

toc_lines.append('</ol></body></html>')
with open(TOC_HTML, "w", encoding="utf-8") as f:
    f.write("\n".join(toc_lines))
print(f'TOC HTML prepared as {TOC_HTML}')

# 4. Вызов wkhtmltopdf по свежему toc.html
cmd = [
    WKHTMLTOPDF,
    '--enable-local-file-access',
    '--page-size', PAGE_SIZE,
    '--margin-top', MARGIN_TOP,
    '--margin-bottom', MARGIN_BOTTOM,
    str(TOC_HTML),
    str(OUTPUT_PDF)
]
try:
    subprocess.run(cmd, check=True)
    print(f'=== New full documentation PDF created: {OUTPUT_PDF} ===')
except subprocess.CalledProcessError as e:
    print('Error running wkhtmltopdf:', e)
    exit(1)
