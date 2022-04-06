import mido

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


