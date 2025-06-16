@echo off
echo Starting Chess Game...
cd /d "%~dp0"
python chess.py
if errorlevel 1 (
    echo.
    echo Error occurred. Make sure Python and pygame are installed.
    echo Press any key to exit...
    pause > nul
)
