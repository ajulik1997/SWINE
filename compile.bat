pyinstaller ^
	--distpath=./__TEMP__/dist ^
	--workpath=./__TEMP__/build ^
	--noconfirm ^
	--clean ^
	--onefile ^
	--specpath=./__TEMP__/ ^
	--icon=./icon.ico ^
	SWINE.py