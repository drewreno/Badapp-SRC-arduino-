import cloudinary
import cloudinary.uploader
import os

# Configure Cloudinary with your credentials
cloudinary.config( 
  cloud_name = 'dsos2ijvk', 
  api_key = '357994591796565', 
  api_secret = 'JF3y6_QW-MW2HDCAPKsOtyqLLMg',
  secure = True
)

# Directory of the folder you want to upload
directory_path = 'badapple\\bmp_frames'  # Update this path as needed

# Function to upload a file to Cloudinary
def upload_file(file_path):
    try:
        response = cloudinary.uploader.upload(file_path, folder="bmp")
        print("Uploaded:", response.get('url'))
    except Exception as e:
        print("Error in uploading file:", file_path, "\nError:", e)

# Read files from the directory and upload them
for filename in os.listdir(directory_path):
    if filename.endswith(".bmp"):  # Update this if you have different file types
        file_path = os.path.join(directory_path, filename)
        upload_file(file_path)
