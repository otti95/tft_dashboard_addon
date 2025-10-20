import serial
import psutil
import time
import subprocess
import socket
from datetime import datetime

# === Einstellungen ===
PORT = "/dev/ttyUSB0"   # Arduino
BAUD = 9600

def get_temperature():
    try:
        # Raspberry Pi CPU-Temperatur
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_str = f.readline().strip()
            return float(temp_str) / 1000.0
    except:
        return 0.0

def get_cpu_freq():
    try:
        freq = psutil.cpu_freq().current
        return int(freq)
    except:
        return 0

def get_ram_usage():
    mem = psutil.virtual_memory()
    return mem.used // (1024 * 1024), mem.total // (1024 * 1024)

def get_disk_usage():
    disk = psutil.disk_usage("/")
    return disk.percent

def get_network_status():
    try:
        start = time.time()
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        ping_ms = int((time.time() - start) * 1000)
        return "OK", ping_ms
    except:
        return "OFF", 0

def get_power_usage():
    # Dummywert, später anpassen falls echte Messung möglich
    return 12.5

# --- serielle Verbindung ---
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)  # Arduino bereit machen

while True:
    cpu = psutil.cpu_percent()
    temp = get_temperature()
    freq = get_cpu_freq()
    ram_used, ram_total = get_ram_usage()
    disk = get_disk_usage()
    power = get_power_usage()
    net, ping = get_network_status()
    now = datetime.now().strftime("%H:%M")

    msg = f"CPU:{cpu:.1f}%,TEMP:{temp:.1f}C,FREQ:{freq}MHz,RAM:{ram_used}/{ram_total}MB,DISK:{disk}%,POWER:{power:.1f}W,NET:{net} ({ping}ms),TIME:{now}\n"
    ser.write(msg.encode("utf-8"))
    time.sleep(5)
