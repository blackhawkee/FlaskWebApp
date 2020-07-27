import base64

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import time, os, fnmatch, shutil

# Rename the downloaded JSON file to client_secrets.json
# The client_secrets.json file needs to be in the same directory as the script.
class uploadGDrive(object):
    def uploadBytesToGDrive(self, arg):
        gauth = GoogleAuth()
        drive = GoogleDrive(gauth)

        localTime = time.localtime()
        timestamp = time.strftime('%b-%d-%Y_%H%M', localTime)


        # List files in Google Drive
        fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in fileList:
            print('title: %s, id: %s' % (file1['title'], file1['id']))

        file1 = drive.CreateFile({
            'parents': [{'id': '16p-ZPzW5C_Neyh8Ylagp1u0gUsMcdh6y'}],
            'title': 'Image-' + timestamp + '.jpg'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
        # tempStr = str(arg)
        # tempStr = tempStr[2:-1]
        # print(str(arg))
        # file1.SetContentString(str(base64.b64decode(tempStr)))  # Set content of the file from given string.
        # file1.SetContentFile(arg)
        # file1.SetContentString(arg, 'utf-8')
        # file1.SetContentFile('C:/Users/prems/Desktop/temp/logo.png')
        print(arg)
        file1.SetContentFile('temp/test1.png')
        
        file1.Upload()
