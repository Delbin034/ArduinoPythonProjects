"""
Project 4: Traffic Light Simulator - Tkinter Control Panel
Sends START/STOP to Arduino and mirrors the current light state visually.

Requires: pip install pyserial
"""

import tkinter as tk
from tkinter import messagebox
import serial
import threading
import time

SERIAL_PORT = "COM3"
BAUD_RATE = 9600


class TrafficLightApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Light Simulator")
        self.root.geometry("300x420")
        self.ser = None
        self.running = False

        top = tk.Frame(root)
        top.pack(pady=8)
        tk.Label(top, text="Serial Port:").pack(side="left")
        self.port_var = tk.StringVar(value=SERIAL_PORT)
        tk.Entry(top, textvariable=self.port_var, width=12).pack(side="left", padx=5)
        self.connect_btn = tk.Button(top, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack(side="left", padx=5)

        # Visual light box
        self.canvas = tk.Canvas(root, width=120, height=300, bg="black")
        self.canvas.pack(pady=15)
        self.red_circle = self.canvas.create_oval(20, 20, 100, 100, fill="gray20")
        self.yellow_circle = self.canvas.create_oval(20, 110, 100, 190, fill="gray20")
        self.green_circle = self.canvas.create_oval(20, 200, 100, 280, fill="gray20")

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Start", width=10, bg="lightgreen", command=lambda: self.send_cmd("START")).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Stop", width=10, bg="salmon", command=lambda: self.send_cmd("STOP")).grid(row=0, column=1, padx=5)

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
                if line in ("RED", "YELLOW", "GREEN", "OFF"):
                    self.root.after(0, self.update_lights, line)
            except Exception:
                pass

    def update_lights(self, state):
        colors = {
            "RED": ("red", "gray20", "gray20"),
            "YELLOW": ("gray20", "yellow", "gray20"),
            "GREEN": ("gray20", "gray20", "lime"),
            "OFF": ("gray20", "gray20", "gray20"),
        }
        r, y, g = colors[state]
        self.canvas.itemconfig(self.red_circle, fill=r)
        self.canvas.itemconfig(self.yellow_circle, fill=y)
        self.canvas.itemconfig(self.green_circle, fill=g)


if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficLightApp(root)
    root.mainloop()
