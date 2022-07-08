@echo off

cd %~dp0

if not exist venv ( python -m venv venv )

if exist venv (
	call venv\Scripts\activate.bat
	pip install -r requirements.txt 
)

pause