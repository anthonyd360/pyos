@echo off
title Chess Game
echo ===============================
echo    Chess Game Launcher
echo ===============================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo.
    pause
    exit /b 1
)

:: Check if pygame is installed
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo Installing pygame...
    pip install pygame
    if errorlevel 1 (
        echo ERROR: Failed to install pygame
        echo Please run: pip install pygame
        echo.
        pause
        exit /b 1
    )
)

:: Change to the script directory
cd /d "%~dp0"

:: Run the chess game
echo Starting Chess Game...
echo.
python chess.py

:: Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Game exited with an error.
    pause
)
