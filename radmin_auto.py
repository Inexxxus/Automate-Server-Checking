import os
import time
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui

# ---------------- CONFIG ----------------
USERNAME = "administrator"
FIRST_PASSWORD = "supp0rt_n@n0X"
SECOND_PASSWORD = "np!_n@n0X_np!"

RADMIN_PATHS = [
    r"C:\Program Files\Radmin Viewer 3\radmin.exe",
    r"C:\Program Files (x86)\Radmin Viewer 3\radmin.exe",
]

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

stop_flag = threading.Event()
worker = None

# Hardcoded button positions
CONNECT_BTN = (445, 265)   # "Connect to an address"
REMOTE_TAB = (810, 15)     # Remote session tab
CAD_BTN = (225, 35)        # Ctrl+Alt+Del button

# Event Viewer positions
EV_WINDOWS_LOGS = (175, 170)
EV_SYSTEM = (245, 245)
EV_REFRESH = (1048, 600)


# ---------------- HELPERS ----------------
def launch_radmin():
    """Open Radmin from known paths or Windows search."""
    for path in RADMIN_PATHS:
        if os.path.isfile(path):
            subprocess.Popen([path])
            return
    # fallback: use Windows Search
    pyautogui.press("win")
    time.sleep(0.7)
    pyautogui.typewrite("radmin\n", interval=0.08)


def connect_to_address(address):
    """Click Connect, type IP, enter username + password."""
    time.sleep(5)  # wait for Radmin to open

    pyautogui.click(CONNECT_BTN[0], CONNECT_BTN[1])
    time.sleep(1)

    pyautogui.typewrite(address, interval=0.05)
    pyautogui.press("enter")

    # Username + first password
    time.sleep(2)
    pyautogui.typewrite(USERNAME, interval=0.05)
    pyautogui.press("tab")
    pyautogui.typewrite(FIRST_PASSWORD, interval=0.05)
    pyautogui.press("enter")


def activate_remote_tab():
    """Double click the remote session tab to make it active."""
    time.sleep(5)
    pyautogui.doubleClick(REMOTE_TAB[0], REMOTE_TAB[1])
    time.sleep(2)


def send_second_password():
    """Click Ctrl+Alt+Del button, type Windows password."""
    time.sleep(2)
    pyautogui.click(CAD_BTN[0], CAD_BTN[1])
    time.sleep(2)

    pyautogui.typewrite(SECOND_PASSWORD, interval=0.05)
    pyautogui.press("enter")


def open_event_viewer_remote():
    """Open Event Viewer and click into System logs + refresh."""
    time.sleep(5)

    # Run → eventvwr.msc
    pyautogui.hotkey("win", "r")
    time.sleep(1)
    pyautogui.typewrite("eventvwr.msc\n", interval=0.05)
    time.sleep(8)

    # Click sequence
    pyautogui.click(EV_WINDOWS_LOGS[0], EV_WINDOWS_LOGS[1])  # Windows Logs
    time.sleep(1)
    pyautogui.click(EV_SYSTEM[0], EV_SYSTEM[1])              # System
    time.sleep(1)
    pyautogui.click(EV_REFRESH[0], EV_REFRESH[1])            # Refresh
    time.sleep(1)


# ---------------- MAIN ----------------
def automation(address):
    stop_flag.clear()
    launch_radmin()
    connect_to_address(address)
    activate_remote_tab()
    send_second_password()
    open_event_viewer_remote()


# ---------------- UI ----------------
class AutoUI:
    def __init__(self, root):
        self.root = root
        root.title("Radmin Auto")
        root.attributes("-topmost", True)

        ttk.Label(root, text="Address/IP:").pack(pady=3)
        self.addr = tk.StringVar()
        ttk.Entry(root, textvariable=self.addr, width=30).pack(pady=3)

        self.btn_start = ttk.Button(root, text="Start", command=self.start)
        self.btn_start.pack(side="left", padx=5, pady=8)
        self.btn_stop = ttk.Button(root, text="Stop", command=self.stop, state="disabled")
        self.btn_stop.pack(side="left", padx=5)

    def start(self):
        global worker
        if not self.addr.get().strip():
            messagebox.showerror("Error", "Enter address first!")
            return
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        worker = threading.Thread(target=automation, args=(self.addr.get().strip(),), daemon=True)
        worker.start()

    def stop(self):
        stop_flag.set()
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoUI(root)
    root.mainloop()
