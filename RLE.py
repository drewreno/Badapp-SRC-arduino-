import os
import struct

def encode_rle(data):
    encoding = []
    prev_char = data[0]
    count = 1

    for char in data[1:]:
        if char == prev_char:
            count += 1
        else:
            encoding.append((count, prev_char))
            prev_char = char
            count = 1
    encoding.append((count, prev_char))
    return encoding

def compress_bmp(input_file, output_file):
    try:
        with open(input_file, 'rb') as bmp:
            bmp.seek(54)  # Skip the BMP header
            data = bmp.read()

        compressed_data = encode_rle(data)

        with open(output_file, 'wb') as out:
            for count, value in compressed_data:
                out.write(bytes([count]))  # Write count
                out.write(bytes([value]))  # Write pixel value

        print(f"Successfully compressed: {input_file} -> {output_file}")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

def compress_folder(input_folder, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith('.bmp'):
            input_file = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder, file_name.replace('.bmp', '.rle'))
            compress_bmp(input_file, output_file)

# Example usage
input_folder = 'C:\\Users\\Andrew Cassarino\\OneDrive\\Desktop\\classes\\CODE\\badapple\\bmp_frames'
output_folder = 'C:\\Users\\Andrew Cassarino\\OneDrive\\Desktop\\classes\\CODE\\badapple\\rle_frames'
compress_folder(input_folder, output_folder)
