# Automatic File Organizer (Python)

A beginner-friendly desktop application that sorts files into folders based on their extensions. The interface is built with Tkinter.

## Features

- Choose a folder using a Browse button
- Preview the planned moves before changing files
- Organize images, documents, spreadsheets, presentations, videos, audio, archives, programs, and other files
- Avoid overwriting files by adding a numbered suffix such as `photo_1.jpg`
- Display a summary of successful moves and errors
- Includes basic unit tests

## Requirements

- Python 3.9 or later recommended
- Tkinter (usually included with the standard Windows Python installer)
- No third-party Python packages are required

## Run on Windows

Open Command Prompt or PowerShell in this project folder.

1. Check Python:

   ```bash
   py --version
   ```

2. Check Tkinter:

   ```bash
   py -m tkinter
   ```

   A small demo window should appear. Close it before continuing.

3. Start the application:

   ```bash
   py file_organizer.py
   ```

## How to use

1. Click **Browse...** and select a folder.
2. Click **Preview** to see which files will move and where.
3. Check the preview carefully.
4. Click **Organize Files** and confirm the action.
5. Review the results in the application.

## Safety and limitations

- The app scans files directly inside the selected folder; it does not scan nested subfolders.
- It moves files, rather than copying them.
- It asks for confirmation before moving files.
- It does not overwrite an existing file. If a name is already taken, it chooses a numbered name.
- Choose a test folder with copies of sample files when learning. Do not experiment first on important folders.

## Run tests

From the project folder:

```bash
py -m unittest discover -s tests -v
```

## Project structure

```text
python-automatic-file-organizer/
|-- file_organizer.py
|-- tests/
|   |-- test_file_organizer.py
|-- README.md
|-- .gitignore
```

## Concepts demonstrated

- Functions and modules
- pathlib and file extensions
- os-level file and folder concepts
- shutil for moving files
- Tkinter widgets and event handling
- Exception handling
- Unit testing with unittest

## Future improvements

- Add a file-type customization screen
- Add an undo feature
- Add recursive folder scanning with an explicit option
- Add a scheduled organization feature
- Create an executable using PyInstaller

## GitHub upload

Create a GitHub repository named `python-automatic-file-organizer`, then follow the Git commands in the main project guide.
