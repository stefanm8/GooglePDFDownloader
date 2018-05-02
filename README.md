# Google Drive PDF downloader

Given a file id and a path it will download the corresponding file to the specified location

## Prerequisites

Python 3.2 or above & pip

### Installing

run pip install -r requirements.txt

#### Usage

usage: core.py [-h] file_id file_path

Downloads a file by a given file ID and saves the file in PDF format

positional arguments:
  file_id     File id retrieved from google
  file_path   EX: /home/user/mydir/myfile

optional arguments:
  -h, --help  show this help message and exit


[run] -> python core.py insert_file_id insert_file_path
