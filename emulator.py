import socket
import time
import json
import h5py
import numpy as np

# Constants
IP = "intentlab.iitk.ac.in"
PORT = 9050
DELAY = 1

# Load dataset
dataset = h5py.File("./training_data_env1.h5", "r")
csi = np.array(dataset["channels/real"]).T + 1j * np.array(dataset["channels/imag"]).T
rssi = np.array(dataset["rssi"]).T

avg_magnitude = np.mean(np.abs(csi), axis=(1, 2))  # shape: (samples, 6)
avg_phase = np.mean(np.angle(csi), axis=(1, 2))    # shape: (samples, 6)

# Initialize socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Iterate through samples
for i in range(len(rssi)):

    wifi_data = {
        "id": i,
        "rssi": rssi[i].tolist(),
        "csi_mag": avg_magnitude[i].tolist(),
        "csi_phase": avg_phase[i].tolist()
    }

    message = json.dumps(wifi_data).encode('utf-8')
    sock.sendto(message, (IP, PORT))
    print(f"Sent sample {i}")
    time.sleep(DELAY)
