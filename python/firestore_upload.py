import os
from firebase_admin import credentials, initialize_app, storage

def upload_mp3_to_firebase(file_path, storage_path="audio"):
    cred = credentials.Certificate('... .json')
    initialize_app(cred, {'storageBucket': '... appspot.com'})

    bucket = storage.bucket()

    file_name = os.path.basename(file_path)
    destination_path = f"{storage_path}/{file_name}"

    blob = bucket.blob(destination_path)
    blob.upload_from_filename(file_path)

    print(f"File {file_name} uploaded to Firebase Storage at {destination_path}")
