Set oWS = WScript.CreateObject("WScript.Shell")
sDesktop = oWS.SpecialFolders("Desktop")

' 1. Master Server + Browser Launcher
sLink1 = sDesktop & "\DisinfoShield AI.lnk"
Set oLink1 = oWS.CreateShortcut(sLink1)
oLink1.TargetPath = "d:\Antigravjity workshowp\Launch_Disinfo_App.bat"
oLink1.WorkingDirectory = "d:\Antigravjity workshowp"
oLink1.IconLocation = "d:\Antigravjity workshowp\app_icon.ico,0"
oLink1.Description = "Disinfo Shield AI 2026 - Master Launcher"
oLink1.Save

' 2. Direct Browser App Launcher
sLink2 = sDesktop & "\DisinfoShield Direct UI.lnk"
Set oLink2 = oWS.CreateShortcut(sLink2)
oLink2.TargetPath = "d:\Antigravjity workshowp\desktop_app.html"
oLink2.WorkingDirectory = "d:\Antigravjity workshowp"
oLink2.IconLocation = "d:\Antigravjity workshowp\app_icon.ico,0"
oLink2.Description = "Disinfo Shield AI 2026 - Direct Dashboard"
oLink2.Save

WScript.Echo "SUCCESS"
