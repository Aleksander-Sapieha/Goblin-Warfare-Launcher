import json
import os
import requests
import subprocess
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GAMES_DIR = os.path.join(BASE_DIR, "games")
CACHE_DIR = os.path.join(BASE_DIR, "cache")

os.makedirs(GAMES_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

# Load versions
with open("versions.json", "r") as f:
    data = json.load(f)

versions = data["versions"]

def download_version(version):
    url = version["url"]
    vid = version["id"]

    jar_path = os.path.join(GAMES_DIR, vid, "game.jar")
    os.makedirs(os.path.dirname(jar_path), exist_ok=True)

    r = requests.get(url, stream=True)
    with open(jar_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

def launch_version(version):
    vid = version["id"]
    jar_path = os.path.join(GAMES_DIR, vid, "game.jar")

    if not os.path.exists(jar_path):
        messagebox.showerror("Error", "Game not installed or missing .jar")
        return

    try:
        subprocess.Popen([
            "java",
            "-jar",
            jar_path
        ])
    except FileNotFoundError:
        messagebox.showerror("Error", "Java is not installed or not in PATH")

# UI
root = tk.Tk()
root.title("Game Launcher")
root.geometry("400x300")

tk.Label(root, text="Select Version").pack()

for v in versions:
    frame = tk.Frame(root)
    frame.pack(pady=5)

    tk.Label(frame, text=v["name"]).pack(side=tk.LEFT)

    tk.Button(frame, text="Install", command=lambda v=v: download_version(v)).pack(side=tk.LEFT)
    tk.Button(frame, text="Play", command=lambda v=v: launch_version(v)).pack(side=tk.LEFT)

root.mainloop()