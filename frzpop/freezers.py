from datetime import datetime
from midiutil import MIDIFile
from typing import Callable, Optional


def try_calling(x) -> Optional[int]:
    if callable(x):
        output = x()
    else:
        output = x
    return output


def chill(pitch: int, onset: float, duration: float, vel: int) -> tuple:
    """Check types and return an icecube."""
    assert (
        pitch in range(128)
    ), f"Expected an integer 0-127 or None. Recieved {pitch}."
    assert type(onset) == float, f"Expected a float. Recieved {onset}."
    assert type(duration) == float, f"Expected a float. Recieved {duration}."
    assert vel in range(
        128
    ), f"Expected an integer 0-127. Received {vel}."
    return (pitch, onset, duration, vel)


def freezer(
    duration: float = 1 / 16,
    gate: float = 1.0,
    nudge: float = 0.0,
    advance_time: bool = True,
) -> Callable:
    """Create a freezer function."""
    duration *= 4  # midiutil measures time floats in quarter notes
    gate *= duration

    def freezer_func(pitch, vel, time: float, s: int, t: int) -> tuple[list, float]:
        pitch = try_calling(pitch)
        onset = float(time + nudge)
        vel = try_calling(vel)
        ice_tray = []
        if pitch is not None and vel != 0:
            icecube = chill(pitch, onset, duration, vel)
            ice_tray.append(icecube)
        if advance_time:
            time += duration
        return ice_tray, time

    return freezer_func


def simul(duration: float = 1 / 16, gate: float = 1.0, nudge: float = 0.0) -> Callable:
    return freezer(duration=duration, gate=gate, nudge=nudge, advance_time=False)


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
        pitch, onset, duration, vel = cube
        output_file.addNote(
            track=track_int,
            channel=0,
            pitch=pitch,
            time=onset,
            duration=duration,
            volume=vel,
        )

    filename = f"{filename}.mid"
    with open(filename, "wb") as outf:
        output_file.writeFile(outf)
        print(f"Wrote to file {filename}.")


def freeze_track(track: list, name: Optional[str] = None):
    if name is not None:
        track_names = [name]
    else:
        track_names = None
    freeze_song(song=[track], filename=name, track_names=track_names)


def freeze_section(section: list, name: Optional[str] = None):
    freeze_track(track=[section], name=name)


def freeze_phrase(phrase: list, name: Optional[str] = None):
    freeze_section(section=[phrase], name=name)


if __name__ == "__main__":
    names = [name for name in dir() if not name.startswith("_")]
    imports = ["Callable", "datetime", "MIDIFile", "Optional"]
    for name in imports:
        names.remove(name)
    print(", ".join(names))
