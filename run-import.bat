fc /b %USERPROFILE%\OneDrive\���㬥���\��室�_��室�.xls source-data\��室�_��室�.xls >NUL
IF %ERRORLEVEL% EQU 0 EXIT 0
copy %USERPROFILE%\OneDrive\���㬥���\��室�_��室�.xls source-data 
python script.py %1 %2 %3
