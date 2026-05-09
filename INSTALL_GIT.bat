@echo off
echo Installing Git for Windows...
echo.
echo 1. Downloading Git installer...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.41.0.windows.3/Git-2.41.0.3-64-bit.exe' -OutFile 'git-installer.exe'"
echo.
echo 2. Installing Git...
git-installer.exe /VERYSILENT /NORESTART
echo.
echo 3. Cleaning up...
del git-installer.exe
echo.
echo Git installation complete!
echo.
pause
