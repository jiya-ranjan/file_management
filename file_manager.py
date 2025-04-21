import os
import shutil
import logging
import zipfile
import tarfile
import rarfile
from datetime import datetime

# Setup logging
logging.basicConfig(filename='operations.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Sample user database with roles
USERS = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'jiya': {'password': '1234', 'role': 'user'},
    'sneha': {'password': 'abcd', 'role': 'user'},
    'charvi': {'password': 'pass', 'role': 'user'}
}

class FileManager:
    def __init__(self, root_dir):
        self.current_dir = os.path.abspath(root_dir)
        os.makedirs(self.current_dir, exist_ok=True)

    def log(self, action):
        logging.info(action)

    def create_directory(self, dir_name):
        if USERS.get(current_user)['role'] != 'admin':
            print("Only Admin can create directories.")
            return
        path = os.path.join(self.current_dir, dir_name)
        try:
            os.makedirs(path)
            msg = f"Directory '{dir_name}' created."
            print(msg)
            self.log(msg)
        except FileExistsError:
            msg = f"Directory '{dir_name}' already exists."
            print(msg)
            self.log(msg)

    def create_file(self, file_name):
        path = os.path.join(self.current_dir, file_name)
        if not os.path.exists(path):
            with open(path, 'w') as f:
                pass
            msg = f"File '{file_name}' created."
            print(msg)
            self.log(msg)
        else:
            msg = f"File '{file_name}' already exists."
            print(msg)
            self.log(msg)

    def list_directory(self):
        items = os.listdir(self.current_dir)
        print(f"\nContents of '{self.current_dir}':")
        for item in items:
            print(item)
        self.log("Listed directory contents.")

    def delete_file(self, file_name):
        if USERS.get(current_user)['role'] != 'admin':
            print("Only Admin can delete files.")
            return
        path = os.path.join(self.current_dir, file_name)
        try:
            os.remove(path)
            msg = f"File '{file_name}' deleted."
            print(msg)
            self.log(msg)
        except FileNotFoundError:
            msg = f"File '{file_name}' not found."
            print(msg)
            self.log(msg)

    def delete_directory(self, dir_name):
        if USERS.get(current_user)['role'] != 'admin':
            print("Only Admin can delete directories.")
            return
        path = os.path.join(self.current_dir, dir_name)
        try:
            shutil.rmtree(path)
            msg = f"Directory '{dir_name}' deleted."
            print(msg)
            self.log(msg)
        except FileNotFoundError:
            msg = f"Directory '{dir_name}' not found."
            print(msg)
            self.log(msg)

    def move(self, src, dest):
        try:
            shutil.move(os.path.join(self.current_dir, src), os.path.join(self.current_dir, dest))
            msg = f"Moved '{src}' to '{dest}'."
            print(msg)
            self.log(msg)
        except Exception as e:
            print(f"Error: {e}")
            self.log(f"Move error: {e}")

    def rename(self, old_name, new_name):
        try:
            os.rename(os.path.join(self.current_dir, old_name), os.path.join(self.current_dir, new_name))
            msg = f"Renamed '{old_name}' to '{new_name}'."
            print(msg)
            self.log(msg)
        except FileNotFoundError:
            msg = f"'{old_name}' not found."
            print(msg)
            self.log(msg)

    def copy(self, src, dest):
        src_path = os.path.join(self.current_dir, src)
        dest_path = os.path.join(self.current_dir, dest)
        try:
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path)
            else:
                shutil.copy2(src_path, dest_path)
            msg = f"Copied '{src}' to '{dest}'."
            print(msg)
            self.log(msg)
        except Exception as e:
            print(f"Error: {e}")
            self.log(f"Copy error: {e}")

    def read_file(self, file_name):
        path = os.path.join(self.current_dir, file_name)
        try:
            with open(path, 'r') as f:
                print(f"\n--- Content of '{file_name}' ---")
                print(f.read())
            self.log(f"Read file '{file_name}'.")
        except Exception as e:
            print(f"Error: {e}")
            self.log(f"Read error: {e}")

    def write_file(self, file_name, content):
        path = os.path.join(self.current_dir, file_name)
        try:
            with open(path, 'a') as f:
                f.write(content + '\n')
            msg = f"Content written to '{file_name}'."
            print(msg)
            self.log(msg)
        except Exception as e:
            print(f"Error: {e}")
            self.log(f"Write error: {e}")

    def search(self, name, file_size=None, file_type=None, modified_date=None):
        print(f"\nSearching for '{name}' in '{self.current_dir}'...")
        found = False
        for root, dirs, files in os.walk(self.current_dir):
            for file in files:
                if name in file:
                    file_path = os.path.join(root, file)
                    file_info = os.stat(file_path)
                    
                    if (file_size and file_info.st_size != file_size) or \
                       (file_type and not file.endswith(file_type)) or \
                       (modified_date and datetime.fromtimestamp(file_info.st_mtime).date() != modified_date):
                        continue
                    
                    found = True
                    print("Found:", file_path)
        if not found:
            print("No match found.")
        self.log(f"Searched for '{name}'.")

    def change_directory(self, dir_name):
        path = os.path.abspath(os.path.join(self.current_dir, dir_name))
        if os.path.isdir(path):
            self.current_dir = path
            msg = f"Changed directory to '{self.current_dir}'."
            print(msg)
            self.log(msg)
        else:
            msg = f"Directory '{dir_name}' does not exist."
            print(msg)
            self.log(msg)

    def show_current_path(self):
        print(f"Current Directory: {self.current_dir}")
        self.log("Displayed current directory path.")

    def compress_file(self, file_name, archive_name):
        try:
            with zipfile.ZipFile(archive_name, 'w') as zipf:
                zipf.write(os.path.join(self.current_dir, file_name), file_name)
            msg = f"File '{file_name}' compressed to '{archive_name}'"
            print(msg)
            self.log(msg)
        except Exception as e:
            print(f"Error: {e}")
            self.log(f"Compression error: {e}")

    def decompress_file(self, archive_name):
        try:
            with zipfile.ZipFile(archive_name, 'r') as zipf:
                zipf.extractall(self.current_dir)
            msg = f"File '{archive_name}' decompressed."
            print(msg)
            self.log(msg)
        except Exception as e:
            print(f"Error: {e}")
            self.log(f"Decompression error: {e}")

    def log_dashboard(self):
        print("\n--- Log Dashboard ---")
        with open('operations.log', 'r') as log_file:
            lines = log_file.readlines()
        
        command_counts = {}
        user_counts = {}
        errors = []
        
        for line in lines:
            if "Command" in line:
                command = line.split(" ")[-1].strip()
                command_counts[command] = command_counts.get(command, 0) + 1
            if "User" in line:
                user = line.split(" ")[-2].strip()
                user_counts[user] = user_counts.get(user, 0) + 1
            if "Error" in line:
                errors.append(line)
        
        print("Most used commands:", command_counts)
        print("Most active users:", user_counts)
        print("Errors over time:", len(errors))

