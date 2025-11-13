import os
import shutil
from pathlib import Path
from datetime import datetime
import csv

LOG_FILE = "moves_log.csv"

CATEGORIES = {
    "Images":  [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Docs":    [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Videos":  [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Audio":   [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Archives":[".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
}

def category_for(ext: str) -> str:
    ext = ext.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Others"

def organize_file(file_path: Path, root_folder: Path):
    ext = file_path.suffix
    cat = category_for(ext)
    target_dir = root_folder / cat
    target_dir.mkdir(exist_ok=True)

    counter = 1
    target = target_dir / file_path.name
    while target.exists():
        stem = file_path.stem
        suffix = file_path.suffix
        target = target_dir / f"{stem}_{counter}{suffix}"
        counter += 1

    shutil.move(str(file_path), str(target))

    with open(LOG_FILE, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), str(file_path), str(target)])

def scan_and_organize(root_folder: Path):
    for item in root_folder.iterdir():
        if item.is_file() and not item.name.startswith('.'):
            organize_file(item, root_folder)
