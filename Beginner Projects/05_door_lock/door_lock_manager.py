"""
Project 5: Arduino Digital Door Lock - Password Management GUI
Lets you set a new password on the Arduino and shows a live access log.

Requires: pip install pyserial
"""

import tkinter as tk
from tkinter import messagebox
import serial
import threading
import time
import datetime

SERIAL_PORT = "COM3"
BAUD_RATE = 9600


class DoorLockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Door Lock - Password Manager")
        self.root.geometry("420x420")
        self.ser = None
        self.running = False

        top = tk.Frame(root)
        top.pack(pady=8)
        tk.Label(top, text="Serial Port:").pack(side="left")
        self.port_var = tk.StringVar(value=SERIAL_PORT)
        tk.Entry(top, textvariable=self.port_var, width=12).pack(side="left", padx=5)
        self.connect_btn = tk.Button(top, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack(side="left", padx=5)

        pass_frame = tk.Frame(root)
        pass_frame.pack(pady=15)
        tk.Label(pass_frame, text="New Password:").pack(side="left")
        self.pass_var = tk.StringVar()
        tk.Entry(pass_frame, textvariable=self.pass_var, width=10, show="*").pack(side="left", padx=5)
        tk.Button(pass_frame, text="Set Password", command=self.set_password).pack(side="left", padx=5)

        tk.Label(root, text="Access Log", font=("Arial", 12, "bold")).pack(pady=(15, 0))
        self.log_box = tk.Listbox(root, width=45, height=14)
        self.log_box.pack(pady=5)

    def toggle_connection(self):
        if not self.running:
            try:
                self.ser = serial.Serial(self.port_var.get(), BAUD_RATE, timeout=1)
                time.sleep(2)
                self.running = True
                self.connect_btn.config(text="Disconnect")
                threading.Thread(target=self.read_loop, daemon=True).start()
            except serial.SerialException as e:
                messagebox.showerror("Connection Error", str(e))
        else:
            self.running = False
            if self.ser:
                self.ser.close()
            self.connect_btn.config(text="Connect")

    def set_password(self):
        new_pass = self.pass_var.get().strip()
        if not new_pass:
            messagebox.showwarning("Invalid", "Enter a password first")
            return
        if self.ser and self.ser.is_open:
            self.ser.write((f"SETPASS:{new_pass}\n").encode())
            self.log_event(f"Password change requested -> {new_pass}")

    def read_loop(self):
        while self.running:
            try:
                line = self.ser.readline().decode("utf-8", errors="ignore").strip()
                if line in ("UNLOCKED", "DENIED", "PASS_SET"):
                    self.root.after(0, self.log_event, line)
            except Exception:
                pass

    def log_event(self, text):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_box.insert(tk.END, f"[{ts}] {text}")
        self.log_box.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = DoorLockApp(root)
    root.mainloop()
