@echo off


if not exist "%USERPROFILE%\scoop\shims\chromedriver.exe" (
  ping -n 2 -w 1000 1.1.1.1 | find "bytes="
  if %ERRORLEVEL% EQU 0 (
    echo Internet connection is available. Installing Scoop and chromedriver. . .
    @powershell -NoProfile -Command "& { Set-ExecutionPolicy RemoteSigned -Scope CurrentUser }"
    @powershell -NoProfile -Command "& { irm get.scoop.sh | iex }"
    @powershell -NoProfile -Command "& { scoop install chromedriver }"
  ) else (
    echo Internet connection is unavailable. Skipping Scoop and chromedriver install.
  )
)

cd %~dp0

if not exist venv ( python -m venv venv )

if exist venv (
	call venv\Scripts\activate.bat
	pip install -r requirements.txt 
)

pause
