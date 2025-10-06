from PIL import Image
import os
from tqdm import tqdm

# Folder where the PNG frames are stored
input_folder = 'C:\\Users\\Andrew Cassarino\\OneDrive\\Desktop\\classes\\CODE\\badapple\\frames'

# Folder where the BMP frames will be saved
output_folder = 'C:\\Users\\Andrew Cassarino\\OneDrive\\Desktop\\classes\\CODE\\badapple\\bmp_frames'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get the list of frame files
frame_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]

# Process each frame
for frame_file in tqdm(frame_files, desc="Converting Frames"):
    # Construct the full file paths
    input_path = os.path.join(input_folder, frame_file)
    output_path = os.path.join(output_folder, frame_file.replace('.png', '.bmp'))

    # Open the image
    image = Image.open(input_path)

    # Convert the image to 1-bit pixels, black and white
    image = image.convert('1')

    # Save the image as BMP
    image.save(output_path)

print("Conversion completed!")
