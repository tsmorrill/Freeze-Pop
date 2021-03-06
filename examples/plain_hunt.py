# written using Freeze Pop v 0.4.0

from frzpop import dynamics
from frzpop.freezers import freezer, freeze_section
from frzpop.notes import C4, D4, E4, F4, G4, A4, B4, C5
from frzpop.shuffle import plain_hunt

eighth = freezer(note_len=1/8)

f = dynamics.f()

init_phrase = [[C5, f, eighth],
               [B4, f, eighth],
               [A4, f, eighth],
               [G4, f, eighth],
               [F4, f, eighth],
               [E4, f, eighth],
               [D4, f, eighth],
               [C4, f, eighth]]
machine = plain_hunt(init_phrase)

section = [machine for _ in range(16)]

freeze_section(section, name="plain_hunt")
