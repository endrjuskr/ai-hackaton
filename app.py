import streamlit as st

st.title("AI hackaton")

uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])

if uploaded_file is not None:
    print("yeah!")

    video_bytes = uploaded_file.read()
    st.video(video_bytes)