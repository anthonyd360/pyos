# Standalone Chess Game - No PyInstaller needed
import subprocess
import sys
import os

def run_chess():
    """Run the chess game using Python directly"""
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        chess_path = os.path.join(script_dir, 'chess.py')
        
        print("Starting Chess Game...")
        print("Make sure you have pygame installed: pip install pygame")
        print()
        
        # Run the chess game
        result = subprocess.run([sys.executable, chess_path], 
                              cwd=script_dir,
                              capture_output=False)
        
        if result.returncode != 0:
            print(f"\nChess game exited with code: {result.returncode}")
        
    except FileNotFoundError:
        print("Error: chess.py not found!")
        print("Make sure this script is in the same folder as chess.py")
    except Exception as e:
        print(f"Error running chess game: {e}")
    
    input("\nPress Enter to close...")

if __name__ == "__main__":
    run_chess()
