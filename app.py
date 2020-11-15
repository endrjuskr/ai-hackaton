import streamlit as st
from video import preprocessing, model
import pandas as pd

from app_music import music_app
import io

import os

st.title("AI hackathon by Hobbmate")

st.subheader('Video & Audio analyzer')

st.info('For performance and cost reasons analysis is limited to first 30 sec. Audio analyzer accepts only Polish sound.')

uploaded_file = st.file_uploader("Choose a file...", type=["mp4", 'mp3'])

if uploaded_file is not None:

    if uploaded_file.name.lower().strip().endswith("mp4"):
        name = uploaded_file.name.replace(" ", "").replace(".", "_")
        output_path = f'uploads/{name}.mp4'
        if not os.path.exists(output_path):
            preprocessing.upload_temporary(io.BytesIO(uploaded_file.read()), output_path)

        placeholder = st.empty()
        placeholder.text('Sampling video...')
        bar_placeholder = st.empty()
        bar_placeholder.progress(0)

        fps = preprocessing.get_fps(output_path)
        placeholder.text('Sampling video...')
        frame_path = f'frames/frames_{name}'
        if not os.path.exists(frame_path):
            os.makedirs(frame_path, exist_ok=True)
            preprocessing.get_frames(output_path, frame_path, fps, 30, bar_placeholder)
        placeholder.text('Magic happens...')

        bar_placeholder.progress(0)

        def call_model(path):
            return model.predict_frames(path, bar_placeholder)

        pr = call_model(frame_path)

        st.success('Video analysis is done')
        bar_placeholder.empty()
        placeholder.empty()

        out = model.process_predictions(pr)

        df = pd.DataFrame(
            [[k, t[0], t[1]] for k in out.keys() for t in out[k]],
            columns=['category', 'from', 'to']
        )

        st.table(df)

        video_file = open(output_path, 'rb')
        video_bytes = video_file.read()

        row_index = st.selectbox("Select section", df.index)
        if st.button('Show'):
            video_placeholder = st.empty()
            video_placeholder.video(video_bytes, start_time=df['from'][row_index])
    else:
        music_app(uploaded_file)