import streamlit as st
from video import preprocessing, model
import pandas as pd
import io

import os

st.title("AI hackaton")

labels = ["Amusement park", "Animals", "Bench", "Building", "Castle", "Cave", "Church", "City", "Cross", "Cultural institution", "Food", "Footpath", "Forest", "Furniture", "Grass", "Graveyard", "Lake", "Landscape", "Mine", "Monument", "Motor vehicle", "Mountains", "Museum", "Open-air museum", "Park", "Person", "Plants", "Reservoir", "River", "Road", "Rocks", "Snow", "Sport", "Sports facility", "Stairs", "Trees", "Watercraft", "Windows"]

st.subheader('Video analyzer')

st.text('Upload video to see when 38 categories can be spotted.')

st.info('For performance and cost reasons video analysis is limited to first 20 sec.')

uploaded_file = st.file_uploader("Choose a video...", type=["mp4"])

if uploaded_file is not None:

    output_path = f'{hash(uploaded_file.name)}.mp4'
    if not os.path.exists(output_path):
        preprocessing.upload_temporary(io.BytesIO(uploaded_file.read()), output_path)

    placeholder = st.empty()
    placeholder.text('Sampling video...')
    bar_placeholder = st.empty()
    bar_placeholder.progress(0)

    fps = preprocessing.get_fps(output_path)
    placeholder.text('Sampling video...')
    frame_path = f'frames_{hash(uploaded_file.name)}'
    if not os.path.exists(frame_path):
        os.makedirs(frame_path, exist_ok=True)
        preprocessing.get_frames(output_path, frame_path, fps, 10, bar_placeholder)
    placeholder.text('Magic happens...')

    bar_placeholder.progress(0)

    @st.cache(persist=True)
    def call_model(path):
        return [{'Grass': 0.3087106943130493, 'City': 0.6419469118118286, 'Church': 0.14725708961486816, 'Landscape': 0.12454783916473389, 'Cross': 0.33660638332366943, 'Trees': 0.793880045413971, 'Plants': 0.3586842715740204, 'Footpath': 0.39658093452453613, 'Windows': 0.27514970302581787, 'Building': 0.7506213188171387, 'Person': 0.3120952844619751, 'Road': 0.2412111759185791, 'Name': '5.0.jpg'}, {'Grass': 0.46526384353637695, 'City': 0.553439199924469, 'Church': 0.21690639853477478, 'Landscape': 0.17960456013679504, 'Cross': 0.4460863173007965, 'Trees': 0.7692573666572571, 'Plants': 0.34022432565689087, 'Footpath': 0.310443639755249, 'Windows': 0.22343796491622925, 'Building': 0.6942331194877625, 'Person': 0.23729604482650757, 'Road': 0.19961750507354736, 'Name': '7.0.jpg'}, {'Grass': 0.5168365836143494, 'Graveyard': 0.1046290397644043, 'City': 0.609474778175354, 'Motor vehicle': 0.12374413013458252, 'Church': 0.3039708733558655, 'Landscape': 0.16428416967391968, 'Cross': 0.5606313943862915, 'Trees': 0.8599545955657959, 'Plants': 0.4905676245689392, 'Footpath': 0.3798556625843048, 'Windows': 0.3211686313152313, 'Building': 0.752217710018158, 'Person': 0.29346150159835815, 'Road': 0.3093758523464203, 'Name': '3.0.jpg'}, {'Grass': 0.512409508228302, 'Graveyard': 0.16529539227485657, 'City': 0.5426971316337585, 'Motor vehicle': 0.10680320858955383, 'Forest': 0.11310398578643799, 'Church': 0.2763845920562744, 'Landscape': 0.10440891981124878, 'Cross': 0.5869269967079163, 'Trees': 0.8964648246765137, 'Plants': 0.4305913746356964, 'Footpath': 0.24550238251686096, 'Windows': 0.14259877800941467, 'Building': 0.5501377582550049, 'Person': 0.3329416513442993, 'Road': 0.18828538060188293, 'Name': '1.0.jpg'}, {'Grass': 0.3344569802284241, 'City': 0.483887255191803, 'Church': 0.25792694091796875, 'Landscape': 0.1560066044330597, 'Cross': 0.39626210927963257, 'Trees': 0.8145322799682617, 'Plants': 0.34431174397468567, 'Footpath': 0.38550543785095215, 'Windows': 0.24933505058288574, 'Building': 0.7200826406478882, 'Person': 0.18422165513038635, 'Road': 0.19155347347259521, 'Name': '6.0.jpg'}, {'Grass': 0.4293639063835144, 'City': 0.6051448583602905, 'Church': 0.18756455183029175, 'Landscape': 0.12081244587898254, 'Cross': 0.4549829661846161, 'Trees': 0.8127233982086182, 'Plants': 0.4005934000015259, 'Footpath': 0.4169887900352478, 'Windows': 0.27531611919403076, 'Building': 0.7383756637573242, 'Person': 0.317405641078949, 'Road': 0.25942862033843994, 'Name': '4.0.jpg'}, {'Grass': 0.46666011214256287, 'Graveyard': 0.17608657479286194, 'City': 0.6187540292739868, 'Forest': 0.11570045351982117, 'Church': 0.39231032133102417, 'Landscape': 0.10543844103813171, 'Cross': 0.598162829875946, 'Trees': 0.9003602266311646, 'Plants': 0.407392293214798, 'Footpath': 0.22856652736663818, 'Windows': 0.18655404448509216, 'Building': 0.6407525539398193, 'Person': 0.2657005488872528, 'Road': 0.15874066948890686, 'Name': '0.0.jpg'}, {'Grass': 0.4727894961833954, 'Graveyard': 0.19435006380081177, 'City': 0.5772087574005127, 'Forest': 0.10132375359535217, 'Church': 0.45846447348594666, 'Landscape': 0.10283401608467102, 'Cross': 0.6924537420272827, 'Trees': 0.9002237319946289, 'Plants': 0.43157199025154114, 'Footpath': 0.2361062467098236, 'Windows': 0.14053723216056824, 'Building': 0.584099531173706, 'Person': 0.2740408778190613, 'Road': 0.15962767601013184, 'Name': '2.0.jpg'}, {'City': 0.15065857768058777, 'Trees': 0.16577282547950745, 'Footpath': 0.2753429412841797, 'Windows': 0.11118188500404358, 'Building': 0.49681857228279114, 'Person': 0.2980937361717224, 'Road': 0.12601417303085327, 'Name': '8.0.jpg'}, {'City': 0.12279975414276123, 'Trees': 0.25372007489204407, 'Footpath': 0.34283116459846497, 'Windows': 0.13906338810920715, 'Building': 0.6261826157569885, 'Person': 0.22018423676490784, 'Road': 0.15209704637527466, 'Name': '9.0.jpg'}]
        # return model.predict_frames(path, bar_placeholder)

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