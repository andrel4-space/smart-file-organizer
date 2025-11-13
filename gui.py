import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import threading
from organizer import scan_and_organize, organize_file
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class OrganizerHandler(FileSystemEventHandler):
    def __init__(self, root_folder: Path):
        self.root = root_folder

    def on_created(self, event):
        if not event.is_directory:
            organize_file(Path(event.src_path), self.root)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart File Organizer")
        self.geometry("400x200")
        self.folder = None
        self.observer = None

        ttk.Label(self, text="Choose a folder to keep organized:").pack(pady=10)
        ttk.Button(self, text="Browse…", command=self.pick).pack()
        self.start_btn = ttk.Button(self, text="Start Organizing", command=self.start, state="disabled")
        self.start_btn.pack(pady=10)
        ttk.Button(self, text="Stop", command=self.stop).pack()

    def pick(self):
        dir_ = filedialog.askdirectory()
        if dir_:
            self.folder = Path(dir_)
            self.start_btn.config(state="normal")
            messagebox.showinfo("Folder selected", f"Watching: {self.folder}")

    def start(self):
        if not self.folder:
            return
        scan_and_organize(self.folder)
        event_handler = OrganizerHandler(self.folder)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.folder), recursive=False)
        self.observer.start()
        messagebox.showinfo("Started", "Organizer is running in the background.\nMinimize this window.")

    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
        self.destroy()

if __name__ == "__main__":
    App().mainloop()
