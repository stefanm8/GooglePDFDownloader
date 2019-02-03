import argparse
import os
from oauth2client import file, client, tools
from oauth2client.file import Storage as CredentialStorage
from oauth2client.clientsecrets import InvalidClientSecretsError
from apiclient.discovery import build
from apiclient.http import MediaIoBaseDownload
from httplib2 import Http


GDOWNLOAD_CLIENT_SECRET = "client_secret.json"
GDOWNLOAD_CLIENT_STORAGE = "creds.json"

def build_parser():
    desc = """
    Downloads a file by a given file ID and saves the file in PDF format
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("file_id", type=str, help="File id retrieved from google")
    parser.add_argument("file_path", type=str, help="EX: /home/user/mydir/myfile")
    parser.add_argument(
        "--client-secret", 
        type=str, 
        default=GDOWNLOAD_CLIENT_SECRET,
        help="Credentials file from google api console",
    )
    parser.add_argument(
        "--creds-storage", 
        type=str, 
        default=GDOWNLOAD_CLIENT_STORAGE,
        help="Where to store credentials or to find existing",
    )

    return parser


def get_file_from_input():
    exists = ["exit", "quit", "q", "quit()"]
    fname = input("Enter the path where client_secret is located\n>")
    if os.path.isfile(fname):
        return fname

    if fname in exists:
        raise SystemExit

    get_file_from_input()

def get_service(creds_file=GDOWNLOAD_CLIENT_SECRET, creds_storage=GDOWNLOAD_CLIENT_STORAGE):
    SCOPES = "https://www.googleapis.com/auth/drive"

    credential_storage = CredentialStorage(creds_storage)
    creds = credential_storage.get()
    if not creds or creds.invalid:
        
        try:
            flow = client.flow_from_clientsecrets(creds_file, SCOPES)
            creds = tools.run_flow(flow, credential_storage)
        except InvalidClientSecretsError:
            print(
                "Client secret file was not found\n" +  
                "Enter the path where the client secret is," +  
                "optionally you may enter exit/quit to exit this prompt")
            creds_file = get_file_from_input()
            flow = client.flow_from_clientsecrets(creds_file, SCOPES)
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


def main(file_id, file_path, service, **kwargs):
    print("Downloading file {}".format(file_id))
    io_file = download_file_pdf(file_id, service)
    save_file(file_path, io_file)
    print("File saved to {}".format(file_path))


def init():
    parser = build_parser()
    try:
        args = parser.parse_args()
    except SystemExit: 
        get_service()
        raise SystemExit

    service = get_service(creds_storage=args.creds_storage, creds_file=args.client_secret)
    main(args.file_id, parse_path(args.file_path), service)
