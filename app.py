import streamlit as st
from video import preprocessing
import io
import os

st.title("AI hackaton")

uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])

if uploaded_file is not None:
    print("yeah!")

    # video_bytes = uploaded_file.read()
    # uploaded_file.
    # st.video(video_bytes)

    my_bar = st.progress(0)

    output_path = "check.mp4"

    preprocessing.upload_temporary(io.BytesIO(uploaded_file.read()), output_path)

    video_file = open(output_path, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

    fps = preprocessing.get_fps(output_path)
    st.text(f"FPS {fps}")

    my_bar.progress(50)

    os.makedirs('frames', exist_ok=True)

    preprocessing.get_frames(output_path, 'frames', fps)

    my_bar.progress(100)

    st.text(f"Files {len(os.listdir('frames'))}")