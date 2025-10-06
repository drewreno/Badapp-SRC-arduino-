from PIL import Image

def bmp_to_binary_file(image_path, output_file):
    try:
        # Open the BMP image using Pillow
        img = Image.open(image_path)

        # Check if the image is 1-bit (mode '1')
        if img.mode != '1':
            raise ValueError("The image is not 1-bit BMP")

        # Get the pixel data without padding
        pixel_data = img.tobytes()

        # Open a binary file for writing in binary mode ('wb')
        with open(output_file, 'wb') as f:
            f.write(pixel_data)

        print(f"Binary data saved to {output_file}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    bmp_file = r"C:\\Users\\Andrew Cassarino\\OneDrive\\Desktop\\classes\\CODE\\badapple\\bmp_frames\\frame_145.bmp"
    output_binary_file = r"C:\\Users\\Andrew Cassarino\\Downloads\\frame_145.bin"

    bmp_to_binary_file(bmp_file, output_binary_file)