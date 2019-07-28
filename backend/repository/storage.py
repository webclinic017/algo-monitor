from firebase_admin import storage
from helpers.helpers import mkdir_conditional

_bucket = storage.bucket()

def upload(blob_name: str, path: str):
    blob = _bucket.blob(blob_name)
    blob.upload_from_filename(path)

def download(blob_name: str, path: str):
    blob = _bucket.blob(blob_name)
    mkdir_conditional('public')
    blob.download_to_filename(path)

def delete(blob_name: str):
    blob = _bucket.blob(blob_name)
    blob.delete()