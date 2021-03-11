@echo on
(echo set Wshell=CreateObject^("Wscript.Shell"^)
echo Wshell.SendKeys "first"
echo Wshell.SendKeys "{ENTER}"
echo Wshell.SendKeys "first -b main_hz"
echo Wshell.SendKeys "{ENTER}")>"%tmp%\inputpassword.vbs"
start "" "%tmp%\inputpassword.vbs"
cd C:\Users\suzto_naw1ufi\Princess-connection-farm
python main_new.py
pause

