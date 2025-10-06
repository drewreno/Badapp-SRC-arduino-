import os
from PIL import Image

def convert_bmp_to_xbm(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith('.bmp'):
            # Create file paths
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, os.path.splitext(filename)[0] + '.xbm')

            # Open the image and convert
            with Image.open(input_path) as img:
                # Convert image to 1-bit pixels (black and white)
                img = img.convert('1')
                xbm_data = img.tobitmap()

                # Write to xbm file
                with open(output_path, 'wb') as f:
                    f.write(xbm_data)

# Example usage
input_dir = 'badapple\\bmp_frames'  # Replace with your BMP files directory
output_dir = 'badapple\\xbm' # Replace with your desired output directory
convert_bmp_to_xbm(input_dir, output_dir)
