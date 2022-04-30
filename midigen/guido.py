import random

guido_scale = [55, 57, 59, 60, 62,           # list indices will be taken mod 5
               64, 65, 67, 69, 71,
               72, 74, 76, 77, 79,
               81]


def guido(lyric, scale=guido_scale):
    """Probalistically assign pitches to text using method of Guido d'Arezzo.
    """
    lyric = lyric.upper()
    vowels = [char for char in lyric if char in "AEIOU"]

    dict = {"A": scale[0::5],
            "E": scale[1::5],
            "I": scale[2::5],
            "O": scale[3::5],
            "U": scale[4::5]}

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
