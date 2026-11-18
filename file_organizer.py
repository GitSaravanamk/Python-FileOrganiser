"""
Automatic File Organizer
A small Tkinter desktop app that sorts files in a selected folder by file type.

Safety notes:
- Preview shows planned moves before anything is changed.
- Only files directly inside the selected folder are organized (not subfolders).
- Existing files are never overwritten; a numbered name is chosen instead.
"""

from pathlib import Path
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".tiff"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"},
    "Spreadsheets": {".xls", ".xlsx", ".csv", ".ods"},
    "Presentations": {".ppt", ".pptx", ".odp"},
    "Videos": {".mp4", ".mkv", ".mov", ".avi", ".wmv", ".webm"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Programs": {".py", ".java", ".js", ".html", ".css", ".json", ".exe", ".msi"},
}


def category_for(file_path: Path) -> str:
    """Return the destination folder name for a file."""
    extension = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"


def available_destination(destination: Path) -> Path:
    """Return a non-existing destination path without overwriting a file."""
    if not destination.exists():
        return destination

    counter = 1
    while True:
        candidate = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )
        if not candidate.exists():
            return candidate
        counter += 1


def planned_moves(folder: Path):
    """Create a list of (source, destination) pairs for files in one folder."""
    moves = []
    if not folder.is_dir():
        raise ValueError("Please select an existing folder.")

    for item in sorted(folder.iterdir(), key=lambda path: path.name.lower()):
        if not item.is_file():
            continue
        category = category_for(item)
        destination_folder = folder / category
        destination = available_destination(destination_folder / item.name)
        moves.append((item, destination))

    return moves


def organize_folder(folder: Path):
    """Move files into category folders. Returns (successful_moves, errors)."""
    moves = planned_moves(folder)
    successful_moves = []
    errors = []

    for source, destination in moves:
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            # Recheck the destination immediately before moving.
            destination = available_destination(destination)
            shutil.move(str(source), str(destination))
            successful_moves.append((source, destination))
        except OSError as error:
            errors.append(f"{source.name}: {error}")

    return successful_moves, errors


class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automatic File Organizer")
        self.root.geometry("760x540")
        self.root.minsize(620, 430)

        self.folder_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Choose a folder to get started.")

        self.build_interface()

    def build_interface(self):
        main = ttk.Frame(self.root, padding=16)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main, text="Automatic File Organizer", font=("Arial", 18, "bold")
        ).pack(anchor="w")

        ttk.Label(
            main,
            text="Sort files into folders based on their file extensions.",
        ).pack(anchor="w", pady=(4, 14))

        folder_row = ttk.Frame(main)
        folder_row.pack(fill="x")

        ttk.Entry(folder_row, textvariable=self.folder_var).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(folder_row, text="Browse...", command=self.choose_folder).pack(
            side="left", padx=(8, 0)
        )

        button_row = ttk.Frame(main)
        button_row.pack(fill="x", pady=12)

        ttk.Button(button_row, text="Preview", command=self.preview).pack(side="left")
        ttk.Button(
            button_row, text="Organize Files", command=self.organize
        ).pack(side="left", padx=8)
        ttk.Button(button_row, text="Clear", command=self.clear_preview).pack(
            side="left"
        )

        ttk.Label(main, text="Preview / Results", font=("Arial", 11, "bold")).pack(
            anchor="w", pady=(4, 6)
        )

        output_frame = ttk.Frame(main)
        output_frame.pack(fill="both", expand=True)

        self.output = tk.Text(output_frame, wrap="word", height=16, state="disabled")
        scrollbar = ttk.Scrollbar(
            output_frame, orient="vertical", command=self.output.yview
        )
        self.output.configure(yscrollcommand=scrollbar.set)
        self.output.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Label(main, textvariable=self.status_var).pack(anchor="w", pady=(10, 0))
        ttk.Label(
            main,
            text="Safety: Preview first. Subfolders are not scanned, and existing files are not overwritten.",
            wraplength=700,
        ).pack(anchor="w", pady=(5, 0))

    def write_output(self, text):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", text)
        self.output.configure(state="disabled")

    def choose_folder(self):
        selected = filedialog.askdirectory(title="Select a folder to organize")
        if selected:
            self.folder_var.set(selected)
            self.status_var.set("Folder selected. Click Preview before organizing.")

    def get_folder(self):
        folder_text = self.folder_var.get().strip()
        if not folder_text:
            messagebox.showwarning("Folder required", "Please choose a folder first.")
            return None
        folder = Path(folder_text).expanduser()
        if not folder.is_dir():
            messagebox.showerror("Invalid folder", "The selected folder does not exist.")
            return None
        return folder

    def preview(self):
        folder = self.get_folder()
        if folder is None:
            return
        try:
            moves = planned_moves(folder)
        except (OSError, ValueError) as error:
            messagebox.showerror("Preview error", str(error))
            return

        if not moves:
            self.write_output("No files found directly inside this folder.")
            self.status_var.set("Nothing to organize.")
            return

        lines = [f"Selected folder: {folder}", "", "Planned file moves:", ""]
        for source, destination in moves:
            lines.append(f"{source.name}  ->  {destination.parent.name}/{destination.name}")

        self.write_output("\n".join(lines))
        self.status_var.set(f"Preview ready: {len(moves)} file(s) can be organized.")

    def organize(self):
        folder = self.get_folder()
        if folder is None:
            return

        try:
            moves = planned_moves(folder)
        except (OSError, ValueError) as error:
            messagebox.showerror("Organize error", str(error))
            return

        if not moves:
            messagebox.showinfo("Nothing to do", "No files were found in this folder.")
            return

        confirmed = messagebox.askyesno(
            "Confirm organization",
            f"Organize {len(moves)} file(s) in:\n\n{folder}\n\n"
            "Files will be moved into category folders. Continue?",
        )
        if not confirmed:
            return

        successful, errors = organize_folder(folder)

        lines = [
            f"Organization complete for: {folder}",
            "",
            f"Successfully moved: {len(successful)}",
            f"Errors: {len(errors)}",
            "",
        ]
        for source, destination in successful:
            lines.append(f"MOVED: {source.name} -> {destination.parent.name}/{destination.name}")
        for error in errors:
            lines.append(f"ERROR: {error}")

        self.write_output("\n".join(lines))
        self.status_var.set(
            f"Finished: {len(successful)} moved, {len(errors)} error(s)."
        )
        if errors:
            messagebox.showwarning(
                "Completed with errors",
                f"{len(successful)} file(s) moved. {len(errors)} file(s) could not be moved. See results.",
            )
        else:
            messagebox.showinfo(
                "Completed",
                f"Successfully organized {len(successful)} file(s).",
            )

    def clear_preview(self):
        self.write_output("")
        self.status_var.set("Preview cleared.")


def main():
    root = tk.Tk()
    FileOrganizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
