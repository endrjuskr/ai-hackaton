from google.cloud import automl
import os
import streamlit as st

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'key.json'

project_id = 'ai-hackathon-295600'
model_id = 'ICN4781707899476901888'

prediction_client = automl.PredictionServiceClient()
model_full_id = automl.AutoMlClient.model_path(project_id, "us-central1", model_id)


@st.cache(persist=True, suppress_st_warning=True)
def predict(filepath):
    threshold = "0.1"
    with open(filepath, "rb") as content_file:
        content = content_file.read()

    image = automl.Image(image_bytes=content)
    payload = automl.ExamplePayload(image=image)
    params = {"score_threshold": threshold}

    request = automl.PredictRequest(
        name=model_full_id,
        payload=payload,
        params=params
    )

    response = prediction_client.predict(request=request)

    return {**{result.display_name.capitalize(): result.classification.score for result in response.payload},
             **{'Name': os.path.basename(filepath)}}


def predict_frames(path, bar):
    predictions = []

    test_files = os.listdir(path)
    i = 0
    for filename in test_files:
        filepath = os.path.join(path, filename)
        r = predict(filepath)
        predictions.append(r)
        i += 1
        bar.progress(i * 100 // len(test_files))

    return predictions


def process_predictions(predictions):
    t = set()
    for p in predictions:
        for k in p.keys():
            if k != "Name":
                t.add(k)

    w = {}
    for tt in t:
        ww = []
        for p in predictions:
            if tt in p and p[tt] > 0.5:
                ti = int(p["Name"].split('.')[0])
                ww.append(ti)
        if len(ww) > 0:
            w[tt] = sorted(ww)

    out = {}
    for k in w.keys():
        o = []
        st = w[k][0]
        for i in range(1, len(w[k])):
            if w[k][i] <= w[k][i - 1] + 2:
                continue
            else:
                o.append((st, w[k][i - 1] + 1))
                st = w[k][i]
        o.append((st, w[k][-1] + 1))

        out[k] = o

    return out
