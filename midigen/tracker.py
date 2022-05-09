from typing import Callable
from itertools import chain


class Cube:
    def __init__(self, track, channel, pitch, time, duration, vel):
        self.track = track
        self.channel = channel
        self.pitch = pitch
        self.time = time
        self.duration = duration
        self.vel = vel


class Freezer:
    @classmethod
    def freeze_func(func, phrase_counter):
        if isinstance(func, Callable):
            return(func(phrase_counter))
        return(func)

    @classmethod
    def none_freezer(track, channel, time, note,
                     chain_counter, phrase_counter):
        pitch = note.pitch
        vel = note.vel

        midi_note = Freezer.freeze_func(pitch, phrase_counter)
        midi_vel = Freezer.freeze_func(vel, phrase_counter)

        cube = Cube(track, channel, midi_note, time, duration, midi_vel)
        cubes = [cube]

        return(cubes)

    def __init__(self):
        pass

    def freeze_note(Note):
        pitch = Note.pitch
        cubes =
        return cubes


class Note:
    def __init__(self, pitch, vel, freezer):
        if freezer is None:
            freezer = none_freezer
        self.pitch = pitch
        self.vel = vel
        self.freezer = freezer

    def freeze(self, s=0, t=0):
        cubes = self.freezer(self.pitch, self.vel, s, t)
        return(cubes)


class Phrase:
    def __init__(self, notes, time_sig):
        self.notes = []

        for note in notes:
            if note is None:
                note = Note(0, 0, None)
            self.notes.append(note)

        self.time_sig = time_sig

    @classmethod
    def from_pitches(cls, pitches, vel=88, freezer=None, time_sig=None):
        notes = []
        for pitch in pitches:
            if pitch is None:
                note = None
            else:
                note = Note(pitch, vel, freezer)
            notes.append(note)
        return(Phrase(notes, time_sig))

    @classmethod
    def from_trigs(cls, trigs, pitch=60, vel=88, freezer=None, time_sig=None):
        notes = [Note(pitch, vel, freezer) if bool else None for bool in trigs]
        return(Phrase(notes, time_sig))

    def freeze(self, s=0):
        ice_tray = [note.freeze(s, t) for t, note in enumerate(self.notes)]
        cubes = chain.from_iterable(ice_tray)
        return cubes


class Chain:
    def __init__(self, phrases):
        self.phrases = phrases

    def freeze(self):
        ice_tray = [phrase.freeze(s) for s, phrase in enumerate(self.chains)]
        cubes = chain.from_iterable(ice_tray)
        return cubes


class Track:
    def __init__(self, chains, channel):
        self.chains = chains
        self.channel = channel

    def freeze(self):
        ice_tray = [chain.freeze for chain in self.chains]
        cubes = chain.from_iterable(ice_tray)
        return cubes


class Song:
    def __init__(self, tracks):
        self.chains = tracks


if __name__ == "__main__":
    phrase = Phrase.from_trigs([True, True, False, True])
    for note in phrase.notes:
        print(note.pitch)
