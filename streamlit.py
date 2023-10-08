import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.frame = None

    def recv(self, frame):
        self.frame = frame
        return self.frame

def main():
    st.title("WebRTC Camera and Picture Capture")

    webrtc_ctx = webrtc_streamer(
        key="sample",
        video_processor_factory=VideoProcessor
    )

    if st.button("Capture Picture"):
        if webrtc_ctx.state.playing and webrtc_ctx.video_transformer.frame is not None:
            captured_image = webrtc_ctx.video_transformer.frame.to_ndarray()
            st.image(captured_image, channels="RGB", caption="Captured Picture")

if __name__ == "__main__":
    main()