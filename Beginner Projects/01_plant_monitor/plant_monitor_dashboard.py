"""
Project 1: Plant Monitoring System - Python Tkinter Dashboard
Reads "moisture,light" CSV lines from Arduino over serial and displays
live progress bars + status text.

Requires: pip install pyserial
"""

import tkinter as tk
from tkinter import ttk, messagebox
import serial
import threading
import time

SERIAL_PORT = "COM3"      # change to your port, e.g. "/dev/ttyUSB0" on Linux/Mac
BAUD_RATE = 9600


class PlantMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Plant Monitoring Dashboard")
        self.root.geometry("420x320")
        self.ser = None
        self.running = False

        tk.Label(root, text="Plant Monitoring System", font=("Arial", 16, "bold")).pack(pady=10)

        port_frame = tk.Frame(root)
        port_frame.pack(pady=5)
        tk.Label(port_frame, text="Serial Port:").pack(side="left")
        self.port_var = tk.StringVar(value=SERIAL_PORT)
        tk.Entry(port_frame, textvariable=self.port_var, width=12).pack(side="left", padx=5)
        self.connect_btn = tk.Button(port_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack(side="left", padx=5)

        tk.Label(root, text="Soil Moisture", font=("Arial", 12)).pack(pady=(20, 0))
        self.soil_bar = ttk.Progressbar(root, length=300, maximum=100)
        self.soil_bar.pack(pady=5)
        self.soil_label = tk.Label(root, text="-- %", font=("Arial", 12, "bold"))
        self.soil_label.pack()

        tk.Label(root, text="Light Level", font=("Arial", 12)).pack(pady=(20, 0))
        self.light_bar = ttk.Progressbar(root, length=300, maximum=100)
        self.light_bar.pack(pady=5)
        self.light_label = tk.Label(root, text="-- %", font=("Arial", 12, "bold"))
        self.light_label.pack()

        self.status_label = tk.Label(root, text="Disconnected", fg="red")
        self.status_label.pack(pady=15)

    def toggle_connection(self):
        if not self.running:
            try:
                self.ser = serial.Serial(self.port_var.get(), BAUD_RATE, timeout=1)
                time.sleep(2)
                self.running = True
                self.connect_btn.config(text="Disconnect")
                self.status_label.config(text="Connected", fg="green")
                threading.Thread(target=self.read_loop, daemon=True).start()
            except serial.SerialException as e:
                messagebox.showerror("Connection Error", str(e))
        else:
            self.running = False
            if self.ser:
                self.ser.close()
            self.connect_btn.config(text="Connect")
            self.status_label.config(text="Disconnected", fg="red")

    def read_loop(self):
        while self.running:
            try:
                line = self.ser.readline().decode("utf-8", errors="ignore").strip()
                if "," in line:
                    soil_str, light_str = line.split(",")
                    soil = int(soil_str)
                    light = int(light_str)
                    self.root.after(0, self.update_ui, soil, light)
            except Exception:
                pass

    def update_ui(self, soil, light):
        self.soil_bar["value"] = soil
        self.soil_label.config(text=f"{soil} %")
        self.light_bar["value"] = light
        self.light_label.config(text=f"{light} %")


if __name__ == "__main__":
    root = tk.Tk()
    app = PlantMonitorApp(root)
    root.mainloop()
