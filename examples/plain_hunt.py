import frzpop
from frzpop.notes import C3, D3, E3, F3, G3, A3, B3, C4
from frzpop.dynamics import f
from frzpop.phrases import make_plain_hunt

eighth = frzpop.freezers.make_freezer(note_len=1/2)

init_phrase = [[C4, f, eighth],
               [B3, f, eighth],
               [A3, f, eighth],
               [G3, f, eighth],
               [F3, f, eighth],
               [E3, f, eighth],
               [D3, f, eighth],
               [C3, f, eighth]]
phrase_generator = make_plain_hunt(init_phrase)

section = [phrase_generator for _ in range(16)]

frzpop.freeze_section(section, name="plain_hunt")
