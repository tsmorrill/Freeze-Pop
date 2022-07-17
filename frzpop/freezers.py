from datetime import datetime
from frzpop import additives
from math import floor
from midiutil import MIDIFile
from typing import Callable, Optional

rng = additives.rng


def try_calling(x):
    if callable(x):
        output = x()
    else:
        output = x
    return output


def check(pitch: int, onset: float, duration: float, vel: int) -> tuple:
    """Check types and return an icecube."""
    assert (
        pitch in range(128)
    ), f"Expected an integer 0-127 or None. Recieved {pitch}."
    assert type(onset) == float, f"Expected a float. Recieved {onset}."
    assert type(duration) == float, f"Expected a float. Recieved {duration}."
    assert vel in range(
        128
    ), f"Expected an integer 0-127. Received {vel}."


def freezer(
    duration: float = 1 / 16,
    gate: float = 1.0,
    nudge: float = 0.0,
    repeats: int = 1,
    repeats_offset: float = 1 / 16,
    repeats_decay: float = 1.0,
    ratcheting: bool = False,
    prob: float = 1.0,
    seed=None,
    condition_freq: int = 0,
    condition_offset: int = 0,
    advance_time: bool = True,
) -> Callable:
    """Create a freezer function."""
    duration *= 4  # midiutil measures time floats in quarter notes
    if prob < 1.0:
        noise = rng(seed=seed)

    def freezer_func(pitch, vel, time: float, s: int, t: int) -> tuple[list, float]:
        pitch = try_calling(pitch)
        onset = float(time + nudge)
        if ratcheting:
            repeats_offset = duration / repeats
        vel = try_calling(vel)
        check(pitch, onset, duration, vel)
        if prob >= 1.0:
            under_prob = True
        else:
            under_prob = noise() > prob
        condition = s % condition_freq == condition_offset
        ice_tray = []
        if under_prob and condition and vel != 0:
            for r in range(repeats):
                cube_onset = onset + r * repeats_offset
                cube_duration = duration * gate
                if ratcheting:
                    cube_duration /= repeats
                cube_vel = floor(vel * repeats_decay ** r)
                cube = (pitch, cube_onset, cube_duration, cube_vel)
                ice_tray.append(cube)
        if advance_time:
            time += duration
        return ice_tray, time

    return freezer_func


def cond(duration: float = 1 / 16, gate: float = 1.0, nudge: float = 0.0, freq: int = 0, offset: int = 0) -> Callable:
    return freezer(duration=duration, gate=gate, nudge=nudge, condition_freq=freq, condition_offset=offset)


def prob(duration: float = 1 / 16, gate: float = 1.0, nudge: float = 0.0, prob: float = 1.0, seed=None) -> Callable:
    return freezer(duration=duration, gate=gate, nudge=nudge, prob=prob, seed=seed)


def simul(duration: float = 1 / 16, gate: float = 1.0, nudge: float = 0.0) -> Callable:
    return freezer(duration=duration, gate=gate, nudge=nudge, advance_time=False)


def ratchet(duration: float = 1 / 16, gate: float = 1.0, nudge: float = 0.0, ratchets: int = 1) -> Callable:
    return freezer(duration=duration, gate=gate, nudge=nudge, repeats=ratchets, ratcheting=True)


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
                phrase = try_calling(phrase)
                t = 0  # note counter

                for note in phrase:
                    note = try_calling(note)
                    if note is None:
                        note = [0, 0, freezer()]
                    if type(note) is int:
                        pitch = note
                        note = [pitch, 92, freezer()]

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
