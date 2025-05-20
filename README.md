
# File Management System

## Project Summary

Yeh project ek **File Management System** hai jo Python me banaya gaya hai. Isme aap files aur folders ko create, delete, rename, move, copy, compress, encrypt, search, bookmark, aur aur bhi kai tarah se manage kar sakte hain. Isme admin aur user roles ka bhi concept hai.

## Features

- **User Authentication** (Admin/User)
- **Create/Delete/Rename/Move/Copy** files and folders
- **List directory contents**
- **Read/Write files**
- **Search files/folders** (by name, size, type, date)
- **Change directory**
- **Show current path**
- **Compress/Decompress files** (.zip)
- **Encrypt/Decrypt files** (password protected)
- **Show file/folder properties**
- **Show directory tree**
- **Show recent files**
- **Batch rename files**
- **Preview file contents**
- **Find duplicate files**
- **Bookmark folders**
- **View and list bookmarks**
- **Log dashboard** (track operations and errors)

## How to Use

1. **Run the program:**  
   ```
   python file_manager.py
   ```

2. **Login:**  
   - Username and password dalen (default users: admin/admin123, jiya/1234, sneha/abcd, charvi/pass)

## Example Users

| Username | Password  | Role  |
|----------|-----------|-------|
| admin    | admin123  | admin |
| jiya     | 1234      | user  |
| sneha    | abcd      | user  |
| charvi   | pass      | user  |

## Requirements

- Python 3.x
- cryptography (`pip install cryptography`)
- rarfile (`pip install rarfile`)

## Notes

- Kuch features (jaise delete/create directory) sirf admin ke liye hain.
- Sabhi operations ka log `operations.log` file me save hota hai.
- Bookmarks `bookmarks.txt` file me store hote hain.

---


1. **Create Directory (Admin Only)**  
   Naya folder banata hai (sirf admin bana sakta hai).

2. **Create File**  
   Nayi file create karta hai.

3. **List Directory**  
   Current folder ke andar sabhi files aur folders ki list dikhata hai.

4. **Delete File (Admin Only)**  
   File ko delete karta hai (sirf admin ke liye).

5. **Delete Directory (Admin Only)**  
   Folder ko delete karta hai (sirf admin ke liye).

6. **Move File/Directory**  
   File ya folder ko ek jagah se doosri jagah le jata hai.

7. **Rename File/Directory**  
   File ya folder ka naam badalta hai.

8. **Copy File/Directory**  
   File ya folder ki copy banata hai.

9. **Read File**  
   File ka content (text) dikhata hai.

10. **Write to File**  
    File me text add karta hai.

11. **Search File/Directory**  
    Naam, size, type, ya date ke basis par file/folder dhoondta hai.

12. **Change Directory**  
    Kisi doosre folder me chala jata hai.

13. **Show Current Path**  
    Abhi kis folder me ho, uska path dikhata hai.

14. **Compress File (.zip)**  
    File ko zip format me compress karta hai.

15. **Decompress File (.zip)**  
    Zip file ko extract karta hai.

16. **View Log Dashboard**  
    Sabhi operations ka summary aur errors dikhata hai.

17. **Encrypt File**  
    File ko password se lock (encrypt) karta hai.

18. **Decrypt File**  
    Password se file ko unlock (decrypt) karta hai.

19. **Show File/Folder Properties**  
    File/folder ka size, type, permissions, etc. dikhata hai.

20. **Show Directory Tree**  
    Folder ka tree structure dikhata hai (subfolders ke sath).

21. **Show Recent Files**  
    Recent (abhi abhi badle) files ki list dikhata hai.

22. **Batch Rename Files**  
    Ek pattern ke hisaab se kai files ka naam ek sath badalta hai.

23. **Preview File (First 10 lines)**  
    File ki shuru ki 10 lines dikhata hai (preview).

24. **Find Duplicate Files**  
    Same content wali files ko dhoondta hai.

25. **Bookmark Folder**  
    Kisi folder ko bookmark (favourite) me add karta hai.

26. **List Bookmarked Folders**  
    Sabhi bookmarked folders ki list dikhata hai.

27. **Exit**  
    Program band karta hai.

---

