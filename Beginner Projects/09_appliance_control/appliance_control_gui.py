"""
Project 9: Home Appliance Control - Python GUI
Toggle 4 relays (appliances) individually and see live status.

Requires: pip install pyserial
"""

import tkinter as tk
from tkinter import messagebox
import serial
import threading
import time

SERIAL_PORT = "COM3"
BAUD_RATE = 9600
APPLIANCE_NAMES = ["Living Room Light", "Fan", "Kitchen Light", "Pump"]


class ApplianceControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Home Appliance Control")
        self.root.geometry("380x420")
        self.ser = None
        self.running = False
        self.state = [False, False, False, False]

        top = tk.Frame(root)
        top.pack(pady=8)
        tk.Label(top, text="Serial Port:").pack(side="left")
        self.port_var = tk.StringVar(value=SERIAL_PORT)
        tk.Entry(top, textvariable=self.port_var, width=12).pack(side="left", padx=5)
        self.connect_btn = tk.Button(top, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack(side="left", padx=5)

        self.buttons = []
        for i, name in enumerate(APPLIANCE_NAMES):
            frame = tk.Frame(root, pady=10)
            frame.pack(fill="x", padx=20)
            tk.Label(frame, text=name, font=("Arial", 12), width=18, anchor="w").pack(side="left")
            btn = tk.Button(frame, text="OFF", width=8, bg="salmon",
                             command=lambda idx=i: self.toggle_relay(idx))
            btn.pack(side="right")
            self.buttons.append(btn)

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

    def toggle_relay(self, idx):
        if not (self.ser and self.ser.is_open):
            messagebox.showwarning("Not connected", "Connect to Arduino first")
            return
        new_state = not self.state[idx]
        cmd = f"R{idx+1}_{'ON' if new_state else 'OFF'}\n"
        self.ser.write(cmd.encode())

    def read_loop(self):
        while self.running:
            try:
                line = self.ser.readline().decode("utf-8", errors="ignore").strip()
                if line.startswith("R1:"):
                    self.root.after(0, self.update_ui, line)
            except Exception:
                pass

    def update_ui(self, line):
        # line like "R1:ON,R2:OFF,R3:ON,R4:OFF"
        parts = line.split(",")
        for i, part in enumerate(parts):
            if ":" in part:
                _, val = part.split(":")
                is_on = (val == "ON")
                self.state[i] = is_on
                self.buttons[i].config(
                    text="ON" if is_on else "OFF",
                    bg="lightgreen" if is_on else "salmon"
                )


if __name__ == "__main__":
    root = tk.Tk()
    app = ApplianceControlApp(root)
    root.mainloop()
