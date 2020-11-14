import cv2


def upload_temporary(file, path):
    with open(path, 'wb') as out:
        out.write(file.read())


def get_fps(video_path):
    video = cv2.VideoCapture(video_path)
    return video.get(cv2.CAP_PROP_FPS)


def get_frames(video_path, output_path, fps, length=None, bar=None):
    cap = cv2.VideoCapture(video_path)
    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if i % fps == 0:
            cv2.imwrite(f"{output_path}/{str(i // fps)}.jpg", frame)
        i += 1
        if length is not None:
            if bar is not None:
                bar.progress((i//fps) / length)
            if (i//fps) >= length:
                break

    cap.release()
    cv2.destroyAllWindows()
