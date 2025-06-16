import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_file(filename):
    try:
        content = input("Enter content to save: ")
        with open(filename, 'w') as file:
            file.write(content)
        print(f"Successfully saved {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")

def open_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            print(f"Contents of {filename}:")
            print(content)
    except FileNotFoundError:
        print(f"File {filename} not found")
    except Exception as e:
        print(f"Error opening file: {e}")

def list_dir(path):
    try:
        items = os.listdir(path)
        for item in items:
            print(item)
    except Exception as e:
        print(f"Error listing directory: {e}")

def change_dir(path):
    try:
        os.chdir(path)
        print(f"Changed directory to {os.getcwd()}")
    except Exception as e:
        print(f"Error changing directory: {e}")

def mini_os_shell():
    clear_screen()
    print("Welcome to PyOS Shell!")
    while True:
        current_path = os.getcwd()
        command = input(f"pyos $ ").strip().split()

        if not command:
            continue

        cmd = command[0]
        args = command[1:]

        # Handle executable files directly
        if cmd.endswith('.exe'):
            response = input(f"Do you want to open {cmd}? (yes/no): ")
            if response == 'no':
                print("Exiting...")
                continue
            if response == 'yes':
                try:
                    os.startfile(cmd)
                    print(f"Successfully opened {cmd}")
                except Exception as e:
                    print(f"Error opening {cmd}: {e}")
            continue
            
        if cmd == "load" and len(command) > 1 and command[1] == "file":
            if len(command) > 2:
                filename = command[2]
            else:
                filename = input("which file do you want to load? ")
            open_file(filename)
        elif cmd == "save file":
            print("Saving file...")
            if args:
                filename = args[0]
                save_file(filename)
        elif cmd == "exit":
            print("Goodbye!")
            break
        elif cmd == "ls":
            list_dir(current_path)
        elif cmd == "cd":
            if args:
                change_dir(args[0])
            else:
                change_dir = input("Usage: cd <directory>")
                open_dir = input("Enter directory to change to: ")
                change_dir(open_dir)
        elif cmd == "open":
            if args:
                open_file(args[0])
            else:
                print("Usage: open <filename>")
                filename = input("Enter filename to open: ")
                open_file(filename)
                allow_edt = input("Do you want to edit the file? (yes/no): ").strip().lower()
                if allow_edt == 'yes':
                    content = input("Enter new content: ")
                    with open(filename, 'w') as file:
                        file.write(content)
                elif allow_edt == 'no':
                    print("File not modified")
        elif cmd == "clear":
            clear_screen()
        elif cmd == "app":
            if args:
                app_name = args[0]
                user_response = input(f"Do you want to open {app_name}? (yes/no): ").strip().lower()
                if user_response == 'yes':
                    print(f"Opening {app_name}...")
                    try:
                        os.startfile(app_name)  # This will open the executable on Windows
                        print(f"Successfully opened {app_name}")
                    except Exception as e:
                        print(f"Error opening {app_name}: {e}")
            else:
                print("Usage: app <filename>")
        elif cmd == "make_file":
            if args:
                filename = args[0]
                with open(filename, 'w') as file:
                    print(f"Created new file: {filename}")
            else:
                filename = input("name file (yes/no): ")
                if response == 'yes':
                    filename = input("Enter filename: ")
                    with open(filename, 'w') as file:
                        print(f"Created new file: {filename}")
                elif response == 'no':  # Changed 'if' to 'elif'
                    print("File not created")
        elif cmd == "delete":
            if args:
                filename = args[0]
            else:
                filename = input("Enter filename to delete: ")
            
            confirm = input(f"Are you sure you want to delete {filename}? (yes/no): ").strip().lower()
            if confirm == 'yes':
                try:
                    os.remove(filename)
                    print(f"Deleted file: {filename}")
                except Exception as e:
                    print(f"Error deleting file: {e}")
            elif confirm == 'no':
                print("File not deleted")
        elif cmd == "":
            print("No command entered. Please try again.")
        elif cmd == "install":
            if args:
                package_name = args[0]
                try:
                    package_name = input("Usage: install <package_name>")
                    import subprocess
                    print(f"Installing {package_name}...")
                    subprocess.check_call(['pip', 'install', package_name])
                    print(f"{package_name} installed successfully.")
                except Exception as e:
                    print(f"Error installing package: {e}")
        

if __name__ == "__main__":
    mini_os_shell()
# This is a simple mini OS shell implemented in Python.
# It supports basic commands like 'ls', 'cd', 'open', and 'clear'.