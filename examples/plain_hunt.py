import frzpop
from frzpop.notes import C4, D4, E4, F4, G4, A4, B4, C5
from frzpop.dynamics import f
from frzpop.phrases import make_plain_hunt

eighth = frzpop.freezers.make_freezer(note_len=1/2)

init_phrase = [[C5, f, eighth],
               [B4, f, eighth],
               [A4, f, eighth],
               [G4, f, eighth],
               [F4, f, eighth],
               [E4, f, eighth],
               [D4, f, eighth],
               [C4, f, eighth]]
phrase_generator = make_plain_hunt(init_phrase)

section = [phrase_generator for _ in range(16)]

frzpop.freeze_section(section, name="plain_hunt")
