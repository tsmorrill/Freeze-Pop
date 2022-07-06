from datetime import datetime
from midiutil import MIDIFile


def make_cube(pitch, time, note_len, vel, t):
    """Freeze callables and return a cube."""
    frozen_pitch = pitch
    if callable(pitch):
        frozen_pitch = pitch()
    frozen_vel = vel
    if callable(vel):
        frozen_vel = vel()

    cube = None
    if frozen_vel and frozen_pitch is not None:           # no cube if vel == 0
        cube = [frozen_pitch, time, note_len, frozen_vel]
    return cube


def make_freezer(note_len=1/16, gate=1, nudge=0):
    note_len *= 4                     # midiutil measures time in quarter notes

    def freezer(pitch, vel, time, s, t):
        ice_tray = []
        cube_time = time + nudge         # push cube off-grid and maintain time
        cube_len = note_len * gate       # adjust cube length and maintain time
        cube = make_cube(pitch, cube_time, cube_len, vel, t)
        time += note_len
        if cube is not None:
            ice_tray.append(cube)
        return ice_tray, time

    return freezer


def freeze_song(song, filename=None, track_names=None, combine_tracks=False):
    if filename is None:
        dt = datetime.now()
        filename = dt.strftime("%Y-%m-%d_%H%M%S")

    output_file = MIDIFile()
    if combine_tracks:
        output_file.addTrackName(0, 0, filename)

    default_freezer = make_freezer(note_len=1/16)       # tracks can share this

    for track_number, track in enumerate(song):
        if combine_tracks:
            track_number = 0           # just dump all the ice buckets together

        track_name = f"Track {track_number}"
        if track_names:
            track_name = track_name[track_number]
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
                        freezer = None
                        note = [pitch, vel, freezer]

                    pitch, vel, freezer = note
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

    filename = f"{filename}.mid"
    with open(filename, 'wb') as outf:
        output_file.writeFile(outf)
        print(f"Wrote to file {filename}.")


def freeze_track(track, name=None):
    song = [track]
    freeze_song(song, filename=name, track_names=[name])


def freeze_section(section, name=None):
    track = [section]
    freeze_track(track, name)


def freeze_phrase(phrase, name=None):
    section = [phrase]
    freeze_section(section, name)


if __name__ == "__main__":
    names = [name for name in dir() if not name.startswith("_")]
    imports = ["MIDIFile", "datetime"]
    for name in imports:
        names.remove(name)
    print(", ".join(names))
