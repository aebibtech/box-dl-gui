@echo off

ping -n 2 -w 1000 1.1.1.1 | find "bytes="
if %ERRORLEVEL% EQU 0 (
	echo Internet connection is available. Installing Google Chrome, VLC, etc. . .
	@powershell -NoProfile -ExecutionPolicy Bypass -Command "& { Set-ExecutionPolicy Bypass -Force }"
	@powershell -NoProfile -ExecutionPolicy Bypass -Command "& {[System.Net.WebRequest]::DefaultWebProxy.Credentials = [System.Net.CredentialCache]::DefaultCredentials; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))}"
	start /b /wait %programdata%\chocolatey\bin\choco.exe install chromedriver -y --ignore-checksums
) else (
	echo Internet connection is unavailable. Skipping choco install.
)

cd %~dp0

if not exist venv ( python -m venv venv )

if exist venv (
	call venv\Scripts\activate.bat
	pip install -r requirements.txt 
)

pause