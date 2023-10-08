from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

image_url =  'image1.jpg'
# 키 파일 (JSON) 경로
SERVICE_ACCOUNT_FILE = 'sinchon-90059d067194.json'

SCOPES = ['https://www.googleapis.com/auth/drive']
creds = None
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

# 파일 업로드
file_metadata = {'name': 'sample_name'}
media = MediaFileUpload(image_url,
                        mimetype='application/octet-stream',
                        resumable=True)
created = drive_service.files().create(body=file_metadata,
                                       media_body=media,
                                       fields='id').execute()
print('File ID: {}'.format(created.get('id')))


creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

file_id = '{}'.format(created.get('id'))

# 파일을 공개로 설정
def set_public(service, file_id):
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    request = service.permissions().create(
        fileId=file_id,
        body=permission,
        fields='id'
    )
    request.execute()

set_public(drive_service, file_id)
import qrcode

qrl = "https://drive.google.com/file/d/"+file_id+"/view"
qr_gen = qrcode.make(qrl)
qr_gen.save("qrcode1.png")
print(qrl)

from PIL import Image

original_image_path = "test.png"
qr_image_path = "qrcode1.png"

original_image = Image.open(image_url)
qr_image = Image.open(qr_image_path)

qr_image = qr_image.resize((50, 50))

position = (original_image.width - qr_image.width, original_image.height - qr_image.height)

original_image.paste(qr_image, position)

original_image.save("merged_image.png")

original_image.show()

