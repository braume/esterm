1-Unpackage the archive in the desired folder.

2-Install python 2.7
	-> type 'python -V' in terminal to check the version

3-Copy the folder serial in C:\Python27\Lib\Site-packages
	-> type : 'python' in terminal
	-> then 'import serial' display prompt if it is ok

4-Change home path in parameters.ini (path of the files you want to work on).


If you want a shortcut:

5- Create a .bat in the esterm.py folder and create a shortcut of it wherever you want.

6-In the .bat write:
@echo off
color 0E
:begin
python c:\Python27\esterm\esterm.py
pause
goto begin