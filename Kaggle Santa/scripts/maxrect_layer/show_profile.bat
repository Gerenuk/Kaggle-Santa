SET PYTHONPATH=
IF !%1!==!! (SET PROFILEFILE="%CD%\default.profile"
) ELSE (SET PROFILEFILE=%1)
"C:\Program Files\Python 2.7.6\python.exe" -m runsnakerun.runsnake %PROFILEFILE%
