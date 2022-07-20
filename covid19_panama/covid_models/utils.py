from typing import Dict, Any
from pandas import DataFrame
from decimal import Decimal
from datetime import datetime
from covid19_panama.covid_models.models import DataSource
from covid19_panama.covid_models.models import RealValue
from covid19_panama.covid_models.models import ForecastDataSource
from covid19_panama.covid_models.models import Forecast
from covid19_panama.covid_models.models import ForecastedValue
from covid19_panama.covid_models.models import StatisticalModel


def store_cleaned_data_to_db(
    model: Dict[str, Any],
    cleaned_data: 'DataFrame',
    data_source: 'DataSource'
):
    for field_to_store in model['clean_data_fields_to_store']:
        field_data = cleaned_data.loc[:, field_to_store]

        for date, data in field_data.items():
            RealValue.objects.create(
                value=Decimal(data),
                label=date.to_pydatetime(),
                name=field_to_store,
                data_source=data_source
            )


def store_forecast_data_to_db(
    model: Dict[str, Any],
    forecast_dataframe: 'DataFrame',
    data_source: 'DataSource'
):
    statistical_model = StatisticalModel.objects.get(
        name=model['statistical_model_name']
    )

    forecast_data_source = ForecastDataSource.objects.create(
        access_date=datetime.now(),
        data_source=data_source
    )

    forecast = Forecast.objects.create(
        forecast_data_source=forecast_data_source,
        statistical_model=statistical_model
    )

    for field_to_store in model['forecast_fields_to_store']:
        field_data = forecast_dataframe.loc[:, field_to_store]

        for date, data in field_data.items():
            ForecastedValue.objects.create(
                value=Decimal(data),
                label=date.to_pydatetime(),
                name=field_to_store,
                forecast=forecast
            )


def obtain_statistical_model_parameters(model: Dict[str, Any], data: 'DataFrame'):
    parameters = {}

    for index, parameter in enumerate(model['statistical_model_parameters']):
        parameters[parameter] = model['statistical_model_parameter_callbacks'][index](data)

    return parameters
