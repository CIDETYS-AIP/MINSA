from django.conf import settings
from django.test import TestCase
from covid19_panama.cleaning.strategies import CSVStrategy
from covid19_panama.cleaning.callbacks import SIRCallbacks
from covid19_panama.covid_models.models import DataSource
from covid19_panama.covid_models.models import RealValue
from covid19_panama.covid_models.models import DataSourceType
from decimal import Decimal


class CSVStrategyTestCase(TestCase):
    def test_clean(self):
        csv_strategy = CSVStrategy(
            files=[
                {
                    'csv_locations': [
                        settings.SIR_MOBILIDAD_DATA_SOURCE_2020,
                        settings.SIR_MOBILIDAD_DATA_SOURCE_2021
                    ],
                    'start_end_locations': [
                        {'start': 23, 'end': 321},
                        {'start': 0, 'end': 59}
                    ]
                },
                settings.SIR_COVID_DATA_SOURCE,
                settings.SIR_RECUPERADOS_DATA_SOURCE
            ],
            callbacks=[
                SIRCallbacks.obtain_mobilidad_data,
                SIRCallbacks.obtain_panama_data,
                SIRCallbacks.obtain_recuperados
            ],
            read_file_functions=[
                SIRCallbacks.read_and_merge_mobility_csvs,
                SIRCallbacks.read_csv,
                SIRCallbacks.read_csv,
            ],
            dataframe_start_end=[
                {'start': 0, 'end': 357},
                {'start': 0, 'end': 357},
                {'start': 48, 'end': 405},
            ],
            consolidate_data_function=SIRCallbacks.consolidate_data,
        )

        cleaned_data = csv_strategy.clean()
        self.assertEqual(len(cleaned_data.index), 357)
