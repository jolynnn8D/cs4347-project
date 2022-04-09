import streamlit as st
import os 

from pydub import AudioSegment
from melody.inference import make_predictions
from melody.process_midi import process
from lyrics.inference import transcribe_lyrics

st.title("CS4347 Music Transcription Application")

INPUT_FILE_PATH = "./input/input_file.mp3"
OUTPUT_PATH = "./melody/results"
MODEL_PATH = "./melody/model/model_1"

MIDI_PATH = "./melody/results/trans.mid"
FINAL_MIDI = "./melody/results/finals.mid"

def transcribe(file):
    lyrics = ""
    with st.spinner('Transcribing...'):
        st.write(file)
        sound = AudioSegment.from_mp3(file)      
        sound.export(INPUT_FILE_PATH,format="mp3")
        make_predictions(INPUT_FILE_PATH, OUTPUT_PATH, MODEL_PATH, 0.4, 0.5)
        lyrics = transcribe_lyrics(INPUT_FILE_PATH)
    st.write("Done transcribing!")
    with st.spinner("Animating... (this will take up to several minutes)"):
        process(MIDI_PATH, FINAL_MIDI)
        os.system('midani -s ./melody/settings.py')
        os.system('ffmpeg -y -i ./output/animated_midi.mp4 -vcodec libx264 ./output/html_midi.mp4')
        os.remove('./output/animated_midi.mp4')
    st.subheader("Your video!")
    st.subheader("You can download the video by clicking on the three dots in the bottom right of the video.")
    user_video_file = open('./output/html_midi.mp4', 'rb')
    user_video_bytes = user_video_file.read()
    st.video(user_video_bytes)
    st.subheader("Transcribed lyrics")
    st.write(lyrics)

st.subheader("Sample Video")
video_file = open('./output/sample_video.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)
music_file = st.file_uploader("Import your music here!", type="mp3", accept_multiple_files=False)
if st.button("Transcribe!") and music_file is not None:
    transcribe(music_file)
