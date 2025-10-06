def binary_to_xbm(binary_file, xbm_file, width, height):
    try:
        with open(binary_file, 'rb') as binary_f:
            binary_data = binary_f.read()

        # Calculate the number of bytes needed per row (including padding)
        bytes_per_row = width // 8
        if width % 8 != 0:
            bytes_per_row += 1

        # Create the X BitMap (XBM) header
        xbm_header = f"#define {xbm_file[:-4]}_width {width}\n"
        xbm_header += f"#define {xbm_file[:-4]}_height {height}\n"
        xbm_header += f"static unsigned char {xbm_file[:-4]}_bits[] = {{\n"

        # Write binary data as bytes, taking care of padding
        for i in range(0, len(binary_data), bytes_per_row):
            byte_chunk = binary_data[i:i + bytes_per_row]
            xbm_header += "0x" + ", 0x".join(f"{byte:02X}" for byte in byte_chunk) + ",\n"

        # Close the XBM data array and add a semicolon
        xbm_header += "};"

        # Write the X BitMap (XBM) data to the output file
        with open(xbm_file, 'w') as xbm_f:
            xbm_f.write(xbm_header)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    binary_file = r"C:\\Users\\Andrew Cassarino\\Downloads\\frame_145.bin"
    xbm_file = r"C:\\Users\\Andrew Cassarino\\Downloads\\frame_145.xbm"
    image_width = 86  # Adjust as per your original image dimensions
    image_height = 64  # Adjust as per your original image dimensions

    binary_to_xbm(binary_file, xbm_file, image_width, image_height)
    print(f"XBM file saved to {xbm_file}")
