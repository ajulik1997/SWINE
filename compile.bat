@echo off
setlocal
PATH=C:\mcstas-2.4.1\miniconda3\Scripts;%PATH%
@echo on
pyinstaller ^
	--distpath=./__TEMP__/dist ^
	--workpath=./__TEMP__/build ^
	--specpath=./__TEMP__/ ^
	--noconfirm ^
	--clean ^
	--onefile ^
	--icon=./icon.ico ^
	SWINE.py