
from google.cloud import speech_v1p1beta1
import io
import spacy


def predict(path):
    client = speech_v1p1beta1.SpeechClient()

    with io.open(path, "rb") as audio_file:
        content = audio_file.read()
        audio = speech_v1p1beta1.RecognitionAudio(content=content)

    config = speech_v1p1beta1.RecognitionConfig(
        encoding=speech_v1p1beta1.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code="pl-PL",
    )

    operation = client.long_running_recognize(
        request={"config": config, "audio": audio}
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=60)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    text = ' '.join([result.alternatives[0].transcript for result in response.results])
    return text


def aggregate(text):

    nlp = spacy.load("pl_core_news_sm")
    doc = nlp(text.lower())

    labels = ["Amusement park", "Animals", "Bench", "Building", "Castle", "Cave", "Church", "City", "Cross",
              "Cultural institution", "Food", "Footpath", "Forest", "Furniture", "Grass", "Graveyard", "Lake",
              "Landscape", "Mine", "Monument", "Motor vehicle", "Mountains", "Museum", "Open-air museum", "Park",
              "Person", "Plants", "Reservoir", "River", "Road", "Rocks", "Snow", "Sport", "Sports facility", "Stairs",
              "Trees", "Watercraft", "Windows"]

    pl_labels = ["park rozrywki", "zwierzę", "ławka", "budynek", "zamek", "jaskinia", "kościół", "miasto", "krzyż",
              "instytucja kulturowa", "jedzenie", "ścieżka", "las", "mebel", "trawa", "cmentarz", "jezioro",
              "krajobraz", "kopalnia", "zabytek", "pojazd", "góry", "muzeum", "muzeum plenerowe", "park",
              "osoba", "roślina", "rezerwuar", "rzeka", "droga", "kamień", "śnieg", "sport", "hala sportowa", "schody",
              "drzewo", "łódź", "okno"]

    d = []

    for i, e in enumerate(pl_labels):
        c = 0
        for token in doc:
            if e in token.text:
                c += 1
        if c > 0:
            d.append((c, labels[i], e))

    d = sorted(d)

    out = d

    if len(out) > 3:
        out = out[:3]

    return out
