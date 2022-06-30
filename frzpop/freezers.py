from datetime import datetime
from midiutil import MIDIFile
from random import random


def default_freezer(pitch, vel, time, s, t):
    if callable(pitch):
        pitch = pitch(t)
    if callable(vel):
        vel = vel(t)
    note_len = 1/4            # one sixteenth note as measured in quarter notes
    ice_tray = []
    if vel and pitch is not None:                # ignore notes with velocity 0
        cube = [pitch, time, note_len, vel]
        ice_tray.append(cube)
    time += note_len
    return ice_tray, time


def freeze(song, filename=None):
    output_file = MIDIFile()

    for track_number, track in enumerate(song):
        track_name = f"Track {track_number}"
        track_channel = 0

        time = 0
        output_file.addTrackName(track_number, time, track_name)

        ice_bucket = []

        for section in track:
            s = 0                                              # phrase counter

            for phrase in section:
                if callable(phrase):
                    phrase = phrase(s)
                t = 0                                            # note counter

                for note in phrase:
                    if type(note) is int:
                        pitch = note
                        vel = 80
                        freezer = default_freezer
                        note = [pitch, vel, freezer]
                    if freezer is None:
                        freezer = default_freezer
                    ice_tray, time = freezer(pitch, vel, time, s, t)
                    ice_bucket.extend(ice_tray)
                t += 1
            s += 1

    for cube in ice_bucket:
        pitch, time, note_len, vel = cube
        output_file.addNote(track_number, track_channel,
                            pitch, time, note_len, vel)

    if filename is None:
        dt = datetime.now()
        filename = dt.strftime("%Y-%m-%d_%H%M%S")
    filename = f"{filename}.mid"
    with open(filename, 'wb') as outf:
        output_file.writeFile(outf)
        print(f"Wrote to file {filename}.")


if __name__ == "__main__":
    phrase = [[60,   92, None],
              [62,   92, None],
              [64,   92, None],
              [65,    0, None],
              [67,   88, None],
              [69,  127, None],
              [72,   92, None],
              [None, 72, None]]
    section = [phrase, phrase]
    track = [section]
    test_song = [track]
    freeze(test_song)
