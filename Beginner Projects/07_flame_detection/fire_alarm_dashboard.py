"""
Project 7: Flame Detection System - Fire Alarm Dashboard
Shows a full-screen-style alert when a flame is detected, with an event log.

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


class FireAlarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fire Alarm Dashboard")
        self.root.geometry("420x420")
        self.ser = None
        self.running = False
        self.last_state = None

        top = tk.Frame(root)
        top.pack(pady=8)
        tk.Label(top, text="Serial Port:").pack(side="left")
        self.port_var = tk.StringVar(value=SERIAL_PORT)
        tk.Entry(top, textvariable=self.port_var, width=12).pack(side="left", padx=5)
        self.connect_btn = tk.Button(top, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack(side="left", padx=5)

        self.status_frame = tk.Frame(root, bg="green", width=380, height=150)
        self.status_frame.pack(pady=15)
        self.status_frame.pack_propagate(False)
        self.status_label = tk.Label(self.status_frame, text="SAFE", font=("Arial", 28, "bold"), bg="green", fg="white")
        self.status_label.pack(expand=True)

        tk.Label(root, text="Event Log", font=("Arial", 12, "bold")).pack(pady=(10, 0))
        self.log_box = tk.Listbox(root, width=45, height=10)
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

    def read_loop(self):
        while self.running:
            try:
                line = self.ser.readline().decode("utf-8", errors="ignore").strip()
                if line in ("FIRE", "SAFE"):
                    self.root.after(0, self.update_ui, line)
            except Exception:
                pass

    def update_ui(self, state):
        if state == "FIRE":
            self.status_frame.config(bg="red")
            self.status_label.config(text="🔥 FIRE DETECTED!", bg="red")
        else:
            self.status_frame.config(bg="green")
            self.status_label.config(text="SAFE", bg="green")

        if state != self.last_state:
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            self.log_box.insert(tk.END, f"[{ts}] State changed -> {state}")
            self.log_box.see(tk.END)
            self.last_state = state


if __name__ == "__main__":
    root = tk.Tk()
    app = FireAlarmApp(root)
    root.mainloop()
