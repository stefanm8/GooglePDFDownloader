from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaIoBaseDownload
from oauth2client.file import Storage as CredentialStorage
import argparse
import os


def build_parser():
    desc = """
    Downloads a file by a given file ID and saves the file in PDF format
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("file_id", type=str, help="File id retrieved from google")
    parser.add_argument("file_path", type=str, help="EX: /home/user/mydir/myfile")

    return parser


def get_service():
    SCOPES = "https://www.googleapis.com/auth/drive"

    credential_storage = CredentialStorage("creds.json")
    creds = credential_storage.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets("client_secret.json", SCOPES)
        creds = tools.run_flow(flow, credential_storage)

    return build("drive", "v3", http=creds.authorize(Http()))


def download_file_pdf(file_id, service):
    request = service.files().export_media(
        fileId=file_id, mimeType="application/pdf"
    ).execute()
    return request


def save_file(file_location, io_file):
    with open(file_location, "wb") as out:
        out.write(io_file)


def parse_path(path):
    if path.endswith("/"):
        raise Exception("Invalid file name")

    if not path.endswith(".pdf"):
        path = path + ".pdf"

    if "/" in path:
        os.makedirs(os.path.dirname(path), exist_ok=True)

    return path


def main(file_id, file_path, service):
    io_file = download_file_pdf(file_id, service)
    save_file(file_path, io_file)


if __name__ == "__main__":
    service = get_service()
    parser = build_parser()
    args = parser.parse_args()
    main(args.file_id, parse_path(args.file_path), service)
