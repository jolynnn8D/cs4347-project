import mido
import math 
import json

def process(file_path, output_path):
    mid2 = mido.MidiFile(file_path)

    new_mid = mido.MidiFile()
    track = mido.MidiTrack()
    meta_track = mido.MidiTrack()
    new_mid.tracks.append(meta_track)
    new_mid.tracks.append(track)


    idx = 0
    meta = None
    for t in mid2.tracks:
        for msg in t:
            if msg.is_meta and idx == 0:
                meta = msg
            else: 
                track.append(msg)
            idx += 1

    meta_track.append(mido.Message('program_change', channel=0, program=0, time=0))
    meta_track.append(meta)
    meta_track.append(mido.MetaMessage('end_of_track', time=0))
    new_mid.save(output_path)

    create_settings(output_path)


def parse_notes(midi_path):
    mid2 = mido.MidiFile(midi_path)

    pitch_list = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    notes = {}

    def convert_note(note_number):
        pitch = note_number % 12
        octave = math.floor(note_number / 12)  
        octave = int(octave)
        
        return pitch_list[pitch] + str(octave)

    curr_time = 0
    for msg in mid2:
        if msg.type == 'note_on':
            notes[curr_time] = convert_note(msg.note)
        curr_time += msg.time

    return notes

def create_settings(midi_path):
    settings_default = """
{
    "midi_fname": "./melody/results/finals.mid",
    "audio_fname": "./input/input_file.mp3",
    "video_fname": "./output/animated_midi.mp4",
    "color_loop": [  
        (21, 114, 161),
        (154, 208, 236),
        (239, 218, 215),
        (227, 190, 198),
        (253, 206, 185),
        (216, 133, 163),
        (120, 151, 171),
        (101, 93, 138),
    ],
    "lyrics": {
"""
    notes = parse_notes(midi_path)
    with open('./melody/settings.py', 'w') as settings_file:
        settings_file.write(settings_default)
        for time, note in notes.items():
            settings_file.write(f"\t\t{time}: \'{note}\', \n")
        settings_file.write('\t}\n')
        settings_file.write('}')



