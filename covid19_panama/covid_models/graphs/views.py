from chartjs.views.lines import BaseLineChartView
from covid19_panama.covid_models.models import Forecast
from covid19_panama.covid_models.models import StatisticalModel


class ARIMAChartView(BaseLineChartView):
    real_values = []
    predicted_values = []
    dates = []

    def get_labels(self):
        labels = []

        return labels

    def get_providers(self):
        return ["Pronóstico", "Casos verdaderos"]

    def get_data(self):
        return [
            [],
            [],
        ]


class SIRChartDailyCasesView(BaseLineChartView):
    def get_labels(self):
        labels = []

        forecast = Forecast.objects.filter(
            statistical_model=StatisticalModel.objects.get(name='SIR LSTM')
        )

        if forecast.exists():
            forecast = forecast.latest('created')

            forecast_dates = (
                [
                    forecast_value.label for forecast_value
                    in forecast.forecasted_values.filter(name='Prediccion de nuevos casos')
                ]
            )

            real_value_dates = (
                [
                    real_value.label for real_value
                    in forecast.forecast_data_source.data_source.real_values.filter(name='nuevos_casos')
                ]
            )

            labels = [*real_value_dates, *forecast_dates]

        return labels

    def get_providers(self):
        return ["Pronóstico de nuevos casos", "Casos reportados"]

    def get_data(self):
        data = []
        real_values = []
        forecasted_values = []

        forecast = Forecast.objects.filter(
            statistical_model=StatisticalModel.objects.get(name='SIR LSTM')
        )

        if forecast.exists():
            forecast = forecast.latest('created')
            real_values = (
                [
                    real_value.value for real_value
                    in forecast.forecast_data_source.data_source.real_values.filter(name='nuevos_casos')
                ]
            )
            forecasted_values = (
                [
                    forecasted_value.value for forecasted_value
                    in forecast.forecasted_values.filter(name='Prediccion de nuevos casos')
                ]
            )

            forecasted_values = ([None] * len(real_values)) + forecasted_values

            data = [forecasted_values, real_values]

        return data


class SIRChartDailyDeathsView(BaseLineChartView):
    def get_labels(self):
        labels = []

        forecast = Forecast.objects.filter(
            statistical_model=StatisticalModel.objects.get(name='SIR LSTM')
        )

        if forecast.exists():
            forecast = forecast.latest('created')

            forecast_dates = (
                [
                    forecast_value.label for forecast_value
                    in forecast.forecasted_values.filter(name='Prediccion de Defunciones diarias')
                ]
            )

            real_value_dates = (
                [
                    real_value.label for real_value
                    in forecast.forecast_data_source.data_source.real_values.filter(name='defunciones_nuevas')
                ]
            )

            labels = [*real_value_dates, *forecast_dates]

        return labels

    def get_providers(self):
        return ["Pronóstico de nuevas defunciones", "Defunciones reportadas"]

    def get_data(self):
        data = []
        real_values = []
        forecasted_values = []

        forecast = Forecast.objects.filter(
            statistical_model=StatisticalModel.objects.get(name='SIR LSTM')
        )

        if forecast.exists():
            forecast = forecast.latest('created')
            real_values = (
                [
                    real_value.value for real_value
                    in forecast.forecast_data_source.data_source.real_values.filter(name='defunciones_nuevas')
                ]
            )
            forecasted_values = (
                [
                    forecasted_value.value for forecasted_value
                    in forecast.forecasted_values.filter(name='Prediccion de Defunciones diarias')
                ]
            )

            forecasted_values = ([None] * len(real_values)) + forecasted_values

            data = [forecasted_values, real_values]

        return data


class SIRChartDailyTestsView(BaseLineChartView):
    def get_labels(self):
        labels = []

        forecast = Forecast.objects.filter(
            statistical_model=StatisticalModel.objects.get(name='SIR LSTM')
        )

        if forecast.exists():
            forecast = forecast.latest('created')

            forecast_dates = (
                [
                    forecast_value.label for forecast_value
                    in forecast.forecasted_values.filter(name='Prediccion de pruebas diarias')
                ]
            )

            real_value_dates = (
                [
                    real_value.label for real_value
                    in forecast.forecast_data_source.data_source.real_values.filter(name='nuevas_pruebas')
                ]
            )

            labels = [*real_value_dates, *forecast_dates]

        return labels

    def get_providers(self):
        return ["Pronóstico de nuevas pruebas", "Nuevas pruebas reportadas"]

    def get_data(self):
        data = []
        real_values = []
        forecasted_values = []

        forecast = Forecast.objects.filter(
            statistical_model=StatisticalModel.objects.get(name='SIR LSTM')
        )

        if forecast.exists():
            forecast = forecast.latest('created')
            real_values = (
                [
                    real_value.value for real_value
                    in forecast.forecast_data_source.data_source.real_values.filter(name='nuevas_pruebas')
                ]
            )
            forecasted_values = (
                [
                    forecasted_value.value for forecasted_value
                    in forecast.forecasted_values.filter(name='Prediccion de pruebas diarias')
                ]
            )

            forecasted_values = ([None] * len(real_values)) + forecasted_values

            data = [forecasted_values, real_values]

        return data
