rem fc /b %USERPROFILE%\OneDrive\Документы\доходы_расходы.xls source-data\доходы_расходы.xls >NUL
"C:\Program Files (x86)\KDiff3\bin"\cmp %USERPROFILE%\OneDrive\Документы\доходы_расходы.xls source-data\доходы_расходы.xls
IF %ERRORLEVEL% EQU 0 EXIT 0
copy %USERPROFILE%\OneDrive\Документы\доходы_расходы.xls source-data 
python script.py %1 %2 %3
