# written using Freeze Pop v 0.4.3

import frzpop
from frzpop.freezers import freezer, freeze_phrase
from frzpop.quantize import quantizer

F = 65

chord = frzpop.chords.major(F)
q_chord = quantizer(chord)

scale = frzpop.scales.major(F)
pickups = [note for note in scale if note not in chord]
q_scale = quantizer(pickups)

contour = frzpop.machines.contour(iter=4, init=[0, 0.75, 0, 0.5, 0.25])
melody = frzpop.machines.attenuvert(contour, mult=26, offset=58)

eighth = freezer(note_len=1/8)
sixteenth = freezer(note_len=1/16)
pickup = freezer(note_len=1/16, nudge=1/11)

phrase = [
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, sixteenth],
    [q_scale(melody()), 92, pickup],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, sixteenth],
    [q_scale(melody()), 92, pickup],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, sixteenth],
    [q_scale(melody()), 92, pickup],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, sixteenth],
    [q_scale(melody()), 92, pickup],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, sixteenth],
    [q_scale(melody()), 92, pickup],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, sixteenth],
    [q_scale(melody()), 92, pickup],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, sixteenth],
    [q_scale(melody()), 92, pickup],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, sixteenth],
    [q_scale(melody()), 92, pickup],
    [q_chord(melody()), 92, eighth],
    [q_chord(melody()), 92, eighth],
]

freeze_phrase(phrase, name="contour")
