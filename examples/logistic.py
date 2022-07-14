# written using Freeze Pop v 0.4.0

import frzpop
from frzpop.chords import dom7
from frzpop.machines import logistic
from frzpop.quantize import quantizer

f = 88                                                                  # forte

quarter = frzpop.freezers.freezer(note_len=1/4)
eighth = frzpop.freezers.freezer(note_len=1/8)
sixteenth = frzpop.freezers.freezer(note_len=1/16)

function_generator = logistic(0.25)

D = 62
Ddom7 = dom7(D)

quantizer = quantizer(Ddom7)

note_list_0 = [quantizer(20*function_generator() + 38) for _ in range(8)]

phrase_0 = [[note_list_0[0], f, quarter],
            [note_list_0[1], f, eighth],
            [note_list_0[2], f, eighth],
            [note_list_0[3], f, eighth],
            [note_list_0[4], f, sixteenth],
            [note_list_0[5], f, sixteenth],
            [note_list_0[6], f, eighth],
            [note_list_0[7], f, eighth]]

note_list_1 = [quantizer(18*function_generator() + 42) for _ in range(8)]

phrase_1 = [[note_list_1[0], f, quarter],
            [note_list_1[1], f, eighth],
            [note_list_1[2], f, eighth],
            [note_list_1[3], f, eighth],
            [note_list_1[4], f, sixteenth],
            [note_list_1[5], f, sixteenth],
            [note_list_1[6], f, eighth],
            [note_list_1[7], f, eighth]]


section = [phrase_0, phrase_1, phrase_0, phrase_1[::-1],
           phrase_0, phrase_0, phrase_1, phrase_0[::-1]]

frzpop.freezers.freeze_section(section, name="logistic")