def authenticate():
    global current_user
    print("--- Login ---")
    username = input("Username: ")
    password = input("Password: ")
    if USERS.get(username) and USERS[username]['password'] == password:
        current_user = username
        print("Login successful.")
        logging.info(f"User '{username}' logged in.")
        return True
    else:
        print("Invalid credentials.")
        logging.warning("Failed login attempt.")
        return False

def display_menu():
    print("\n--- File Management System ---")
    print("1. Create Directory (Admin Only)")
    print("2. Create File")
    print("3. List Directory")
    print("4. Delete File (Admin Only)")
    print("5. Delete Directory (Admin Only)")
    print("6. Move File/Directory")
    print("7. Rename File/Directory")
    print("8. Copy File/Directory")
    print("9. Read File")
    print("10. Write to File")
    print("11. Search File/Directory")
    print("12. Change Directory")
    print("13. Show Current Path")
    print("14. Compress File (.zip)")
    print("15. Decompress File (.zip)")
    print("16. View Log Dashboard")
    print("17. Exit")
    print("Type --help for instructions.")

def main():
    if not authenticate():
        return

    fm = FileManager("file_management_system")

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '--help':
            print("Help Instructions: Use the menu options to manage files.")
            continue
        elif choice == '1':
            fm.create_directory(input("Directory name: "))
        elif choice == '2':
            fm.create_file(input("File name: "))
        elif choice == '3':
            fm.list_directory()
        elif choice == '4':
            fm.delete_file(input("File name: "))
        elif choice == '5':
            fm.delete_directory(input("Directory name: "))
        elif choice == '6':
            fm.move(input("Source: "), input("Destination: "))
        elif choice == '7':
            fm.rename(input("Old name: "), input("New name: "))
        elif choice == '8':
            fm.copy(input("Source: "), input("Destination: "))
        elif choice == '9':
            fm.read_file(input("File name: "))
        elif choice == '10':
            fm.write_file(input("File name: "), input("Content: "))
        elif choice == '11':
            fm.search(input("Name to search: "), file_size=1000)  # Example: size > 1000 bytes
        elif choice == '12':
            fm.change_directory(input("Directory name: "))
        elif choice == '13':
            fm.show_current_path()
        elif choice == '14':
            fm.compress_file(input("File name: "), input("Archive name: "))
        elif choice == '15':
            fm.decompress_file(input("Archive name: "))
        elif choice == '16':
            fm.log_dashboard()
        elif choice == '17':
            print("Goodbye!")
            logging.info("Session ended.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
