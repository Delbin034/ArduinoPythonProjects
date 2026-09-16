"""
Project 2: Temperature & Humidity Monitor - Live Graph Dashboard
Reads "temperature,humidity" from Arduino and plots a live rolling graph
using matplotlib embedded inside Tkinter.

Requires: pip install pyserial matplotlib
"""

import tkinter as tk
from tkinter import messagebox
import serial
import threading
import time
from collections import deque

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

SERIAL_PORT = "COM3"
BAUD_RATE = 9600
MAX_POINTS = 50


class TempHumidityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Temperature & Humidity Monitor")
        self.root.geometry("700x500")
        self.ser = None
        self.running = False

        self.temps = deque(maxlen=MAX_POINTS)
        self.hums = deque(maxlen=MAX_POINTS)
        self.xdata = deque(maxlen=MAX_POINTS)
        self.counter = 0

        top = tk.Frame(root)
        top.pack(pady=8)
        tk.Label(top, text="Serial Port:").pack(side="left")
        self.port_var = tk.StringVar(value=SERIAL_PORT)
        tk.Entry(top, textvariable=self.port_var, width=12).pack(side="left", padx=5)
        self.connect_btn = tk.Button(top, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack(side="left", padx=5)

        self.current_label = tk.Label(root, text="Temp: -- °C   Humidity: -- %", font=("Arial", 13, "bold"))
        self.current_label.pack(pady=5)

        self.fig = Figure(figsize=(6.5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.line_temp, = self.ax.plot([], [], label="Temperature (°C)", color="red")
        self.line_hum, = self.ax.plot([], [], label="Humidity (%)", color="blue")
        self.ax.legend(loc="upper right")
        self.ax.set_xlabel("Sample #")

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

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
                if "," in line and "ERR" not in line:
                    t_str, h_str = line.split(",")
                    t = float(t_str)
                    h = float(h_str)
                    self.root.after(0, self.update_ui, t, h)
            except Exception:
                pass

    def update_ui(self, t, h):
        self.counter += 1
        self.xdata.append(self.counter)
        self.temps.append(t)
        self.hums.append(h)

        self.current_label.config(text=f"Temp: {t:.1f} °C   Humidity: {h:.1f} %")

        self.line_temp.set_data(self.xdata, self.temps)
        self.line_hum.set_data(self.xdata, self.hums)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = TempHumidityApp(root)
    root.mainloop()
