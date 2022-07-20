from django.conf import settings
from django.test import TestCase
from covid19_panama.cleaning.callbacks import SIRCallbacks


class SIRCleaningCallbacksTestCase(TestCase):
    def test_read_csv(self):
        dataframe = SIRCallbacks.read_csv(settings.SIR_COVID_DATA_SOURCE)
        self.assertFalse(dataframe.empty)
        dataframe = SIRCallbacks.read_csv(settings.SIR_RECUPERADOS_DATA_SOURCE)
        self.assertFalse(dataframe.empty)
        dataframe = SIRCallbacks.read_csv(settings.SIR_MOBILIDAD_DATA_SOURCE_2020)
        self.assertFalse(dataframe.empty)

    def test_obtain_recuperados(self):
        dataframe = SIRCallbacks.read_csv(settings.SIR_RECUPERADOS_DATA_SOURCE)
        key, value = SIRCallbacks.obtain_recuperados(dataframe, start=48, end=405)
        self.assertEqual(key, 'recuperados_data')
        self.assertFalse(dataframe.empty)

    def test_obtain_panama_data(self):
        dataframe = SIRCallbacks.read_csv(settings.SIR_COVID_DATA_SOURCE)
        key, value = SIRCallbacks.obtain_panama_data(dataframe, start=0, end=357)
        self.assertEqual(key, 'panama_data')
        self.assertFalse(dataframe.empty)

    def test_obtain_mobilidad_data(self):
        dataframe = SIRCallbacks.read_csv(settings.SIR_MOBILIDAD_DATA_SOURCE_2020)
        key, value = SIRCallbacks.obtain_mobilidad_data(dataframe, start=23, end=380)
        self.assertEqual(key, 'mobilidad_data')
        self.assertFalse(dataframe.empty)

    def test_consolidate_data(self):
        data = {}

        dataframe = SIRCallbacks.read_and_merge_mobility_csvs(
            {
                'csv_locations': [
                    settings.SIR_MOBILIDAD_DATA_SOURCE_2020,
                    settings.SIR_MOBILIDAD_DATA_SOURCE_2021
                ],
                'start_end_locations': [
                    {'start': 23, 'end': 321},
                    {'start': 0, 'end': 59}
                ]
            }
        )

        key, value = SIRCallbacks.obtain_mobilidad_data(dataframe, start=0, end=357)
        data[key] = value

        dataframe = SIRCallbacks.read_csv(settings.SIR_COVID_DATA_SOURCE)
        key, value = SIRCallbacks.obtain_panama_data(dataframe, start=0, end=357)
        data[key] = value

        dataframe = SIRCallbacks.read_csv(settings.SIR_RECUPERADOS_DATA_SOURCE)
        key, value = SIRCallbacks.obtain_recuperados(dataframe, start=48, end=405)
        data[key] = value

        consolidated_data = SIRCallbacks.consolidate_data(data)
        self.assertFalse(consolidated_data.empty)
