"""
Downloads data files from a Google Drive folder to the local data directory.
This script uses the gdown library to download all files from a specified 
Google Drive folder containing research data. The downloaded files are saved 
to the local 'data/' directory for use in the Pistachio CLSC project.
Requirements:
    - gdown library must be installed
    - Internet connection required
    - Google Drive folder must be publicly accessible
Usage:
    Run this script directly to download the required data files:
    $ python load_data.py
Note:
    The download process will show progress information unless quiet=True.
    No authentication cookies are used for the download process.
"""

import gdown

# URL of the Google Drive folder containing the data files
url = "https://drive.google.com/drive/folders/18zZWQAwMMx2YtLj5mivQT3I6t91yd__C?usp=sharing"

# Local directory to save the downloaded files
output = "data/"

# Download all files from the specified Google Drive folder
# The 'quiet' parameter controls the verbosity of the download process
gdown.download_folder(url, output=output, quiet=False, use_cookies=False)