from django import forms


class GenerateForecastForm(forms.Form):
    FORECAST_MODELS = (
        ('arima', 'ARIMA'),
        ('sir', 'SIR')
    )

    file = forms.FileField(label='Archivo csv o excel (opcional)', required=False)
    forecast = forms.ChoiceField(label='Modelo estadístico', required=True, choices=FORECAST_MODELS)
