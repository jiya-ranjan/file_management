import os
import shutil
import logging
import zipfile
import tarfile
import rarfile
from datetime import datetime
import base64
import hashlib
from cryptography.fernet import Fernet


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
    def __init__(self, root_dir, current_user):
        self.current_dir = os.path.abspath(root_dir)
        self.current_user = current_user
        os.makedirs(self.current_dir, exist_ok=True)


    def log(self, action):
        logging.info(action)

    def create_directory(self, dir_name):
        if USERS.get(self.current_user)['role'] != 'admin':
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
        if USERS.get(self.current_user)['role'] != 'admin':
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
        if USERS.get(self.current_user)['role'] != 'admin':
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

    def _generate_key(self, password):
        return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

    def encrypt_file(self, file_name, password):
        path = os.path.join(self.current_dir, file_name)
        if not os.path.isfile(path):
            print(f"File '{file_name}' does not exist.")
            return

        try:
            key = self._generate_key(password)
            fernet = Fernet(key)
            with open(path, 'rb') as file:
                original = file.read()
            encrypted = fernet.encrypt(original)

            with open(path, 'wb') as file:
                file.write(encrypted)
            msg = f"File '{file_name}' encrypted with password."
            print(msg)
            self.log(msg)
        except Exception as e:
            print(f"Error: {e}")
            self.log(f"Encryption error: {e}")

    def decrypt_file(self, file_name, password):
        path = os.path.join(self.current_dir, file_name)
        if not os.path.isfile(path):
            print(f"File '{file_name}' does not exist.")
            return

        try:
            key = self._generate_key(password)
            fernet = Fernet(key)
            with open(path, 'rb') as file:
                encrypted = file.read()
            decrypted = fernet.decrypt(encrypted)

            with open(path, 'wb') as file:
                file.write(decrypted)
            msg = f"File '{file_name}' decrypted with password."
            print(msg)
            self.log(msg)
        except Exception as e:
            print(f"Error: {e}")
            self.log(f"Decryption error: {e}")

    def show_properties(self, name):
        path = os.path.join(self.current_dir, name)
        if not os.path.exists(path):
            print("File/Folder does not exist.")
            return
        print(f"\nProperties for: {path}")
        print(f"Type: {'Directory' if os.path.isdir(path) else 'File'}")
        print(f"Size: {os.path.getsize(path)} bytes")
        print(f"Last Modified: {datetime.fromtimestamp(os.path.getmtime(path))}")
        print(f"Permissions: {oct(os.stat(path).st_mode)[-3:]}")
        self.log(f"Viewed properties of {name}")

    def show_tree(self, path=None, prefix=""):
        if path is None:
            path = self.current_dir
            print(f"\nDirectory tree for: {path}")
        items = os.listdir(path)
        for idx, item in enumerate(items):
            full_path = os.path.join(path, item)
            connector = "└── " if idx == len(items) - 1 else "├── "
            print(prefix + connector + item)
            if os.path.isdir(full_path):
                self.show_tree(full_path, prefix + ("    " if idx == len(items) - 1 else "│   "))
        if prefix == "":
            self.log("Displayed directory tree.")

    def show_recent_files(self, count=5):
        files = []
        for root, dirs, filenames in os.walk(self.current_dir):
            for f in filenames:
                full_path = os.path.join(root, f)
                files.append((full_path, os.path.getmtime(full_path)))
        files.sort(key=lambda x: x[1], reverse=True)
        print("\nRecent files:")
        for f, t in files[:count]:
            print(f"{f} (Last Modified: {datetime.fromtimestamp(t)})")
        self.log("Viewed recent files.")

    def batch_rename(self, old_pattern, new_pattern):
        renamed = 0
        for fname in os.listdir(self.current_dir):
            if old_pattern in fname:
                new_name = fname.replace(old_pattern, new_pattern)
                os.rename(os.path.join(self.current_dir, fname), os.path.join(self.current_dir, new_name))
                print(f"Renamed: {fname} -> {new_name}")
                renamed += 1
        print(f"Total files renamed: {renamed}")
        self.log(f"Batch renamed files from {old_pattern} to {new_pattern}")

    def preview_file(self, file_name, lines=10):
        path = os.path.join(self.current_dir, file_name)
        if not os.path.isfile(path):
            print("File does not exist.")
            return
        print(f"\nPreview of '{file_name}':")
        with open(path, 'r', errors='ignore') as f:
            for i in range(lines):
                line = f.readline()
                if not line:
                    break
                print(line.rstrip())
        self.log(f"Previewed file {file_name}")

    def find_duplicates(self):
        hashes = {}
        duplicates = []
        for root, dirs, files in os.walk(self.current_dir):
            for fname in files:
                path = os.path.join(root, fname)
                try:
                    with open(path, 'rb') as f:
                        filehash = hashlib.md5(f.read()).hexdigest()
                    if filehash in hashes:
                        duplicates.append((path, hashes[filehash]))
                    else:
                        hashes[filehash] = path
                except Exception:
                    continue
        if duplicates:
            print("\nDuplicate files found:")
            for dup, orig in duplicates:
                print(f"{dup} == {orig}")
        else:
            print("No duplicate files found.")
        self.log("Checked for duplicate files.")

    # Simple bookmarking using a file
    def bookmark_folder(self, folder_name):
        path = os.path.join(self.current_dir, folder_name)
        if not os.path.isdir(path):
            print("Folder does not exist.")
            return
        with open("bookmarks.txt", "a") as f:
            f.write(path + "\n")
        print(f"Bookmarked: {path}")
        self.log(f"Bookmarked folder {folder_name}")

    def list_bookmarks(self):
        print("\nBookmarked folders:")
        try:
            with open("bookmarks.txt", "r") as f:
                for line in f:
                    print(line.strip())
        except FileNotFoundError:
            print("No bookmarks found.")
        self.log("Listed bookmarks.")

# Move authenticate outside the class
def authenticate():
    print("--- Login ---")
    username = input("Username: ")
    password = input("Password: ")
    if USERS.get(username) and USERS[username]['password'] == password:
        print("Login successful.")
        logging.info(f"User '{username}' logged in.")
        return username
    else:
        print("Invalid credentials.")
        logging.warning("Failed login attempt.")
        return None

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
    print("17. Encrypt File")
    print("18. Decrypt File")
    print("19. Show File/Folder Properties")
    print("20. Show Directory Tree")
    print("21. Show Recent Files")
    print("22. Batch Rename Files")
    print("23. Preview File (First 10 lines)")
    print("24. Find Duplicate Files")
    print("25. Bookmark Folder")
    print("26. List Bookmarked Folders")
    print("27. Exit")
    print("Type --help for instructions.")

def main():
    current_user = authenticate()
    if not current_user:
        return

    fm = FileManager("file_management_system", current_user)

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
            fm.search(input("Name to search: "), file_size=1000)
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
            fm.encrypt_file(input("File name: "), input("Password: "))
        elif choice == '18':
            fm.decrypt_file(input("File name: "), input("Password: "))
        elif choice == '19':
            fm.show_properties(input("File/Folder name: "))
        elif choice == '20':
            fm.show_tree()
        elif choice == '21':
            fm.show_recent_files()
        elif choice == '22':
            fm.batch_rename(input("Old pattern: "), input("New pattern: "))
        elif choice == '23':
            fm.preview_file(input("File name: "))
        elif choice == '24':
            fm.find_duplicates()
        elif choice == '25':
            fm.bookmark_folder(input("Folder name: "))
        elif choice == '26':
            fm.list_bookmarks()
        elif choice == '27':
            print("Goodbye!")
            logging.info("Session ended.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

