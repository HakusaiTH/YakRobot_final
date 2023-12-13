import os
from firebase_admin import credentials, initialize_app, storage

def upload_mp3_to_firebase(file_path, storage_path="audio"):
    cred = credentials.Certificate('D:\\sanbot_final\\pythonbackend\\my-robot-9fdff-firebase-adminsdk-37upn-709ad75796.json')
    initialize_app(cred, {'storageBucket': 'my-robot-9fdff.appspot.com'})

    bucket = storage.bucket()

    file_name = os.path.basename(file_path)
    destination_path = f"{storage_path}/{file_name}"

    blob = bucket.blob(destination_path)
    blob.upload_from_filename(file_path)

    print(f"File {file_name} uploaded to Firebase Storage at {destination_path}")

# Example usage
'''
mp3_file_path = "output.mp3"
upload_mp3_to_firebase(mp3_file_path)

'''
