fc /b %USERPROFILE%\OneDrive\Документы\доходы_расходы.xls source-data\доходы_расходы.xls >NUL
IF %ERRORLEVEL% EQU 0 EXIT 0
copy %USERPROFILE%\OneDrive\Документы\доходы_расходы.xls source-data 
python script.py %1 %2 %3
