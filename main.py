import tkinter as tk
from tkinter import Scrollbar, Text, END, RIGHT, Y, BOTH, LEFT, X
import tkinter.font as tkFont 
import subprocess
import socket
import speedtest
import platform
import threading


# Function to ping a host
def ping_host():
    host = e1.get()
    if host:
        output_text.insert(END, f"Pinging {host}...\n")
        param = "-n" if platform.system().lower() == "windows" else "-c"
        try:
            result = subprocess.check_output(f"ping {param} 5 {host}", shell=True, text=True)
            output_text.insert(END, result + "\n")
        except subprocess.CalledProcessError:
            output_text.insert(END, f"Failed to ping {host}\n")
    else:
        output_text.insert(END, "Please enter a Host/IP to ping.\n")

# Function to check internet connectivity
def check_internet():
    output_text.insert(END, "Checking internet connection...\n")
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        output_text.insert(END, "Internet Connection: Active\n")
    except OSError as e:
        output_text.insert(END, f"Internet Connection: Inactive ({e})\n")

# Function to display IP configuration
def show_ip_config():
    output_text.insert(END, "Fetching IP Configuration...\n")
    command = "ipconfig" if platform.system().lower() == "windows" else "ifconfig"
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        output_text.insert(END, result + "\n")
    except subprocess.CalledProcessError:
        output_text.insert(END, "Error fetching IP configuration.\n")

# Function to perform speed test
def speed_test():
    def run_speed_test():
        output_text.insert(END, "Running speed test...\n")
        try:
            st = speedtest.Speedtest()
            download_speed = st.download() / 1_000_000  # Mbps
            upload_speed = st.upload() / 1_000_000
            output_text.insert(END, f"Download Speed: {download_speed:.2f} Mbps\n")
            output_text.insert(END, f"Upload Speed: {upload_speed:.2f} Mbps\n")
        except Exception as e:
            output_text.insert(END, f"Speed test failed: {e}\n")

    threading.Thread(target=run_speed_test).start()

def clear_results():
    output_text.delete(1.0, END)

# GUI Setup
root = tk.Tk()
root.title("Networking Toolkit")
root.geometry('700x500')

font = tkFont.Font(family="Helvetica", size=15, weight="bold")
lbl = tk.Label(root, text="Networking Toolkit", font=font)
lbl.pack(pady=10)

# Button Frame
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

button1 = tk.Button(button_frame, text="Check Internet", command=check_internet)
button1.grid(row=0, column=0, padx=10, pady=5)
button1.config(bg="blue")

button2 = tk.Button(button_frame, text="Speed Test", command=speed_test)
button2.grid(row=0, column=1, padx=10, pady=5)
button2.config(bg="red")

button3 = tk.Button(button_frame, text="Show IP Config", command=show_ip_config)
button3.grid(row=0, column=2, padx=10, pady=5)
button3.config(bg="purple")

# Ping Section
ping_frame = tk.Frame(root)
ping_frame.pack(pady=10)

lbl_ping = tk.Label(ping_frame, text="Host/IP to Ping:")
lbl_ping.grid(row=0, column=0, padx=5)


e1 = tk.Entry(ping_frame)
e1.grid(row=0, column=1, padx=5)

button4 = tk.Button(ping_frame, text="Ping", command=ping_host)
button4.grid(row=0, column=2, padx=5)
button4.config(bg="lightgreen")

button5 = tk.Button(ping_frame, text="Clear Results", command=clear_results)
button5.grid(row=0, column=3, padx=5)
button5.config(bg="grey")
# Output Box
frame_output = tk.Frame(root)
frame_output.pack(fill=BOTH, expand=True, padx=10, pady=5)

scrollbar = Scrollbar(frame_output)
scrollbar.pack(side=RIGHT, fill=Y)

output_text = Text(frame_output, wrap='word', yscrollcommand=scrollbar.set)
output_text.pack(fill=BOTH, expand=True)

scrollbar.config(command=output_text.yview)

root.mainloop()
