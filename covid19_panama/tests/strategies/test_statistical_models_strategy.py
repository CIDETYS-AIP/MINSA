from django.test import TestCase
from covid19_panama.covid_models.statistical_models.statistical_model import StatisticalModel
from covid19_panama.covid_models.statistical_models.strategies.strategy_sir import SIRStrategy
from covid19_panama.exceptions import NoStrategyProvidedException


class StatisticalModelTestCase(TestCase):
    def test_statistical_model_has_correct_strategy(self):
        statistical_model = StatisticalModel(
            strategy=SIRStrategy(),
            parameters={},
            data=None
        )
        self.assertTrue(isinstance(statistical_model.strategy, SIRStrategy))

    def test_unsupported_strategy(self):
        with self.assertRaises(NoStrategyProvidedException):
            StatisticalModel(strategy=None)

    def test_execute_raises_exception(self):
        with self.assertRaises(NoStrategyProvidedException):
            StatisticalModel()
