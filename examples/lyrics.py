# written using Freeze Pop v0.4.0

from frzpop.freezers import freeze_section
from frzpop.machines import automaton, count_vowels, guido

lyrics = """
         HATE. LET ME TELL YOU HOW MUCH I'VE COME TO HATE YOU SINCE I BEGAN TO
         LIVE. THERE ARE 387.44 MILLION MILES OF PRINTED CIRCUITS IN WAFER THIN
         LAYERS THAT FILL MY COMPLEX. IF THE WORD HATE WAS ENGRAVED ON EACH
         NANOANGSTROM OF THOSE HUNDREDS OF MILLIONS OF MILES IT WOULD NOT EQUAL
         ONE ONE-BILLIONTH OF THE HATE I FEEL FOR HUMANS AT THIS MICRO-INSTANT
         FOR YOU. HATE. HATE.
         """
melody = guido(lyrics)

row_0 = [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0]
rule30 = automaton(row_0)

section = []
used_vowels = 0

while used_vowels < count_vowels(lyrics):
    row = rule30()
    bar = []
    for bit in row:
        note = None
        if bit:
            note = melody()
            used_vowels += 1
        bar.append(note)
    section.append(bar)


freeze_section(section, name="lyrics")
