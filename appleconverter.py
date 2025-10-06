import cv2
import numpy as np
import os
from tqdm import tqdm

# Specify the full path of your video file and destination folder
video_path = 'C:\\Users\\Andrew Cassarino\\OneDrive\\Desktop\\classes\\CODE\\badapple\\badapple.mp4'  # Replace with your video file path
output_folder = 'C:\\Users\\Andrew Cassarino\\OneDrive\\Desktop\\classes\\CODE\\badapple\\frames'   # Replace with your desired folder path

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the video
cap = cv2.VideoCapture(video_path)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Get the total number of frames

# Loop through each frame with a progress bar
for i in tqdm(range(frame_count), desc="Processing Frames"):
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert to binary
    _, binary_frame = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY)

    # Save the frame to the output folder
    cv2.imwrite(os.path.join(output_folder, f'frame_{i}.png'), binary_frame)

cap.release()
