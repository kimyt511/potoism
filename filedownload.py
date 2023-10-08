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



