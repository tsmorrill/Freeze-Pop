from datetime import datetime
from midiutil import MIDIFile
from typing import Callable, Optional


def chill(
    pitch: int, time: int, note_len: int, vel: int
) -> Optional[tuple]:
    """Freeze callables and return an icecube."""
    frozen_pitch = pitch
    if callable(pitch):
        frozen_pitch = pitch()
    frozen_vel = vel
    if callable(vel):
        frozen_vel = vel()

    ignored = frozen_vel == 0 or frozen_pitch is None
    icecube = None if ignored else (frozen_pitch, time, note_len, frozen_vel)
    return icecube


def make_freezer(
    note_len: float = 1 / 16, gate: float = 1, nudge: float = 0
) -> Callable:
    note_len *= 4  # midiutil measures time in quarter notes

    def freezer(pitch, vel, time, s, t):
        cube_time = time + nudge  # push cube off-grid and maintain time
        cube_len = note_len * gate  # adjust cube length and maintain time
        icecube = chill(pitch, cube_time, cube_len, vel)
        ice_tray = []
        if icecube is not None:
            ice_tray.append(icecube)
        return ice_tray, time + note_len

    return freezer


def freeze_song(
    song: list,
    filename: Optional[str] = None,
    track_names: Optional[list] = None,
):
    if filename is None:
        dt = datetime.now()
        filename = dt.strftime("%Y-%m-%d_%H%M%S")

    output_file = MIDIFile()

    default_freezer = make_freezer(note_len=1 / 16)  # tracks can share this

    for track_number, track in enumerate(song):
        track_name = f"Track {track_number}"
        if track_names:
            track_name = track_names[track_number]
        track_channel = 0

        time = 0
        output_file.addTrackName(track_number, time, track_name)
        ice_bucket = []

        for section in track:
            s = 0  # phrase counter

            for phrase in section:
                if callable(phrase):
                    phrase = phrase(s)
                t = 0  # note counter

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
        output_file.addNote(track_number, track_channel, pitch, time, note_len, vel)

    filename = f"{filename}.mid"
    with open(filename, "wb") as outf:
        output_file.writeFile(outf)
        print(f"Wrote to file {filename}.")


def freeze_track(track: list, name: Optional[str] = None):
    song = [track]
    freeze_song(song, filename=name, track_names=[name])


def freeze_section(section: list, name: Optional[str] = None):
    track = [section]
    freeze_track(track, name)


def freeze_phrase(phrase: list, name: Optional[str] = None):
    section = [phrase]
    freeze_section(section, name)


if __name__ == "__main__":
    names = [name for name in dir() if not name.startswith("_")]
    imports = ["Callable", "datetime", "MIDIFile", "Optional"]
    for name in imports:
        names.remove(name)
    print(", ".join(names))

    print(chill(pitch=None, time=0, note_len=1/4, vel=62))
