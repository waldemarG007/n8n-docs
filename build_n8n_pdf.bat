@echo off
REM === Универсальная сборка общего PDF по всем HTML ===
setlocal enabledelayedexpansion
set "html_list_file=all_html_files.txt"
set "output_pdf=docs-n8n-full.pdf"

REM 1. Получить список всех .html (только index.html)
del "%html_list_file%" 2>nul
for /r %%f in (site\index.html) do echo %%f>>"%html_list_file%"
for /r %%f in (site\*\index.html) do echo %%f>>"%html_list_file%"

REM 2. Проверить, нужно ли обновлять PDF
set "update_pdf=no"
if not exist "%output_pdf%" (
  set "update_pdf=yes"
) else (
  for /f "delims=" %%f in (%html_list_file%) do (
    for %%h in (%%f) do for %%p in ("%output_pdf%") do (
      if %%~th GTR %%~tp set "update_pdf=yes"
    )
  )
)

if "!update_pdf!"=="yes" (
  echo Building full docs PDF out of all index.html files...
  set "html_files="
  for /f "delims=" %%f in (%html_list_file%) do set "html_files=!html_files! \"%%f\""
  call set "html_files=%%html_files:~1%%"
  "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" --enable-local-file-access --page-size A4 --margin-top 10mm --margin-bottom 10mm !html_files! "%output_pdf%"
  echo === New full documentation PDF created: %output_pdf% ===
) else (
  echo Full documentation PDF (%output_pdf%) is already up to date. Nothing to do.
)

endlocal
pause
