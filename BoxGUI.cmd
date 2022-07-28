@echo off

if exist venv (
	call venv\Scripts\activate.bat
	python gui.py 
)