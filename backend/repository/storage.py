from firebase_admin import storage

_bucket = storage.bucket()

def upload(blob_name: str, path: str):
    blob = _bucket.blob(blob_name)
    blob.upload_from_filename(path)

def download(blob_name: str, path: str):
    blob = _bucket.blob(blob_name)
    blob.download_to_filename(path)