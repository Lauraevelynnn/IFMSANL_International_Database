from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def upload(file_path, file_name, folder_id):
    custom_settings_path = 'tokens/pydrive_settings.yaml'
    gauth = GoogleAuth(settings_file=custom_settings_path)
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    file = drive.CreateFile({'title': file_name, 'parents': [{'id': folder_id}]})
    file.SetContentFile(file_path)
    file.Upload()
    return file['alternateLink']