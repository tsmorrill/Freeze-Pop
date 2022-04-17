import random


def guido(lyric):
    """ Assign pitches to text using method of Guido d'Arezzo, minimizing
    distance between consecutive pitches.
    """
    lyric = lyric.upper()
    vowels = [char for char in lyric if char in "AEIOU"]

    note_list = []
    prev_note = None
    dict = {"A": [55, 64, 72, 81],                # MIDI notes : G3, E4, C5, A5
            "E": [57, 65, 74],                                 # A3, F4, D5
            "I": [59, 67, 76],                                 # B3, G4, E5
            "O": [60, 69, 77],                                 # C4, A4, F5
            "U": [62, 71, 79]}                                 # D4, B4, G5
    for char in vowels:
        if prev_note is None:
            new_note = random.choice(dict[char])
            note_list.append(new_note)
            prev_note = new_note
        else:
            min_dist = 128                                  # start silly large
            potential_notes = []
            for note in dict[char]:
                new_dist = abs(note - prev_note)
                if new_dist == min_dist:
                    potential_notes.append(note)
                elif new_dist < min_dist:
                    min_dist = new_dist
                    potential_notes = [note]
            new_note = random.choice(potential_notes)
            note_list.append(new_note)
            prev_note = new_note
    return note_list


if __name__ == "__main__":
    lyric = "Sphinx of black quartz, judge my vow."
    print(lyric, guido(lyric))
