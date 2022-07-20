from pandas import DataFrame
from pandas import read_csv
from pandas import to_numeric
from pandas import to_datetime
from pandas import concat
from typing import Tuple, Any, Dict
from math import ceil


class SIRCallbacks:
    @staticmethod
    def read_csv(csv_location: str) -> 'DataFrame':
        '''
        squeeze: If the parsed data only contains one column then return a Series.
        '''
        dataframe: 'DataFrame' = read_csv(csv_location, parse_dates=True).squeeze('columns')
        return dataframe

    @staticmethod
    def read_and_merge_mobility_csvs(parameters: Dict[str, Any]) -> 'DataFrame':
        dataframes = []
        for index, csv in enumerate(parameters['csv_locations']):
            dataframe = SIRCallbacks.read_csv(csv)
            dataframe = dataframe[
                parameters['start_end_locations'][index]['start']:
                parameters['start_end_locations'][index]['end']
            ]
            dataframes.append(dataframe)
        dataframe = concat(dataframes, axis=0)

        return dataframe

    @staticmethod
    def obtain_recuperados(dataframe: 'DataFrame', start: int, end: int) -> Tuple[str, 'DataFrame']:
        recuperados = dataframe.loc[dataframe['Country/Region'] == 'Panama']
        recuperados = recuperados.drop(['Province/State', 'Lat', 'Long'], axis=1)
        recuperados = recuperados.T
        recuperados.columns = ['recuperados']
        recuperados = recuperados[start:end]
        recuperados = recuperados.apply(to_numeric)
        recuperados.index = to_datetime(recuperados.index)
        return 'recuperados_data', recuperados

    @staticmethod
    def obtain_panama_data(dataframe: 'DataFrame', start: int, end: int) -> Tuple[str, 'DataFrame']:
        panama_data = dataframe.loc[dataframe['location'] == 'Panama']
        panama_data = panama_data.fillna(0)
        panama_data.index = to_datetime(panama_data.date)
        panama_data = panama_data[start:end]
        complete_panama_data = panama_data.set_index('date')
        complete_panama_data = panama_data[['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'new_tests']]
        complete_panama_data.columns = [
            'casos_totales', 'nuevos_casos', 'defunciones_totales', 'defunciones_nuevas', 'nuevas_pruebas'
        ]
        complete_panama_data = complete_panama_data.asfreq(freq='1D')
        return 'panama_data', complete_panama_data

    @staticmethod
    def obtain_mobilidad_data(dataframe: 'DataFrame', start: int, end: int) -> Tuple[str, 'DataFrame']:
        dataframe.index = to_datetime(dataframe.date)
        dataframe = dataframe[
            [
                'retail_and_recreation_percent_change_from_baseline',
                'grocery_and_pharmacy_percent_change_from_baseline',
                'parks_percent_change_from_baseline',
                'transit_stations_percent_change_from_baseline',
                'workplaces_percent_change_from_baseline',
                'residential_percent_change_from_baseline'
            ]
        ]
        dataframe = dataframe[start:end]

        return 'mobilidad_data', dataframe

    @staticmethod
    def consolidate_data(data: Dict[str, Any]) -> 'DataFrame':
        '''
        Concat only works if the dataframes are the same length.
        The mobility data file only includes data from 2020.
        Either add the data for 2021 or just use merge
        '''
        consolidated_data = concat(
            [data['panama_data'], data['recuperados_data']],
            axis=1
        )

        consolidated_data = concat(
            [consolidated_data, data['mobilidad_data']],
            axis=1,
        )

        return consolidated_data

    @staticmethod
    def get_test_length(data: 'DataFrame') -> int:
        return ceil(0.1*len(data.index))

    @staticmethod
    def get_number_of_features(data: 'DataFrame') -> int:
        return len(data.columns)
