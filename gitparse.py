import os
import subprocess
from tqdm import tqdm  # Import tqdm for the progress bar

GITHUB_REPO_URL = 'https://github.com/drewreno/badapp.git'
FOLDER_PATH = 'C:\\Users\\Andrew Cassarino\\OneDrive\\Desktop\\classes\\CODE\\badapple\\xbm'
REPO_ROOT_PATH = 'C:\\Users\\Andrew Cassarino\\OneDrive\\Desktop\\classes\\CODE\\badapple\\xbm'

def divide_into_chunks(files, num_chunks=3):
    if not files:
        print("No files found in the folder.")
        return []

    chunk_size = max(1, len(files) // num_chunks)
    return [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

def configure_git_line_endings(repo_root_path):
    os.chdir(repo_root_path)  # Change working directory to the repository root

    if not os.path.exists('.git'):
        print("Initializing Git...")
        subprocess.run(["git", "init"])  # Initialize Git repository

    # Configure Git to handle line endings consistently
    subprocess.run(["git", "config", "core.autocrlf", "false"])
    subprocess.run(["git", "config", "core.eol", "lf"])

def initialize_git(repo_root_path, github_repo_url):
    configure_git_line_endings(repo_root_path)

    if github_repo_url:
        subprocess.run(["git", "remote", "add", "origin", github_repo_url])  # Add GitHub repository as remote
        subprocess.run(["git", "fetch", "--all"])  # Fetch GitHub repository data

def upload_files(files, folder_path, repo_root_path, github_repo_url=None):
    initialize_git(repo_root_path, github_repo_url)

    os.chdir(repo_root_path)  # Change working directory to the repository root

    # Use tqdm to create a progress bar
    with tqdm(total=len(files), desc="Uploading Files") as pbar:
        for filename in files:
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                # Add the file to Git
                subprocess.run(["git", "add", file_path])
                pbar.update(1)  # Update the progress bar

    # Commit and push
    subprocess.run(["git", "commit", "-m", "Uploading files"])
    print("Uploading to GitHub...")
    subprocess.run(["git", "push", "origin", "main"])  # Assuming you want to push to the 'main' branch

def main():
    files = [f for f in os.listdir(FOLDER_PATH) if os.path.isfile(os.path.join(FOLDER_PATH, f))]
    upload_files(files, FOLDER_PATH, REPO_ROOT_PATH, GITHUB_REPO_URL)

if __name__ == "__main__":
    main()
