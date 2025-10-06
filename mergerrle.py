import os

def merge_rle_files(input_folder, output_file, delimiter=b'\x00\xFF\x00\xFF'):
    with open(output_file, 'wb') as out_file:
        for file_name in sorted(os.listdir(input_folder)):
            if file_name.lower().endswith('.rle'):
                input_path = os.path.join(input_folder, file_name)

                with open(input_path, 'rb') as in_file:
                    rle_data = in_file.read()
                    out_file.write(rle_data)

                # Write the delimiter after each file's data
                out_file.write(delimiter)

# Example usage
input_folder = "C:\\Users\\Andrew Cassarino\\OneDrive\\Desktop\\classes\\CODE\\badapple\\rle_frames"
output_file = "C:\\Users\\Andrew Cassarino\\OneDrive\\Desktop\\classes\\CODE\\badapple\\onerle"
merge_rle_files(input_folder, output_file)
