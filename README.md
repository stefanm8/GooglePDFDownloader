# Google Drive PDF downloader

Given a file id and a path it will download the corresponding file to the specified location

## Prerequisites

Python 3.2 or above & pip

## Installing

### Option 1
1. obtain credentials file from google api console by following the step 1 from this link
https://developers.google.com/drive/v3/web/quickstart/python

2. Copy the the downloaded file to the project folder and rename it to client_secret.json

3. run pip install -r requirements.txt

4. run the script without arguments, you will get a url to put in your browser and authenticate with the corresponding user


## Usage

```console
usage: gdownload [-h] [--client-secret CLIENT_SECRET]
                 [--creds-storage CREDS_STORAGE]
                 file_id file_path

Downloads a file by a given file ID and saves the file in PDF format

positional arguments:
  file_id               File id retrieved from google
  file_path             EX: /home/user/mydir/myfile

optional arguments:
  -h, --help            show this help message and exit
  --client-secret CLIENT_SECRET
                        Credentials file from google api console
  --creds-storage CREDS_STORAGE
                        Where to store credentials or to find existing
```
