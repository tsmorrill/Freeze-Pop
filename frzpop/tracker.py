from typing import Callable
from itertools import chain
from random import random


class Cube:
    def __init__(self, pitch, time, note_len, vel):
        self.pitch = pitch
        self.time = time
        self.note_len = note_len
        self.vel = vel


class Freezer:
    def __init__(self, freeze):
        if freeze is None:
            freeze = Freezer.freeze_note
        self.freeze = freeze
        pass

    @classmethod
    def freeze_func(func, note_counter):
        if isinstance(func, Callable):
            return(func(note_counter))
        return(func)

    @classmethod
    def freeze_note(cls, note, time=0, phrase_counter=0,
                    note_counter=0):
        pitch = Freezer.freeze_func(note.pitch, note_counter)
        vel = Freezer.freeze_func(note.vel, note_counter)
        len = note.len

        cube = Cube(pitch, time, len, vel)
        cubes = [cube]
        time = time + len

        return(cubes, time)

    @classmethod
    def conditional(cls, condition):
        def func(note, time=0, phrase_counter=0, note_counter=0):
            if condition(phrase_counter, note_counter):
                cubes = Freezer.freeze_Note(note, time, phrase_counter,
                                            note_counter)
                return(cubes)
            return([])
        return Freezer(func)

    @classmethod
    def mod(k, n, offset=0):
        def func(phrase_counter, note_counter):
            return(bool(phrase_counter - offset % n == 0))
        return(Freezer.contitional(func))

    @classmethod
    def prob(percent):
        if percent < 0 or percent > 100:
            raise ValueError("percent must be within 0 and 100 inclusive")

        def func(phrase_counter, note_counter):
            return(bool(random() < percent/100))
        return(Freezer.contitional(func))

    # @classmethod
    # def ratchet(mult):
    #     def func(note, time=0, phrase_counter=0, note_counter=0):
    #         for n in range(mult):
    #             pass
    #     return(Freezer(func))


class Note:
    def __init__(self, pitch, vel=88, len=1/4, freezer=None):
        if freezer is None:
            freezer = Freezer(None)
        self.pitch = pitch
        self.vel = vel
        self.len = len
        self.freezer = freezer

    def freeze(self, time=0, phrase_counter=0, note_counter=0):
        cubes, time = self.freezer.freeze(self, time, phrase_counter,
                                          note_counter)
        return(cubes, time)


class Phrase:
    def __init__(self, notes):
        self.notes = []

        for note in notes:
            if note is None:
                note = Note(0, 0, None)
            self.notes.append(note)

    @classmethod
    def from_pitches(cls, pitches, vel=88, len=1/4, freezer=None):
        notes = []
        for pitch in pitches:
            if pitch is None:
                note = None
            else:
                note = Note(pitch, vel, len, freezer)
            notes.append(note)
        return(Phrase(notes))

    @classmethod
    def from_trigs(cls, trigs, pitch=60, vel=88, len=1/4, freezer=None):
        notes = [Note(pitch, vel, len, freezer) if bool else None
                 for bool in trigs]
        return(Phrase(notes))

    def freeze(self, time=0, phrase_counter=0):
        ice_tray = []
        for note_counter, note in enumerate(self.notes):
            cubes, time = note.freeze(time, phrase_counter, note_counter)
            ice_tray.extend(cubes)
        cubes = chain.from_iterable(ice_tray)
        return(cubes, time)


class Section:
    def __init__(self, phrases, time=0):
        self.phrases = phrases
        self.time = time

    def freeze(self, time=0):
        ice_tray = []
        for phrase_counter, phrase in enumerate(self.phrases):
            cubes, time = phrase.freeze(time, phrase_counter)
            ice_tray.extend(cubes)
        cubes = chain.from_iterable(ice_tray)
        return(cubes)


class Track:
    def __init__(self, sections, channel=0):
        self.sections = sections
        self.channel = channel

    def freeze(self, time):
        time = 0
        ice_tray = []
        for section in self.sections:
            cubes, time = section.freeze(time)
            ice_tray.extend(cubes)
        cubes = chain.from_iterable(ice_tray)
        return(cubes)


class Song:
    def __init__(self, name, tracks):
        self.name = name
        self.chains = tracks

    def freeze(self):
        ice_tray = [track.freeze for track in self.tracks]
        cubes = chain.from_iterable(ice_tray)
        return(cubes)

    def to_file(self):
        cubes = self.freeze()
        for cube in cubes:
            pass


if __name__ == "__main__":
    phrase = Phrase.from_trigs([True, True, False, True])
    for note in phrase.notes:
        print(note.pitch)
