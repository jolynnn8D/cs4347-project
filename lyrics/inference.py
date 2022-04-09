import os
import shutil
from pydub import AudioSegment
from pydub.utils import make_chunks
from speechbrain.pretrained import EncoderDecoderASR

SNIPPET_FOLDER = "lyrics/audio_snippets"
SNIPPET_LEN = 5000

def split_audio(input_file):
    audio = AudioSegment.from_file(input_file)

    snippets = make_chunks(audio, SNIPPET_LEN)
    for index, snippet in enumerate(snippets):
        snippet.export(f"{SNIPPET_FOLDER}/input_snippet_{index}.mp3", format="mp3")


def transcribe_lyrics(input_file):
    if not os.path.exists(SNIPPET_FOLDER):
        os.mkdir(SNIPPET_FOLDER)
    
    split_audio(input_file)

    asr_model = EncoderDecoderASR.from_hparams(source="lyrics/pretrained_model", hparams_file="hyperparams.yaml",
                                            savedir="lyrics/tmp")
    lyrics = []
    for filename in os.listdir(SNIPPET_FOLDER):
        snippet_file = os.path.join(SNIPPET_FOLDER, filename)
        lyrics.append(asr_model.transcribe_file(snippet_file))

    # shutil.rmtree(SNIPPET_FOLDER)
    shutil.rmtree("lyrics/tmp")

    return " ".join(lyrics)