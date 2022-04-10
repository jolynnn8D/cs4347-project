# Music Transcription Web App

## Running the app on local
Note that you need to have R installed on your local machine.  
On Mac OS, use: `brew install r`. On Windows, install an official distribution on R.  

### Running Streamlit
`pipenv shell`  
`streamlit run app.py`

### Transcription
To transcribe any piece of music, run the Streamlit app on localhost and upload a `mp3` file. The final animation file can be found in `output/html_midi.mp4` while the final midi can be found at `melody/results/finals.mid`.

### To install dependencies
`pipenv install <package>`
