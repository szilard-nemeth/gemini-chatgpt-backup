import subprocess
import os
import re
import time

# --- CONFIGURATION ---
# Path to your Chrome Profile (Example for Windows: r'C:\Users\Name\AppData\Local\Google\Chrome\User Data')
# For Mac: '~/Library/Application Support/Google/Chrome'
CHROME_DATA_DIR = r'C:\Users\YourName\AppData\Local\Google\Chrome\User Data'
PROFILE_NAME = 'Default'  # Or 'Profile 1', etc.
OUTPUT_DIR = './gemini_exports'
LINKS_FILE = '/Users/snemeth/development/my-repos/gemini-chatgpt-backup/gemini-export/input.txt'

# Create output folder if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def sanitize_filename(filename):
    """Removes illegal characters for file systems."""
    return re.sub(r'[\\/*?:"<>|]', "", filename).strip()

def download_gemini_link(url):
    print(f"Processing: {url}")

    # We use --dump-content first to find the title, or just let SingleFile
    # handle the naming via its internal placeholder system.
    # The --filename-template "{page-title}.html" is the key here.

    command = [
        'single-file',
        url,
        '--browser-executable-path', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', # Update path if needed
        '--browser-args', f'--user-data-dir="{CHROME_DATA_DIR}" --profile-directory="{PROFILE_NAME}"',
        '--filename-template', '{page-title}.html',
        '--output-directory', OUTPUT_DIR,
        '--browser-wait-until', 'networkidle0',
        '--browser-wait-delay', '3000' # Give Gemini time to render the chat blocks
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Successfully saved content from {url}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {url}: {e}")

def main():
    if not os.path.exists(LINKS_FILE):
        print(f"Error: {LINKS_FILE} not found.")
        return

    with open(LINKS_FILE, 'r') as f:
        links = [line.strip() for line in f if line.strip()]

    for link in links:
        download_gemini_link(link)
        time.sleep(2) # Short pause to avoid rate limiting

if __name__ == "__main__":
    main()