from typing import Callable

C0 = 12
Db0 = 13
D0 = 14
Eb0 = 15
E0 = 16
F0 = 17
Gb0 = 18
G0 = 19
Ab0 = 20
A0 = 21
Bb0 = 22
B0 = 23
C1 = 24
Db1 = 25
D1 = 26
Eb1 = 27
E1 = 28
F1 = 29
Gb1 = 30
G1 = 31
Ab1 = 32
A1 = 33
Bb1 = 34
B1 = 35
C2 = 36
Db2 = 37
D2 = 38
Eb2 = 39
E2 = 40
F2 = 41
Gb2 = 42
G2 = 43
Ab2 = 44
A2 = 45
Bb2 = 46
B2 = 47
C3 = 48
Db3 = 49
D3 = 50
Eb3 = 51
E3 = 52
F3 = 53
Gb3 = 54
G3 = 55
Ab3 = 56
A3 = 57
Bb3 = 58
B3 = 59
C4 = 60
Db4 = 61
D4 = 62
Eb4 = 63
E4 = 64
F4 = 65
Gb4 = 66
G4 = 67
Ab4 = 68
A4 = 69
Bb4 = 70
B4 = 71
C5 = 72
Db5 = 73
D5 = 74
Eb5 = 75
E5 = 76
F5 = 77
Gb5 = 78
G5 = 79
Ab5 = 80
A5 = 81
Bb5 = 82
B5 = 83
C6 = 84
Db6 = 85
D6 = 86
Eb6 = 87
E6 = 88
F6 = 89
Gb6 = 90
G6 = 91
Ab6 = 92
A6 = 93
Bb6 = 94
B6 = 95
C7 = 96
Db7 = 97
D7 = 98
Eb7 = 99
E7 = 100
F7 = 101
Gb7 = 102
G7 = 103
Ab7 = 104
A7 = 105
Bb7 = 106
B7 = 107
C8 = 108
Db8 = 109
D8 = 110
Eb8 = 111
E8 = 112
F8 = 113
Gb8 = 114
G8 = 115
Ab8 = 116
A8 = 117
Bb8 = 118
B8 = 119
C9 = 120
Db9 = 121
D9 = 122
Eb9 = 123
E9 = 124
F9 = 125
Gb9 = 126
G9 = 127


def expressive(func):
    # stress pattern of 16th notes in common time
    stresses = [7, -1, 3, -5, 5, -3, 1, -7, 6, -2, 2, -6, 4, -4, 0, -8]

    def wrap(t):
        # add current stress to velocity
        t %= 16
        val = func() + stresses[t]
        val = max(0, min(val, 127))
        return val
    return wrap


@expressive
def ppp(): return(8)                                          # 0 < ppp < 15


@expressive
def pp(): return(24)                                          # 16 < pp < 31


@expressive
def p(): return(40)                                           # 32 < p < 47


@expressive
def mp(): return(56)                                          # 48 < mp < 63


@expressive
def mf(): return(72)                                          # 64 < mf < 79


@expressive
def f(): return(88)                                           # 80 < f < 95


@expressive
def ff(): return(104)                                         # 96 < ff < 111


@expressive
def fff(): return(120)                                        # 112 < fff < 127


def process_function(func, t):
    if isinstance(func, Callable):
        return func(t)
    return func


def none_cmd(pitch, vel, s, t):
    midi_note = process_function(pitch, t)
    midi_vel = process_function(vel, t)
    print(f"At phrase {s}, time {t} play pitch {midi_note} "
          + f"with velocity {midi_vel}.")


def print_cmd(pitch, vel, s, t):
    midi_note = process_function(pitch, t)
    midi_vel = process_function(vel, t)
    print(f"At phrase {s}, time {t} play pitch {midi_note} "
          + f"with velocity {midi_vel}.")


class Note:
    def __init__(self, pitch, vel, cmd):
        if cmd is None:
            cmd = none_cmd
        self.pitch = pitch
        self.vel = vel
        self.cmd = cmd

    @classmethod
    def process_function(func, t):
        if isinstance(func, Callable):
            return func(t)
        return func

    def render(self, s, t):
        self.cmd(self.pitch, self.vel, s, t)


class Phrase:
    def __init__(self, notes, time_sig):
        len, unit = time_sig
        self.notes = []

        for note in notes:
            if note is None:
                note = Note(0, 0, None)
            self.notes.append(note)

        self.len = len
        self.unit = unit

    @classmethod
    def from_pitches(cls, pitches, vel=88, cmd=None):
        notes = []
        for pitch in pitches:
            if pitch is None:
                note = None
            else:
                note = Note(pitch, vel, cmd)
            notes.append(note)
        time_sig = [None, None]
        return(Phrase(notes, time_sig))

    @classmethod
    def from_trigs(cls, trigs, pitch=60, vel=88, cmd=None):
        notes = []
        for bool in trigs:
            note = Note(pitch, vel, cmd) if bool else None
            notes.append(note)
        time_sig = [None, None]
        return(Phrase(notes, time_sig))


class Chain:
    def __init__(self, phrases):
        self.phrases = phrases


class Song:
    def __init__(self, chains):
        self.chains = chains


if __name__ == "__main__":
    phrase = Phrase.from_trigs([True, True, False, True])
    for note in phrase.notes:
        print(note.pitch)
