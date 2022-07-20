from covid19_panama.exceptions import NoStrategyProvidedException


class Cleaner:
    strategy = None

    def __init__(self, strategy=None):
        if strategy is None:
            raise NoStrategyProvidedException
        else:
            self.strategy = strategy

    def clean(self):
        return self.strategy.clean()
