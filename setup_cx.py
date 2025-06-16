from cx_Freeze import setup, Executable
import os

# Get current directory and images folder
current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, 'images')

# Build options
build_exe_options = {
    "packages": ["pygame", "sys", "os"],
    "include_files": [(images_dir, "images")],
    "excludes": ["tkinter"],
    "zip_include_packages": ["pygame"],
}

# Target executable
target = Executable(
    script="chess.py",
    base="Win32GUI",  # Use Win32GUI for windowed apps
    target_name="ChessGame.exe",
    icon=None
)

setup(
    name="Chess Game",
    version="1.0",
    description="2-Player Chess Game",
    options={"build_exe": build_exe_options},
    executables=[target]
)
