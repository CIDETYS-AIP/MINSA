from config import celery_app
from covid19_panama.autoupdate_module.autoupdate import AutoUpdate
from covid19_panama.cleaning.strategy import Cleaner
from covid19_panama.cleaning.strategies import CSVStrategy
from covid19_panama.cleaning.callbacks import SIRCallbacks
from covid19_panama.covid_models.statistical_models.strategies.strategy_sir import SIRStrategy # noqa
from covid19_panama.covid_models.statistical_models.statistical_model import StatisticalModel
from covid19_panama.covid_models.utils import store_cleaned_data_to_db
from covid19_panama.covid_models.utils import store_forecast_data_to_db
from covid19_panama.covid_models.utils import obtain_statistical_model_parameters
from covid19_panama.covid_models.models import DataSource
from covid19_panama.covid_models.models import DataSourceType
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@celery_app.task(soft_time_limit=1800)
def autoupdate():
    '''
    30 minutes = 1800 seconds
    '''
    models = [
        {
            'statistical_model_name': 'SIR LSTM',
            'statistical_model_strategy': SIRStrategy(),
            'statistical_model_parameters': [
                'test_data_length',
                'number_of_features'
            ],
            'statistical_model_parameter_callbacks': [
                SIRCallbacks.get_test_length,
                SIRCallbacks.get_number_of_features
            ],
            'forecast_fields_to_store': [
                'Prediccion de nuevos casos',
                'Prediccion de Defunciones diarias',
                'Prediccion de pruebas diarias'
            ],
            'repositories': [
                settings.OWID_REPOSITORY_NAME,
                settings.CSSE_REPOSITORY_NAME,
                settings.MOBILITY_DATA_REPOSITORY_NAME
            ],
            'branches_to_pull': [
                settings.OWID_BRANCH_TO_PULL,
                settings.CSSE_BRANCH_TO_PULL,
                settings.MOBILITY_DATA_BRANCH_TO_PULL
            ],
            'autoupdate_strategy': settings.SIR_AUTOUPDATE_STRATEGY,
            'autoupdate_results': [],
            'cleaning_strategy': CSVStrategy(
                files=[
                    {
                        'csv_locations': [
                            settings.SIR_MOBILIDAD_DATA_SOURCE_2020,
                            settings.SIR_MOBILIDAD_DATA_SOURCE_2021,
                            settings.SIR_MOBILIDAD_DATA_SOURCE_2022
                        ],
                        'start_end_locations': [
                            {'start': 23, 'end': 321},
                            {'start': 0, 'end': 365},
                            {'start': 0, 'end': 135},
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
                    {'start': 0, 'end': 798},
                    {'start': 0, 'end': 798},
                    {'start': 48, 'end': 846},
                ],
                consolidate_data_function=SIRCallbacks.consolidate_data,
            ),
            'clean_data_fields_to_store': [
                'nuevos_casos', 'defunciones_nuevas', 'nuevas_pruebas'
            ],
            'data_source_type': 'CSV',
            'data_source_name': 'Consolidated CSV data for SIR',
        }
    ]

    for model in models:
        logger.info(f'Autoupdate for model: {model}')
        assert len(model['repositories']) == len(model['branches_to_pull'])

        for index, repository in enumerate(model['repositories']):
            autoupdate = AutoUpdate(
                strategy=model['autoupdate_strategy'],
                repository=repository,
                branch_to_pull=model['branches_to_pull'][index]
            )

            executed = autoupdate.execute()

            model['autoupdate_results'].append(executed)

        '''
        If at least one repository was updated
        '''
        if True in model['autoupdate_results']:
            cleaner = Cleaner(
                strategy=model['cleaning_strategy']
            )

            cleaned_data = cleaner.clean()

            logger.info(cleaned_data)

            data_source = DataSource.objects.create(
                source_type=DataSourceType.objects.get(type=model['data_source_type']),
                source_name=model['data_source_name']
            )

            store_cleaned_data_to_db(
                model=model,
                cleaned_data=cleaned_data,
                data_source=data_source
            )

            assert len(model['statistical_model_parameters']) == len(model['statistical_model_parameter_callbacks'])

            parameters = obtain_statistical_model_parameters(model=model, data=cleaned_data)

            statistical_model = StatisticalModel(
                strategy=model['statistical_model_strategy'],
                parameters=parameters,
                data=cleaned_data
            )

            statistical_model.execute()

            store_forecast_data_to_db(
                model=model,
                forecast_dataframe=statistical_model.strategy.forecast,
                data_source=data_source
            )
