import streamlit as st
from video import preprocessing, model
from audio import preprocessing as ps, model as md
import pandas as pd
from annotated_text import annotated_text
import io

import os


def music_app(uploaded_file):

    output_path = f'{hash(uploaded_file.name)}.mp3'
    if not os.path.exists(output_path):
        preprocessing.upload_temporary(io.BytesIO(uploaded_file.read()), output_path)

    placeholder = st.empty()
    placeholder.text('Magic happens...')

    @st.cache(persist=True, suppress_st_warning=True)
    def call_model(path):
        return md.predict(path)

    pr = call_model(f'{output_path}')

    placeholder.empty()
    st.success('Audio analysis is done')

    @st.cache(persist=True, suppress_st_warning=True)
    def call_agg(pr):
        return md.aggregate(pr)


    out = call_agg(pr)

    df = pd.DataFrame(
        [[o[1], o[0]] for o in out],
        columns=['category', 'count']
    )

    st.table(df)

    row_index = st.selectbox("Select category", df.index)
    if st.button('Show'):
        w = out[row_index][2]
        w2 = out[row_index][1]
        pr2 = pr.split(' ')

        for i in range(0, len(pr2), 30):
            t = []
            for j in range(i, i + 30):
                if j >= len(pr2):
                    break
                if w in pr2[j].lower():
                    t.append((pr2[j], w2, "#8ef"))
                else:
                    t.append(f" {pr2[j]} ")
            annotated_text(*t)
    else:
        pr2 = pr.split(' ')

        for i in range(0, len(pr2), 10):
            st.text(' '.join(pr2[i: i + 10]))

