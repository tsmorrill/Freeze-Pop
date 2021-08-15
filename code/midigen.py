from heightmap import heightmap_1D

class Song:

    def __init__(self, skeleton, sections):
        self.skeleton = skeleton
        self.sections = sections

    def mutate(self):
        pass

class Skeleton:

    def __init__(self):
        pass

    def mutate(self):
        pass

class Section:

    def __init__(self, skeleton, themes):
        self.skeleton = skeleton
        self.themes = themes

    def mutate(self):
        pass

class Theme:

    def __init__(self, skeleton, phrases):
        self.skeleton = skeleton
        self.phrases = phrases

    def mutate(self):
        pass

class Phrase:

    def __init__(self, skeleton, flows):
        self.skeleton = skeleton
        self.flows = flows

    def mutate(self):
        pass

class Flow:

    def __init__(self, stress, pitch):
        self.stress = stress
        self.pitch = pitch

    def mutate(self):
        pass

    @staticmethod
    def from_seed_1D(iter, smoothing, seed, init):
        stress = heightmap_1D(iter, smoothing, seed + "stress", init)
        pitch = heightmap_1D(iter, smoothing, seed + "pitch", init)
        return Flow(stress, pitch)
