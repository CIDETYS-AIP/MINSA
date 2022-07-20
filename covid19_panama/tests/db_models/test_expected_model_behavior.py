from covid19_panama.covid_models.models import (
    DataSourceType, DataSource, ForecastedValue,
    RealValue, StatisticalModel, ForecastDataSource, Forecast,
)
from datetime import datetime, timedelta
from decimal import Decimal
from django.test import TestCase


class ModelsTestCase(TestCase):
    def test_deleting_statistical_model_or_forecast_data_source_deletes_forecast(self):
        statistical_model = StatisticalModel.objects.create(
            name='SIR'
        )

        data_source_type = DataSourceType.objects.create(type='Database')

        data_source = DataSource.objects.create(source_type=data_source_type, source_name='Local Postgres DB')

        forecast_data_source = ForecastDataSource.objects.create(
            access_date=datetime.today(),
            data_source=data_source
        )

        Forecast.objects.create(
            from_date=datetime.today(),
            to_date=datetime.today() + timedelta(days=7),
            forecast_data_source=forecast_data_source,
            statistical_model=statistical_model
        )

        self.assertEqual(Forecast.objects.count(), 1)

        statistical_model.delete()

        self.assertEqual(Forecast.objects.count(), 0)

        statistical_model = StatisticalModel.objects.create(
            name='SIR'
        )

        Forecast.objects.create(
            from_date=datetime.today(),
            to_date=datetime.today() + timedelta(days=7),
            forecast_data_source=forecast_data_source,
            statistical_model=statistical_model
        )

        self.assertEqual(Forecast.objects.count(), 1)

        forecast_data_source.delete()

        self.assertEqual(Forecast.objects.count(), 0)

    def test_delete_forecast_deletes_forecasted_values(self):
        statistical_model = StatisticalModel.objects.create(
            name='SIR'
        )

        data_source_type = DataSourceType.objects.create(type='Database')

        data_source = DataSource.objects.create(source_type=data_source_type, source_name='Local Postgres DB')

        forecast_data_source = ForecastDataSource.objects.create(
            access_date=datetime.today(),
            data_source=data_source
        )

        forecast = Forecast.objects.create(
            from_date=datetime.today(),
            to_date=datetime.today() + timedelta(days=7),
            forecast_data_source=forecast_data_source,
            statistical_model=statistical_model
        )

        for i in range(0, 10):
            ForecastedValue.objects.create(
                label='hello',
                value=Decimal(i),
                forecast=forecast
            )

        self.assertEqual(ForecastedValue.objects.count(), 10)

        forecast.delete()

        self.assertEqual(ForecastedValue.objects.count(), 0)

    def test_delete_data_source_deletes_forecast_data_source_and_real_values(self):
        data_source_type = DataSourceType.objects.create(type='Database')

        data_source = DataSource.objects.create(source_type=data_source_type, source_name='Local Postgres DB')

        ForecastDataSource.objects.create(
            access_date=datetime.today(),
            data_source=data_source
        )

        for i in range(0, 10):
            RealValue.objects.create(
                value=i,
                label='hello',
                data_source=data_source
            )

        self.assertEqual(RealValue.objects.count(), 10)
        self.assertEqual(ForecastDataSource.objects.count(), 1)

        data_source.delete()

        self.assertEqual(ForecastDataSource.objects.count(), 0)
        self.assertEqual(RealValue.objects.count(), 0)

    def test_delete_data_source_type_makes_field_in_data_source_null(self):
        data_source_type = DataSourceType.objects.create(
            type='Database'
        )

        data_source = DataSource.objects.create(
            source_type=data_source_type,
            source_name='Remote Postgres DB'
        )

        self.assertEqual(data_source.source_type, data_source_type)

        data_source_type.delete()

        data_source = DataSource.objects.get(source_name='Remote Postgres DB')

        self.assertEqual(data_source.source_type, None)
