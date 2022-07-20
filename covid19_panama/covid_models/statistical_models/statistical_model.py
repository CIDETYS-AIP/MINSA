from covid19_panama.exceptions import NoStrategyProvidedException


class StatisticalModel:
    strategy = None
    parameters = {}
    data = None

    def __init__(self, strategy=None, parameters={}, data=None, *args, **kwargs):
        if strategy is None:
            raise NoStrategyProvidedException
        else:
            self.strategy = strategy
            self.strategy.parameters = parameters
            self.strategy.data = data

    def execute(self):
        if self.strategy:
            self.strategy.compute_model()
            self.strategy.generate_forecast()
        else:
            raise NoStrategyProvidedException
