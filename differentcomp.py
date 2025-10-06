from PIL import Image
import os

def image_to_binary_array(image_path):
    """Convert an image to a binary array."""
    with Image.open(image_path) as img:
        img = img.convert('L')  # Convert to grayscale
        threshold = 128
        return [[1 if img.getpixel((x, y)) < threshold else 0 for x in range(img.width)] for y in range(img.height)]

def find_changes(prev_frame, curr_frame):
    """Find differences between the current frame and the previous frame."""
    changes = []
    for y in range(len(curr_frame)):
        for x in range(len(curr_frame[y])):
            if curr_frame[y][x] != prev_frame[y][x]:
                changes.append((x, y, curr_frame[y][x]))
    return changes

def encode_frame(changes):
    """Encode the changes into a string format."""
    encoded = f'{len(changes):02d}'  # Frame header with number of changes
    for change in changes:
        x, y, value = change
        encoded += f'{x:02d}{y:02d}{value}'
    return encoded

def encode_video(frames_folder, output_path):
    """Encode a sequence of frames from a specified folder and write to a file."""
    encoded_video = ""
    previous_frame = None
    frame_files = sorted(os.listdir(frames_folder))  # Ensure files are sorted

    for frame_file in frame_files:
        frame_path = os.path.join(frames_folder, frame_file)
        current_frame = image_to_binary_array(frame_path)

        if previous_frame is None:
            # For the first frame, encode all pixels
            changes = [(x, y, pixel) for y, row in enumerate(current_frame) for x, pixel in enumerate(row)]
        else:
            changes = find_changes(previous_frame, current_frame)

        encoded_frame = encode_frame(changes)
        encoded_video += encoded_frame + ";"
        previous_frame = current_frame

    # Write the encoded video to a text file
    with open(output_path, 'w') as file:
        file.write(encoded_video)

    return encoded_video

# Specify your frames folder
frames_folder = r"C:\\Users\\Andrew Cassarino\\OneDrive\\Desktop\\classes\\CODE\\badapple\\frames"

# Specify the output path for the encoded video
output_path = r"C:\\Users\\Andrew Cassarino\\OneDrive\\Desktop\\classes\\CODE\\badapple\\bettercomp.txt"

# Encode the video and write to file
encoded_video = encode_video(frames_folder, output_path)
