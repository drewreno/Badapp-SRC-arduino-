import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.signal import find_peaks, iirnotch, lfilter

# Constants
CHUNK_SIZE = 4096 # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate (44.1kHz)
BUFFER_LENGTH = 3  # Length of the buffer in seconds
POS_THRESHOLD = 2000  # Positive threshold for detecting a peak
PEAK_DISTANCE = int(RATE * 0.2)  # Minimum samples between peaks (0.3 seconds)
F0 = 60  # Frequency to be removed from signal, Hz
Q = 30.0  # Quality factor for notch filter

# Initialize PyAudio
p = pyaudio.PyAudio()

# Function to list and choose the audio input device
def select_input_device():
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    
    # List all available devices
    for i in range(0, num_devices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    # Choose the desired device
    dev_index = int(input("Choose the device index: "))
    return dev_index

# Ask user to select the input device
device_index = select_input_device()

# Open stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=CHUNK_SIZE)

# Design notch filter
b_notch, a_notch = iirnotch(F0, Q, RATE)

# Create matplotlib figure and axis
fig, ax = plt.subplots(figsize=(12, 6))
x = np.linspace(0, BUFFER_LENGTH, RATE * BUFFER_LENGTH)
data_buffer = np.zeros(RATE * BUFFER_LENGTH, dtype=np.int16)
line, = ax.plot(x, data_buffer)
peak_plot, = ax.plot([], [], 'r*', markersize=10)  # Plot for indicating peaks
ax.set_ylim(-5000, 10000)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
time_text = ax.text(0.95, 0.95, '', horizontalalignment='right', verticalalignment='top', transform=ax.transAxes)

def update(frame):
    global data_buffer
    new_data = -np.frombuffer(stream.read(CHUNK_SIZE), dtype=np.int16)
    
    # Apply the notch filter to the new data
    filtered_data = lfilter(b_notch, a_notch, new_data)
    
    data_buffer = np.append(data_buffer, filtered_data)[-RATE * BUFFER_LENGTH:]
    line.set_ydata(data_buffer)

    # Find peaks using amplitude threshold and ensuring they are sufficiently spaced
    peaks, _ = find_peaks(data_buffer, height=POS_THRESHOLD, distance=PEAK_DISTANCE)
    peak_times = x[peaks]  # Convert peak indices to time
    peak_amplitudes = data_buffer[peaks]  # Get peak amplitudes
    
    # Update the plot for peaks
    peak_plot.set_data(peak_times, peak_amplitudes)

    # Calculate BPM if enough peaks are found
    if len(peaks) > 1:
        peak_intervals = np.diff(peaks) / RATE
        average_rr_interval = np.mean(peak_intervals)
        bpm = 60 / average_rr_interval if average_rr_interval > 0 else 0
        time_text.set_text(f'BPM: {bpm:.1f}')
    else:
        time_text.set_text('BPM: calculating...')

    return line, peak_plot, time_text

# Create animation
ani = FuncAnimation(fig, update, blit=True, interval=50)

# Display the plot
plt.show()

# Close the stream
stream.stop_stream()
stream.close()
p.terminate()
