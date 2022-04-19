import os
import sys
import json
import logging
from tqdm import tqdm

from speechbrain.utils.data_utils import get_all_files
from speechbrain.dataio.dataio import read_audio

logger = logging.getLogger(__name__)
SAMPLERATE = 16000


def prepare_data(data_folder, save_json_train, save_json_valid,
                 save_json_test):
    # Check if this phase is already done (if so, skip it)
    if skip(save_json_train, save_json_valid, save_json_test):
        logger.info("Preparation completed in previous run, skipping.")
        return

    train_data_folder = os.path.join(data_folder, "DSing_train1/audio")
    test_data_folder = os.path.join(data_folder, "DSing_dev")

    # prepare training data
    train_json_dict = create_json_dict(train_data_folder)
    save_json(train_json_dict, save_json_train)

    # prepare testing data
    test_json_dict = create_json_dict(test_data_folder)
    # 50% for valid, 50% for test
    total_len = len(test_json_dict)
    valid_dict_len = int(0.5 * total_len)
    save_json(dict(list(test_json_dict.items())[:valid_dict_len]),
              save_json_valid)
    save_json(dict(list(test_json_dict.items())[valid_dict_len:]),
              save_json_test)


def get_transcription_dict(transcription_path):
    transcription_dict = {}
    transcription_file = open(transcription_path, "r")
    for line in transcription_file:
        wav_id, wrds = line.rstrip().split(" ", 1)
        transcription_dict[wav_id] = wrds

    logger.info(f"Transcription file {transcription_path} read!")
    transcription_file.close()

    return transcription_dict


def create_json_dict(data_folder):
    extension = [".wav"]
    transcription_filename = "transcription.txt"

    # prepare training data
    transcription_path = os.path.join(data_folder, transcription_filename)
    if not os.path.isfile(transcription_path):
        sys.exit("Cannot find train transcription file: " + transcription_path)

    # List of the wav files
    wav_lst = get_all_files(
        data_folder,
        match_and=extension,
    )

    transcription_dict = get_transcription_dict(transcription_path)

    json_dict = {}

    for wav_file in tqdm(wav_lst, desc='WAV files processed'):
        path_parts = wav_file.split(os.path.sep)
        wav_id, _ = os.path.splitext(path_parts[-1])

        signal = read_audio(wav_file)
        duration = len(signal) / SAMPLERATE

        if wav_id not in transcription_dict:
            raise ValueError("Words not found for wav: " + wav_id)
        wrds = transcription_dict[wav_id]

        json_dict[wav_id] = {
            "wav": wav_file,
            "length": duration,
            "words": wrds,
        }

    return json_dict


def save_json(json_dict, json_file):
    # Writing the dictionary to the json file
    os.makedirs(os.path.dirname(json_file), exist_ok=True)

    with open(json_file, mode="w") as json_f:
        json.dump(json_dict, json_f, indent=2)

    logger.info(f"{json_file} successfully created!")


def skip(*filenames):
    for filename in filenames:
        if not os.path.isfile(filename):
            return False
    return True
