from django.test import TestCase
from covid19_panama.autoupdate_module.tasks import autoupdate
from unittest.mock import patch
from unittest import skip


class CeleryTasksTestCase(TestCase):
    fixtures = [
        'covid19_panama/covid_models/fixtures/data_source_types.json',
        'covid19_panama/covid_models/fixtures/statistical_models.json',
    ]

    @skip('')
    @patch('covid19_panama.autoupdate_module.autoupdate.AutoUpdate.execute')
    @patch('covid19_panama.cleaning.strategy.Cleaner.clean')
    @patch('covid19_panama.covid_models.utils.store_cleaned_data_to_db')
    @patch('covid19_panama.covid_models.utils.store_forecast_data_to_db')
    @patch('covid19_panama.covid_models.utils.obtain_statistical_model_parameters')
    @patch('covid19_panama.covid_models.statistical_models.statistical_model.StatisticalModel.execute')
    def test_autoupdate_calls_all_methods(
        self,
        mock_statistical_model_execute,
        mock_obtain_statistical_model_parameters,
        mock_store_forecast_data_to_db,
        mock_store_clean_data_to_db,
        mock_clean,
        mock_autoupdate_execute
    ):
        autoupdate()

        self.assertTrue(mock_statistical_model_execute.called)
        self.assertTrue(mock_obtain_statistical_model_parameters.called)
        self.assertTrue(mock_store_forecast_data_to_db.called)
        self.assertTrue(mock_store_clean_data_to_db.called)
        self.assertTrue(mock_clean.called)
        self.assertTrue(mock_autoupdate_execute.called)
