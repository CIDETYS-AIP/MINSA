from model_utils.models import TimeStampedModel
from django.db import models


'''
Django creates an id attribute by default.
Inherting from TimeStampedModel gives the model two implicid additional fields: created and modified.
'''


class StatisticalModel(TimeStampedModel):
    name = models.CharField(max_length=255, blank=False, null=False)


class Forecast(TimeStampedModel):
    from_date = models.DateTimeField(blank=True, null=True)
    to_date = models.DateTimeField(blank=True, null=True)
    '''
    If you delete a forecast data source, you will delete the forecast associated with it.
    '''
    forecast_data_source = models.ForeignKey('ForecastDataSource', related_name='forecast', on_delete=models.CASCADE)
    '''
    If you delete a statistical model, you will delete the forecast associated with it.
    '''
    statistical_model = models.ForeignKey('StatisticalModel', related_name='forecasts', on_delete=models.CASCADE)


class ForecastedValue(TimeStampedModel):
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    label = models.CharField(max_length=255, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    '''
    If you delete a forecast, you will also delete associated forecasted value.
    '''
    forecast = models.ForeignKey('Forecast', related_name='forecasted_values', on_delete=models.CASCADE)


class ForecastDataSource(TimeStampedModel):
    access_date = models.DateTimeField()
    '''
    If you delete a data source, you will also delete associated forecast data source.
    '''
    data_source = models.ForeignKey(
        'DataSource',
        related_name='used_as_data_in_following_forecasts',
        on_delete=models.CASCADE
    )


class RealValue(TimeStampedModel):
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    label = models.CharField(max_length=255, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    '''
    If you delete a data source, you will also delete all real values associated with the deleted data source.
    '''
    data_source = models.ForeignKey('DataSource', related_name='real_values', on_delete=models.CASCADE)


class DataSource(TimeStampedModel):
    '''
    If you delete a data source type, the field data_source_type will be set to null.
    '''
    source_type = models.ForeignKey(
        'DataSourceType',
        related_name='data_sources',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    source_name = models.CharField(max_length=255, null=False, blank=False)


class DataSourceType(TimeStampedModel):
    type = models.CharField(max_length=255, null=False, blank=False)
