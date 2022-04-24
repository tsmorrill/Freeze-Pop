import random


def guido(lyric):
    """Probalistically assign pitches to text using method of Guido d'Arezzo.
    """
    lyric = lyric.upper()
    vowels = [char for char in lyric if char in "AEIOU"]

    dict = {"A": [55, 64, 72, 81],                # MIDI notes : G3, E4, C5, A5
            "E": [57, 65, 74],                                 # A3, F4, D5
            "I": [59, 67, 76],                                 # B3, G4, E5
            "O": [60, 69, 77],                                 # C4, A4, F5
            "U": [62, 71, 79]}                                 # D4, B4, G5

    def weighting(potential_notes, prev_note):
        if prev_note is None:
            return [1 for note in potential_notes]
        weights = [1/max(abs(note - prev_note), 1/2)      # avoid division by 0
                   for note in potential_notes]
        return weights

    note_list = []
    prev_note = None

    for char in vowels:
        potential_notes = dict[char]
        weights = weighting(potential_notes, prev_note)
        new_note = random.choices(potential_notes, weights, k=1)[0]
        note_list.append(new_note)
        prev_note = new_note
    return note_list


if __name__ == "__main__":
    lyric = "Sphinx of black quartz, judge my vow."
    print(lyric)
    print(guido(lyric))
