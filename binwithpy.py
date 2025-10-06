import os
from PIL import Image
from tqdm import tqdm

IMAGE_WIDTH = 86
IMAGE_HEIGHT = 64

def process_bmp_files(input_folder, output_folder):
    # Create output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    bmp_files = [f for f in os.listdir(input_folder) if f.endswith(".bmp")]
    for filename in tqdm(bmp_files, desc="Processing BMP Files"):
        bmp_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.bin')
        print_binary_data(bmp_path, output_path)

def print_binary_data(bmp_path, output_path):
    with Image.open(bmp_path) as img, open(output_path, 'wb') as out_file:
        img = img.convert('1')  # Convert to black and white

        for y in range(IMAGE_HEIGHT):
            binary_row = ''
            for x in range(IMAGE_WIDTH):
                pixel = img.getpixel((x, y))
                binary_row += '1' if pixel else '0'
            binary_row_bytes = int(binary_row, 2).to_bytes((len(binary_row) + 7) // 8, byteorder='big')
            out_file.write(binary_row_bytes)
            if y < IMAGE_HEIGHT - 1:  # Add new line after each row except the last
                out_file.write(b'\n')

if __name__ == "__main__":
    input_folder = "badapple\\bmp_frames"
    output_folder = "badapple\\bin"
    process_bmp_files(input_folder, output_folder)
