from datetime import datetime
from midiutil import MIDIFile


def make_cube(pitch, time, note_len=1/4, vel=80, t=0):
    """Freeze callables and return a cube."""
    if callable(pitch):
        pitch = pitch(t)
    if callable(vel):
        vel = vel(t)
    cube = None
    if vel and pitch is not None:                # ignore notes with velocity 0
        cube = [pitch, time, note_len, vel]
    return cube


def default_freezer(pitch, vel, time, s, t):
    note_len = 1/4
    ice_tray = []
    cube = make_cube(pitch, time, note_len, vel)
    time += note_len
    if cube is not None:
        ice_tray.append(cube)
    return ice_tray, time


def freeze(song, filename=None, combine_tracks=False):
    output_file = MIDIFile()
    if combine_tracks:
        output_file.addTrackName(0, 0, "Combined Track")

    for track_number, track in enumerate(song):
        if combine_tracks:
            track_number = 0

        track_name = f"Track {track_number}"
        track_channel = 0

        time = 0
        if not combine_tracks:
            output_file.addTrackName(track_number, time, track_name)
        ice_bucket = []

        for section in track:
            s = 0                                              # phrase counter

            for phrase in section:
                if callable(phrase):
                    phrase = phrase(s)
                t = 0                                            # note counter

                for note in phrase:
                    if note is None:
                        note = [None, 0, None]
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
