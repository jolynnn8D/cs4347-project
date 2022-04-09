import os
import shutil
from pydub import AudioSegment
from pydub.utils import make_chunks
from speechbrain.pretrained import EncoderDecoderASR

TMP_FOLDER = "lyrics/tmp"
SNIPPET_LEN = 30000

def split_audio(input_file):
    audio = AudioSegment.from_file(input_file)

    snippets = make_chunks(audio, SNIPPET_LEN)
    for index, snippet in enumerate(snippets):
        snippet.export(f"{TMP_FOLDER}/input_snippet_{index}.mp3", format="mp3")


def transcribe_lyrics(input_file):
    if not os.path.exists(TMP_FOLDER):
        os.mkdir(TMP_FOLDER)
    
    split_audio(input_file)

    asr_model = EncoderDecoderASR.from_hparams(source="lyrics/pretrained_model",
                                            savedir="tmp")
    lyrics = []
    for filename in os.listdir(TMP_FOLDER):
        snippet_file = os.path.join(TMP_FOLDER, filename)
        lyrics.append(asr_model.transcribe_file(snippet_file))

    shutil.rmtree(TMP_FOLDER)

    return " ".join(lyrics)

# print(transcribe_lyrics("input/input_file.mp3"))