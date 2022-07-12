from datetime import datetime
from midiutil import MIDIFile
from typing import Callable, Optional


def chill(pitch, time: float, note_len: float, vel) -> Optional[tuple]:
    """Freeze callables and return an icecube."""
    frozen_pitch = pitch
    if callable(pitch):
        frozen_pitch = pitch()
    assert (
        frozen_pitch in range(128) or frozen_pitch is None
    ), f"frozen_pitch must be an integer 0-127 or None. Recieved {frozen_pitch}."

    assert type(time) == float, f"time must be a float. Recieved {time}."
    assert type(note_len) == float, f"note_len must be a float. Recieved {note_len}."

    frozen_vel = vel
    if callable(vel):
        frozen_vel = vel()
    assert frozen_vel in range(
        128
    ), f"frozen_vel must be an integer 0-127. Received {frozen_vel}."

    is_rest = frozen_vel == 0 or frozen_pitch is None
    icecube = None if is_rest else (frozen_pitch, time, note_len, frozen_vel)
    return icecube


def freezer(note_len: float = 1 / 16, gate: float = 1, nudge: float = 0) -> Callable:
    """Create a freezer function."""
    note_len *= 4  # midiutil measures time in quarter notes

    def freezer_func(pitch, vel, time, s, t):
        cube_start = float(time + nudge)
        cube_dur = float(note_len * gate)
        icecube = chill(pitch, cube_start, cube_dur, vel)
        ice_tray = []
        if icecube is not None:
            ice_tray.append(icecube)
        return ice_tray, time + note_len

    return freezer_func


def freeze_song(
    song: list,
    filename: Optional[str] = None,
    track_names: Optional[list] = None,
):
    if filename is None:
        dt = datetime.now()
        filename = dt.strftime("%Y-%m-%d_%H%M%S")

    output_file = MIDIFile()

    for track_int, track in enumerate(song):
        if track_names is not None:
            track_name = track_names[track_int]
        else:
            track_name = f"Track {track_int}"

        time = 0
        print(track_name)
        output_file.addTrackName(track_int, time, track_name)
        ice_bucket = []

        for section in track:
            s = 0  # phrase counter

            for phrase in section:
                if callable(phrase):
                    phrase = phrase()
                t = 0  # note counter

                for note in phrase:
                    if note is None:
                        note = [None, 0, freezer()]
                    if type(note) is int:
                        pitch = note
                        note = [pitch, 80, freezer()]

                    pitch, vel, freezer_func = note
                    if freezer_func is None:
                        freezer_func = freezer()
                    ice_tray, time = freezer_func(pitch, vel, time, s, t)
                    ice_bucket.extend(ice_tray)
                    t += 1
                s += 1

    for cube in ice_bucket:
        pitch, time, note_len, vel = cube
        output_file.addNote(
            track=track_int,
            channel=0,
            pitch=pitch,
            time=time,
            duration=note_len,
            volume=vel,
        )

    filename = f"{filename}.mid"
    with open(filename, "wb") as outf:
        output_file.writeFile(outf)
        print(f"Wrote to file {filename}.")


def freeze_track(track: list, name: Optional[str] = None):
    freeze_song(song=[track], filename=name, track_names=[name])


def freeze_section(section: list, name: Optional[str] = None):
    freeze_track(track=[section], name=name)


def freeze_phrase(phrase: list, name: Optional[str] = None):
    section = [phrase]
    freeze_section(section, name)


if __name__ == "__main__":
    names = [name for name in dir() if not name.startswith("_")]
    imports = ["Callable", "datetime", "MIDIFile", "Optional"]
    for name in imports:
        names.remove(name)
    print(", ".join(names))

    chill(27, None, 0, 0)
