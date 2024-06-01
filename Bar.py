class Bar:
    def __init__(self, liquor_lineup: list[str] = None, mixer_lineup: list[str] = None):
        if liquor_lineup is None:
            self.liquors = ['', '', '', '', '', '']
        else:
            self.liquors = liquor_lineup.copy()

        if mixer_lineup is None:
            self.mixers = ['', '', '', '']
        else:
            self.mixers = mixer_lineup.copy()

    def get_liquor(self, idx):
        return self.liquors[idx]

    def set_liquor(self, idx, name):
        self.liquors[idx] = name

    def get_mixer(self, idx):
        return self.mixers[idx]

    def set_mixer(self, idx, name):
        self.mixers[idx] = name

