"""
Project 3: Smart Light Controller - Python GUI
Sends mode commands (AUTO / ON / OFF) to Arduino and displays live
light level + relay status.

Requires: pip install pyserial
"""

import tkinter as tk
from tkinter import messagebox
import serial
import threading
import time

SERIAL_PORT = "COM3"
BAUD_RATE = 9600


class SmartLightApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Light Controller")
        self.root.geometry("380x350")
        self.ser = None
        self.running = False

        top = tk.Frame(root)
        top.pack(pady=8)
        tk.Label(top, text="Serial Port:").pack(side="left")
        self.port_var = tk.StringVar(value=SERIAL_PORT)
        tk.Entry(top, textvariable=self.port_var, width=12).pack(side="left", padx=5)
        self.connect_btn = tk.Button(top, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack(side="left", padx=5)

        self.light_label = tk.Label(root, text="Light Level: --", font=("Arial", 12))
        self.light_label.pack(pady=10)

        self.status_label = tk.Label(root, text="Relay: --", font=("Arial", 14, "bold"))
        self.status_label.pack(pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="AUTO", width=10, command=lambda: self.send_cmd("AUTO")).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Force ON", width=10, bg="lightgreen", command=lambda: self.send_cmd("ON")).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Force OFF", width=10, bg="salmon", command=lambda: self.send_cmd("OFF")).grid(row=0, column=2, padx=5)

        self.mode_label = tk.Label(root, text="Mode: --", font=("Arial", 11))
        self.mode_label.pack(pady=10)

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

    def send_cmd(self, cmd):
        if self.ser and self.ser.is_open:
            self.ser.write((cmd + "\n").encode())

    def read_loop(self):
        while self.running:
            try:
                line = self.ser.readline().decode("utf-8", errors="ignore").strip()
                parts = line.split(",")
                if len(parts) == 3:
                    light, mode, relay = parts
                    self.root.after(0, self.update_ui, light, mode, relay)
            except Exception:
                pass

    def update_ui(self, light, mode, relay):
        self.light_label.config(text=f"Light Level: {light}")
        self.mode_label.config(text=f"Mode: {mode}")
        self.status_label.config(
            text=f"Relay: {relay}",
            fg="green" if relay == "ON" else "red"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartLightApp(root)
    root.mainloop()
