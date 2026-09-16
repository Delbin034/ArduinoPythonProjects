"""
Project 8: Weather Station - Dashboard
Reads "temperature,humidity,light,rain" CSV from Arduino and shows a
combined weather summary with simple condition icons (text-based).

Requires: pip install pyserial
"""

import tkinter as tk
from tkinter import messagebox
import serial
import threading
import time

SERIAL_PORT = "COM3"
BAUD_RATE = 9600


class WeatherStationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Station Dashboard")
        self.root.geometry("400x420")
        self.ser = None
        self.running = False

        top = tk.Frame(root)
        top.pack(pady=8)
        tk.Label(top, text="Serial Port:").pack(side="left")
        self.port_var = tk.StringVar(value=SERIAL_PORT)
        tk.Entry(top, textvariable=self.port_var, width=12).pack(side="left", padx=5)
        self.connect_btn = tk.Button(top, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack(side="left", padx=5)

        self.condition_label = tk.Label(root, text="--", font=("Arial", 40))
        self.condition_label.pack(pady=15)

        self.temp_label = tk.Label(root, text="Temperature: -- °C", font=("Arial", 13))
        self.temp_label.pack(pady=3)
        self.hum_label = tk.Label(root, text="Humidity: -- %", font=("Arial", 13))
        self.hum_label.pack(pady=3)
        self.light_label = tk.Label(root, text="Light: -- %", font=("Arial", 13))
        self.light_label.pack(pady=3)
        self.rain_label = tk.Label(root, text="Rain: --", font=("Arial", 13))
        self.rain_label.pack(pady=3)

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
                parts = line.split(",")
                if len(parts) == 4 and "ERR" not in line:
                    t, h, light, rain = parts
                    self.root.after(0, self.update_ui, float(t), float(h), int(light), int(rain))
            except Exception:
                pass

    def update_ui(self, temp, hum, light, rain):
        self.temp_label.config(text=f"Temperature: {temp:.1f} °C")
        self.hum_label.config(text=f"Humidity: {hum:.1f} %")
        self.light_label.config(text=f"Light: {light} %")
        self.rain_label.config(text=f"Rain: {'Raining' if rain else 'Dry'}")

        if rain:
            icon = "🌧️"
        elif light < 30:
            icon = "☁️"
        elif light > 70:
            icon = "☀️"
        else:
            icon = "⛅"
        self.condition_label.config(text=icon)


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherStationApp(root)
    root.mainloop()
