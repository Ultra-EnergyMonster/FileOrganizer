import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog

# File categories and their extensions (.png, .mp3 etc)
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".7z"],
    "Scripts": [".py", ".js", ".html", ".css"]
}

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")

        # Store selected folder
        self.source_folder = os.path.expanduser("~/Downloads")

        # Label + Folder selection button
        self.folder_label = tk.Label(root, text=f"Target folder:\n{self.source_folder}")
        self.folder_label.pack(pady=5)

        self.browse_btn = tk.Button(root, text="Change Folder", command=self.change_folder)
        self.browse_btn.pack(pady=5)

        # Checkboxes for file categories
        self.vars = {}
        self.checkboxes = []

        tk.Label(root, text="Select categories to organize:").pack()

        for category in FILE_TYPES.keys():
            var = tk.BooleanVar(value=True)  # default checked
            cb = tk.Checkbutton(root, text=category, variable=var)
            cb.pack(anchor="w")
            self.vars[category] = var
            self.checkboxes.append(cb)

        # Organize button
        self.organize_btn = tk.Button(root, text="Organize Files", command=self.organize_files)
        self.organize_btn.pack(pady=10)

    def change_folder(self):
        folder_selected = filedialog.askdirectory(initialdir=self.source_folder)
        if folder_selected:
            self.source_folder = folder_selected
            self.folder_label.config(text=f"Target folder:\n{self.source_folder}")

    def organize_files(self):
        selected_categories = [cat for cat, var in self.vars.items() if var.get()]
        if not selected_categories:
            messagebox.showwarning("Warning", "Please select at least one category!")
            return

        # Create folders for categories
        for category in selected_categories:
            folder_path = os.path.join(self.source_folder, category)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

        moved_files = 0
        skipped_files = 0

        # Loop through files in source folder
        for filename in os.listdir(self.source_folder):
            file_path = os.path.join(self.source_folder, filename)

            if os.path.isdir(file_path):
                continue  # skip

            _, ext = os.path.splitext(filename)
            ext = ext.lower()

            moved = False
            for category in selected_categories:
                if ext in FILE_TYPES[category]:
                    dest_path = os.path.join(self.source_folder, category, filename)
                    shutil.move(file_path, dest_path)
                    print(f"Moved: {filename} → {category}")
                    moved_files += 1
                    moved = True
                    break

            if not moved:
                print(f"Skipped: {filename} (Unknown or unselected file type)")
                skipped_files += 1

        messagebox.showinfo("Done",
                            f"Organizing complete!\n\nFiles moved: {moved_files}\nFiles skipped: {skipped_files}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
