from datetime import datetime
from frzpop import additives
from math import floor
from midiutil import MIDIFile
from typing import Callable, Optional

try_calling = additives.try_calling
rng = additives.rng


def check(cube: tuple[int, float, float, int]):
    pitch, onset, duration, vel = cube
    err_str = f"Expected an integer 0-127. Recieved {pitch}."
    assert pitch in range(128), err_str
    err_str = f"Expected a float. Recieved {onset}."
    assert type(onset) == float, err_str
    err_str = f"Expected a positive float. Recieved {duration}."
    assert type(duration) == float and duration > 0, err_str
    err_str = f"Expected an integer 0-127. Received {vel}."
    assert vel in range(128), err_str


def freezer(
    duration: float = 1 / 16,
    gate: float = 1.0,
    nudge: float = 0.0,
    repeats: int = 1,
    ratcheting: bool = False,
    repeats_offset: float = 1 / 16,
    repeats_decay: float = 1.0,
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
        vel = try_calling(vel)
        if prob >= 1.0:
            under_prob = True
        else:
            under_prob = noise() > prob
        once_every = s % condition_freq == condition_offset
        ice_tray = []
        if under_prob and once_every and vel != 0:
            cube_duration = duration * gate
            if ratcheting:
                cube_duration /= repeats
                repeats_offset = duration / repeats
            for r in range(repeats):
                cube_onset = time + nudge + r * repeats_offset
                cube_vel = floor(vel * repeats_decay ** r)
                cube = (pitch, cube_onset, cube_duration, cube_vel)
                check(cube)
                ice_tray.append(cube)
        if advance_time:
            time += duration
        return ice_tray, time

    return freezer_func


def cond(
    freq: int = 0,
    offset: int = 0,
    duration: float = 1 / 16,
    gate: float = 1.0,
    nudge: float = 0.0,
) -> Callable:
    return freezer(
        duration=duration,
        gate=gate,
        nudge=nudge,
        condition_freq=freq,
        condition_offset=offset,
    )


def prob(
    prob: float = 1.0,
    seed=None,
    duration: float = 1 / 16,
    gate: float = 1.0,
    nudge: float = 0.0,
) -> Callable:
    return freezer(duration=duration, gate=gate, nudge=nudge, prob=prob, seed=seed)


def simul(duration: float = 1 / 16, gate: float = 1.0, nudge: float = 0.0) -> Callable:
    return freezer(duration=duration, gate=gate, nudge=nudge, advance_time=False)


def ratchet(
    ratchets: int = 1,
    duration: float = 1 / 16,
    gate: float = 1.0,
    nudge: float = 0.0,
) -> Callable:
    return freezer(
        duration=duration, gate=gate, nudge=nudge, ratcheting=True, repeats=ratchets
    )


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

        time = 0.0
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
                    elif type(note) is int:
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
