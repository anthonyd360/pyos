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
        command = input(f"{current_path} $ ").strip().split()

        if not command:
            continue

        cmd = command[0]
        args = command[1:]

        # Handle executable files directly
        if cmd.endswith('.exe'):
            print(f"Do you want to open {cmd}? (yes/no): ")
            response = input().strip().lower()
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
            
        # Handle "load file" command properly
        if cmd == "load" and len(command) > 1 and command[1] == "file":
            if len(command) > 2:
                filename = command[2]
            else:
                filename = input("which file do you want to load? ")
            open_file(filename)
        elif cmd == "save" and len(command) > 1 and command[1] == "file":
            print("Saving file...")
            if len(command) > 2:
                filename = command[2]
                save_file(filename)
            else:
                filename = input("Enter filename to save: ")
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
                print("Usage: cd <directory>")
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
                    content = content.strip()
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
                        os.startfile(app_name)
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
                print("name file (yes/no): ")
                response = input().strip().lower()
                if response == 'yes':
                    filename = input("Enter filename: ")
                    with open(filename, 'w') as file:
                        print(f"Created new file: {filename}")
                elif response == 'no':
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
        elif cmd == "install":
            if args:
                package_name = args[0]
                try:
                    import subprocess
                    print(f"Installing {package_name}...")
                    subprocess.check_call(['pip', 'install', package_name])
                    print(f"{package_name} installed successfully.")
                except Exception as e:
                    print(f"Error installing package: {e}")
            else:
                package_name = input("Usage: install <package_name>: ")
                if package_name:
                    try:
                        import subprocess
                        print(f"Installing {package_name}...")
                        subprocess.check_call(['pip', 'install', package_name])
                        print(f"{package_name} installed successfully.")
                    except Exception as e:
                        print(f"Error installing package: {e}")
        elif cmd == "help":
            print("\nAvailable commands:")
            print("load file [filename] - Load and display file contents")
            print("save file [filename] - Save content to a file")
            print("open [filename] - Open and optionally edit a file")
            print("ls - List directory contents")
            print("cd <directory> - Change directory")
            print("clear - Clear screen")
            print("app <filename> - Run an application")
            print("make_file [filename] - Create a new file")
            print("delete [filename] - Delete a file")
            print("install <package> - Install a Python package")
            print("help - Show this help message")
            print("exit - Exit the shell")
        else:
            print(f"Unknown command: {cmd}")
            print("Type 'help' for available commands")

if __name__ == "__main__":
    mini_os_shell()
