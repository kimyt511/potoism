from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import qrcode

from PIL import ImageTk, Image
import pyautogui
import cv2 as cv
import os

phone_number = input()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/potoism-669e35abe0e6.json"
#json 파일 경로

from google.cloud import storage

bucket_name = 'kimyt0511'    # 서비스 계정 생성한 bucket 이름 입력
source_blob_name = phone_number + '.jpg'    # GCP에 저장되어 있는 파일 명
# 전화번호 + (image1, image2, image3, image4) + jpg
destination_file_name = './download/'+phone_number+'.jpg'    # 다운받을 파일을 저장할 경로("local/path/to/file")

f = open(destination_file_name, 'w')
f.close()
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(source_blob_name)
blob.download_to_filename(destination_file_name)


def makeQR():
    
    # 키 파일 (JSON) 경로
    SERVICE_ACCOUNT_FILE = 'sinchon-90059d067194.json'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)
    # 파일 업로드
    file_metadata = {'name': 'sample_name'}
    media = MediaFileUpload(destination_file_name,
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
    qrl = "https://drive.google.com/file/d/"+file_id+"/view"
    qr_gen = qrcode.make(qrl)
    qr_gen.save("qrcode1.png")
    #print(qrl)
    # qr_gen.show() # qr코드 보여주기
    original_image_path = destination_file_name
    qr_image_path = "./download/qrcode1.png"
    original_image = Image.open(original_image_path)
    qr_image = Image.open(qr_image_path)
    qr_image = qr_image.resize((50, 50))
    position = (original_image.width - qr_image.width, original_image.height - qr_image.height)
    original_image.paste(qr_image, position)
    original_image.save("./download/result.png")
    # original_image.show()

    
