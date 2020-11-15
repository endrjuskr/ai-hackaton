from pydub import AudioSegment
AudioSegment.converter = '/usr/bin/ffmpeg'
# import sys
# sys.path.append('/Users/andrzej/Downloads/ffmpeg')
# import ffprobe


def cut(path, new_path):
    startMin = 0
    startSec = 0

    endMin = 0
    endSec = 30

    # Time to miliseconds
    startTime = startMin * 60 * 1000 + startSec * 1000
    endTime = endMin * 60 * 1000 + endSec * 1000

    # Opening file and extracting segment
    song = AudioSegment.from_mp3(path)
    extract = song[startTime:endTime]

    # Saving
    extract.export(new_path, format="mp3")