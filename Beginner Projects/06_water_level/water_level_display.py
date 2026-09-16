"""
Project 6: Water Level Monitor - Tank Level Display
Reads fill % from Arduino and draws an animated tank graphic.

Requires: pip install pyserial
"""

import tkinter as tk
from tkinter import messagebox
import serial
import threading
import time

SERIAL_PORT = "COM3"
BAUD_RATE = 9600


class WaterLevelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Level Monitor")
        self.root.geometry("300x450")
        self.ser = None
        self.running = False

        top = tk.Frame(root)
        top.pack(pady=8)
        tk.Label(top, text="Serial Port:").pack(side="left")
        self.port_var = tk.StringVar(value=SERIAL_PORT)
        tk.Entry(top, textvariable=self.port_var, width=12).pack(side="left", padx=5)
        self.connect_btn = tk.Button(top, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack(side="left", padx=5)

        # Tank canvas
        self.tank_height = 300
        self.tank_width = 150
        self.canvas = tk.Canvas(root, width=self.tank_width, height=self.tank_height, bg="white")
        self.canvas.pack(pady=15)
        self.canvas.create_rectangle(2, 2, self.tank_width - 2, self.tank_height - 2, outline="black", width=3)
        self.water_rect = self.canvas.create_rectangle(4, self.tank_height - 2, self.tank_width - 4, self.tank_height - 2, fill="deepskyblue")

        self.percent_label = tk.Label(root, text="-- %", font=("Arial", 18, "bold"))
        self.percent_label.pack(pady=10)

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
                if line.isdigit():
                    self.root.after(0, self.update_ui, int(line))
            except Exception:
                pass

    def update_ui(self, percent):
        percent = max(0, min(100, percent))
        fill_height = (percent / 100.0) * (self.tank_height - 4)
        y0 = self.tank_height - 2 - fill_height
        self.canvas.coords(self.water_rect, 4, y0, self.tank_width - 4, self.tank_height - 2)

        color = "deepskyblue"
        if percent < 20:
            color = "red"
        elif percent < 50:
            color = "orange"
        self.canvas.itemconfig(self.water_rect, fill=color)

        self.percent_label.config(text=f"{percent} %")


if __name__ == "__main__":
    root = tk.Tk()
    app = WaterLevelApp(root)
    root.mainloop()
