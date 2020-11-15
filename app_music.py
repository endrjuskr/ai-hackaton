import streamlit as st
from video import preprocessing, model
from audio import preprocessing as ps, model as md
import pandas as pd
from annotated_text import annotated_text
import io

import os


def music_app(uploaded_file, language_index):
    name = uploaded_file.name.replace(" ", "")
    output_path = 'uploads/' + name
    if not os.path.exists(output_path):
        preprocessing.upload_temporary(io.BytesIO(uploaded_file.read()), output_path)

    placeholder = st.empty()
    placeholder.text('Audio sampling...')
    if not os.path.exists('uploads/new_' + name):
        ps.cut(output_path, 'uploads/new_' + name)
    output_path = 'uploads/new_' + name
    placeholder.text('Magic happens...')

    @st.cache(persist=True, show_spinner=False, suppress_st_warning=True)
    def call_model(path, language_index):
        return md.predict(path, language_index)

    pr = call_model(output_path, language_index)

    placeholder.text('Postprocessing...')

    @st.cache(persist=True, show_spinner=False, suppress_st_warning=True)
    def call_agg(pr, language_index):
        return md.aggregate(pr, language_index)


    out = call_agg(pr, language_index)

    placeholder.empty()
    st.success('Audio analysis is done')

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
                if w.lower() in pr2[j].lower():
                    t.append((pr2[j], w2, "#8ef"))
                else:
                    t.append(" " + pr2[j] + " ")
            annotated_text(*t)
    else:
        pr2 = pr.split(' ')

        for i in range(0, len(pr2), 10):
            st.text(' '.join(pr2[i: i + 10]))

