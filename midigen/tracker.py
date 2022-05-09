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
    def __init__(self, cmd):
        if cmd is None:
            cmd = Freezer.freeze_note
        self.cmd = cmd
        pass

    @classmethod
    def freeze_func(func, phrase_counter):
        if isinstance(func, Callable):
            return(func(phrase_counter))
        return(func)

    @classmethod
    def freeze_note(cls, Note, track=0, channel=0, time=0, duration=0,
                    phrase_counter=0, note_counter=0):
        pitch = Freezer.freeze_func(note.pitch, phrase_counter)
        vel = Freezer.freeze_func(note.vel, phrase_counter)

        cube = Cube(track, channel, pitch, time, duration, vel)
        cubes = [cube]

        return cubes

    @classmethod
    def from_proposition(cls, proposition):
        def func(Note, track=0, channel=0, time=0, duration=0,
                 phrase_counter=0, note_counter=0):
            cubes = []
            if proposition(phrase_counter, note_counter):
                cubes = Freezer.freeze_Note(Note,
                                            track=0,
                                            channel=0,
                                            time=0,
                                            duration=0,
                                            phrase_counter=0,
                                            note_counter=0)
            return(cubes)

        return Freezer(func)


class Note:
    def __init__(self, pitch, vel, freezer):
        if freezer is None:
            freezer = Freezer(None)
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
