from midiutil import MIDIFile
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

    @classmethod
    def freeze_func(cls, func, note_counter):
        if callable(func):
            return func(note_counter)
        return func

    @classmethod
    def freeze_note(cls, note, time=0, phrase_counter=0,
                    note_counter=0):
        pitch = Freezer.freeze_func(note.pitch, note_counter)
        vel = Freezer.freeze_func(note.vel, note_counter)
        len = note.len

        cube = Cube(pitch, time, len, vel)
        cubes = [cube]
        time = time + len

        return cubes, time

    @classmethod
    def conditional(cls, condition):
        def func(note, time=0, phrase_counter=0, note_counter=0):
            cubes = []
            if condition(phrase_counter, note_counter):
                cubes = Freezer.freeze_Note(note, time, phrase_counter,
                                            note_counter)
            return cubes
        return Freezer(func)

    @classmethod
    def mod(k, n, offset=0):
        def func(phrase_counter, note_counter):
            return (phrase_counter - offset) % n == 0
        return Freezer.contitional(func)

    @classmethod
    def prob(percent):
        if percent < 0 or percent > 100:
            raise ValueError("percent must be within 0 and 100 inclusive")

        def func(phrase_counter, note_counter):
            return random() < percent/100
        return Freezer.contitional(func)

    # @classmethod
    # def ratchet(mult):
    #     def func(note, time=0, phrase_counter=0, note_counter=0):
    #         for n in range(mult):
    #             pass
    #     return Freezer(func)


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
        return cubes, time


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
        return Phrase(notes)

    @classmethod
    def from_trigs(cls, trigs, pitch=60, vel=88, len=1/4, freezer=None):
        notes = [Note(pitch, vel, len, freezer) if bool else None
                 for bool in trigs]
        return Phrase(notes)

    def freeze(self, time=0, phrase_counter=0):
        ice_tray = []
        for note_counter, note in enumerate(self.notes):
            cubes, time = note.freeze(time, phrase_counter, note_counter)
            ice_tray.extend(cubes)
        return ice_tray, time


class Section:
    def __init__(self, phrases, time=0):
        self.phrases = phrases
        self.time = time

    def freeze(self, time=0):
        ice_tray = []
        for phrase_counter, phrase in enumerate(self.phrases):
            cubes, time = phrase.freeze(time, phrase_counter)
            ice_tray.extend(cubes)
        return ice_tray, time


class Track:
    def __init__(self, sections, name=None, channel=0):
        self.sections = sections
        self.name = name
        self.channel = channel

    def freeze(self, time=0):
        time = 0
        ice_tray = []
        for section in self.sections:
            cubes, time = section.freeze(time)
            ice_tray.extend(cubes)
        return cubes


class Song:
    def __init__(self, name, tracks):
        self.name = name
        self.tracks = tracks

    def render(self):
        output_file = MIDIFile()
        for track_number, track in enumerate(self.tracks):
            time = 0
            track_name = track.name
            if track_name is None:
                track_name = f"Track {track_number}"
            output_file.addTrackName(track_number, time, track_name)
            for cube in track.freeze(time):
                output_file.addNote(track_number,
                                    track.channel,
                                    cube.pitch,
                                    cube.time,
                                    cube.note_len,
                                    cube.vel)
            filename = f"{self.name}.mid"
            with open(filename, 'wb') as outf:
                output_file.writeFile(outf)


if __name__ == "__main__":
    phrase = Phrase.from_pitches([60, 62, 64, 65, 67, 69, 71, 72])
    section = Section([phrase])
    track = Track([section])
    song = Song("Scale", [track])
    song.render()
