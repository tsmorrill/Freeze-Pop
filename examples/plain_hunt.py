import frzpop
from frzpop.notes import *
from frzpop.dynamics import f
from frzpop.phrases import make_plain_hunt

init_phrase = [[C4, f, None],
               [B3, f, None],
               [A3, f, None],
               [G3, f, None],
               [F3, f, None],
               [E3, f, None],
               [D3, f, None],
               [C3, f, None]]
phrase_generator = make_plain_hunt(init_phrase)

section = [phrase_generator for _ in range(16)]

frzpop.freeze_section(section, name="plain_hunt")
