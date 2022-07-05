def guido(lyric, gamut=None, seed=None):
    """Generate text-to-pitches method of Guido d'Arezzo using randomness."""
    lyric = lyric.upper()
    vowels = [char for char in lyric if char in "AEIOU"]

    if gamut is None:                     # historical origin of the word gamut
        gamut = [55, 57, 59, 60, 62,         # list indices will be taken mod 5
                 64, 65, 67, 69, 71,
                 72, 74, 76, 77, 79,
                 81]

    note_assignment = {"A": gamut[0::5],
                       "E": gamut[1::5],
                       "I": gamut[2::5],
                       "O": gamut[3::5],
                       "U": gamut[4::5]}

    def weigh(potential_notes, prev_note):
        if prev_note is None:
            return [1 for note in potential_notes]
        weights = [1/max(abs(note - prev_note), 1/2)      # avoid division by 0
                   for note in potential_notes]
        return weights

    notes = []
    prev_note = None
    noise = rng(seed)

    # not sure how to implement next block this way

    for char in vowels:
        potential_notes = note_assignment[char]
        weights = weigh(potential_notes, prev_note)
        new_note = random.choices(potential_notes, weights, k=1)[0]
        notes.append(new_note)
        prev_note = new_note
    return list_reader(notes)
