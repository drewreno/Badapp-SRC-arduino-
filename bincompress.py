import os

# Input folder containing BMP and BIN files
input_folder = "badapple\\bin"  # Replace with the path to your input folder
bmp_bin_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".bmp") or f.lower().endswith(".bin")]

# Output folder for binary files
output_folder = "badapple\\maxbin"  # Replace with the path to your output folder

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Function to write a marker/header to separate images
def write_marker(file):
    marker = b"\xFF\xD8"  # Example marker/header (you can customize)
    file.write(marker)

# Split BMP/BIN files into groups of 100 files
num_files_per_output = 15
output_counter = 1
current_files = []

for bmp_bin_file in bmp_bin_files:
    current_files.append(bmp_bin_file)

    if len(current_files) >= num_files_per_output:
        output_file = os.path.join(output_folder, f"combined_images_{output_counter}.bin")
        
        # Open the output binary file in binary write mode
        with open(output_file, "wb") as output:
            for bmp_bin_file in current_files:
                # Write a marker/header to separate images
                write_marker(output)

                # Open and read each BMP/BIN file
                with open(os.path.join(input_folder, bmp_bin_file), "rb") as file:
                    file_data = file.read()

                # Write the file data to the output file
                output.write(file_data)

        output_counter += 1
        current_files = []

# If there are any remaining files
if current_files:
    output_file = os.path.join(output_folder, f"combined_images_{output_counter}.bin")
    
    # Open the output binary file in binary write mode
    with open(output_file, "wb") as output:
        for bmp_bin_file in current_files:
            # Write a marker/header to separate images
            write_marker(output)

            # Open and read each BMP/BIN file
            with open(os.path.join(input_folder, bmp_bin_file), "rb") as file:
                file_data = file.read()

            # Write the file data to the output file
            output.write(file_data)

print(f"Combined BMP/BIN files from {input_folder} into binary files in {output_folder}")
