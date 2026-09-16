"""
Project 10: Serial Sensor Data Logger - CSV/Excel Logger
Reads "sensor1,sensor2" (or any CSV of numbers) from Arduino, displays
live values, and logs every reading with a timestamp to a CSV file.

To export as .xlsx instead of .csv, install openpyxl and use
export_to_excel() at the bottom (button included).

Requires: pip install pyserial openpyxl
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import serial
import threading
import time
import csv
import datetime

SERIAL_PORT = "COM3"
BAUD_RATE = 9600


class DataLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Sensor Data Logger")
        self.root.geometry("450x420")
        self.ser = None
        self.connected = False
        self.logging = False
        self.log_rows = []  # (timestamp, sensor1, sensor2, ...)

        top = tk.Frame(root)
        top.pack(pady=8)
        tk.Label(top, text="Serial Port:").pack(side="left")
        self.port_var = tk.StringVar(value=SERIAL_PORT)
        tk.Entry(top, textvariable=self.port_var, width=12).pack(side="left", padx=5)
        self.connect_btn = tk.Button(top, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack(side="left", padx=5)

        self.live_label = tk.Label(root, text="Live: --", font=("Arial", 13, "bold"))
        self.live_label.pack(pady=10)

        ctrl_frame = tk.Frame(root)
        ctrl_frame.pack(pady=5)
        self.log_btn = tk.Button(ctrl_frame, text="Start Logging", bg="lightgreen", command=self.toggle_logging)
        self.log_btn.pack(side="left", padx=5)
        tk.Button(ctrl_frame, text="Export CSV", command=self.export_csv).pack(side="left", padx=5)
        tk.Button(ctrl_frame, text="Export Excel", command=self.export_excel).pack(side="left", padx=5)

        tk.Label(root, text="Recent Readings", font=("Arial", 11, "bold")).pack(pady=(15, 0))
        self.log_box = tk.Listbox(root, width=50, height=14)
        self.log_box.pack(pady=5)

    def toggle_connection(self):
        if not self.connected:
            try:
                self.ser = serial.Serial(self.port_var.get(), BAUD_RATE, timeout=1)
                time.sleep(2)
                self.connected = True
                self.connect_btn.config(text="Disconnect")
                threading.Thread(target=self.read_loop, daemon=True).start()
            except serial.SerialException as e:
                messagebox.showerror("Connection Error", str(e))
        else:
            self.connected = False
            self.logging = False
            if self.ser:
                self.ser.close()
            self.connect_btn.config(text="Connect")

    def toggle_logging(self):
        self.logging = not self.logging
        self.log_btn.config(
            text="Stop Logging" if self.logging else "Start Logging",
            bg="salmon" if self.logging else "lightgreen"
        )

    def read_loop(self):
        while self.connected:
            try:
                line = self.ser.readline().decode("utf-8", errors="ignore").strip()
                if "," in line:
                    values = line.split(",")
                    self.root.after(0, self.handle_reading, values)
            except Exception:
                pass

    def handle_reading(self, values):
        self.live_label.config(text="Live: " + ", ".join(values))
        if self.logging:
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row = [ts] + values
            self.log_rows.append(row)
            self.log_box.insert(tk.END, f"{ts}  ->  {', '.join(values)}")
            self.log_box.see(tk.END)

    def export_csv(self):
        if not self.log_rows:
            messagebox.showinfo("No data", "No logged data to export yet")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            n_sensors = len(self.log_rows[0]) - 1
            writer.writerow(["timestamp"] + [f"sensor{i+1}" for i in range(n_sensors)])
            writer.writerows(self.log_rows)
        messagebox.showinfo("Exported", f"Saved to {path}")

    def export_excel(self):
        if not self.log_rows:
            messagebox.showinfo("No data", "No logged data to export yet")
            return
        try:
            import openpyxl
        except ImportError:
            messagebox.showerror("Missing package", "Run: pip install openpyxl")
            return
        path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not path:
            return
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "SensorLog"
        n_sensors = len(self.log_rows[0]) - 1
        ws.append(["timestamp"] + [f"sensor{i+1}" for i in range(n_sensors)])
        for row in self.log_rows:
            ws.append(row)
        wb.save(path)
        messagebox.showinfo("Exported", f"Saved to {path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DataLoggerApp(root)
    root.mainloop()
