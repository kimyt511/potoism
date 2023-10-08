import streamlit as st
import cv2 as cv
import numpy as np
from streamlit_webrtc import webrtc_streamer

st.title("Picture Capture with OpenCV and Streamlit")
cap = cv.VideoCapture(0) # 기본카메라
if not cap.isOpened():
    print("camera open failed")
    exit()

# 카운트 다운을 시작할 시간 설정
start_time = cv.getTickCount()
countdown = 2  # 5초로 설정
    
# 캡쳐 횟수
capturecnt=0
while capturecnt < 8:
    ret, img = cap.read()
    if not ret:
        print("error")
        break
    
    
    # 현재 시간 가져오기
    current_time = cv.getTickCount()
    
    # 경과 시간 계산 (밀리초 단위)
    elapsed_time_ms = (current_time - start_time) / cv.getTickFrequency() * 1000
    
    # 카운트 다운 표시
    remaining_time = countdown - int(elapsed_time_ms / 1000)
    if elapsed_time_ms < countdown * 1000:
        cv.putText(img, f"Countdown: {remaining_time}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 5초 간격으로 캡처 및 카운트 다운 화면에 표시
    if elapsed_time_ms >= countdown * 1000:
        cv.imwrite('capture_%03d.png' % capturecnt,img)
        capturecnt+=1
        print("캡처 완료!")
        start_time = current_time  # 시작 시간 재설정
        
    if cv.waitKey(1) == ord('q'):
        break
    cv.imshow('PC_camera',img)
    
cap.release()
cv.destroyAllWindows()