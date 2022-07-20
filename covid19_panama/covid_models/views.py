from django.views.generic import View
from django.shortcuts import render
from .forms import GenerateForecastForm
from datetime import datetime
from covid19_panama.covid_models.models import Forecast
from covid19_panama.covid_models.models import StatisticalModel


class HomeView(View):
    template_name = 'pages/home.html'

    def get(self, request, *args, **kwargs):
        params = {
            'last_forecast_date': 'N/A'
        }

        forecast = Forecast.objects.filter(
            statistical_model=StatisticalModel.objects.get(name='SIR LSTM')
        )

        if forecast.exists():
            forecast = forecast.latest('created')
            params['last_forecast_date'] = forecast.created

        return render(request, self.template_name, params)

    def post(self, request, format=None):
        return render(request, self.template_name)


class ARIMAView(View):
    template_name = 'covid_models/model_arima.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, format=None):
        return render(request, self.template_name)


class SIRView(View):
    template_name = 'covid_models/model_sir.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, format=None):
        return render(request, self.template_name)


class GenerateForecastView(View):
    template_name = 'covid_models/generate_forecasts.html'

    def get(self, request, *args, **kwargs):
        form = GenerateForecastForm()

        return render(
            request,
            self.template_name,
            {
                'generate_forecast_form': form,
                'last_forecast': {
                    'date': datetime.now(),
                    'type': 'ARIMA',
                    'data_source_type': 'User-provided file',
                }
            }
        )

    def post(self, request, format=None):
        form = GenerateForecastForm(request.POST, request.FILES)
        if form.is_valid():
            return render(request, self.template_name)
        else:
            form = GenerateForecastForm()
        return render(
            request,
            self.template_name,
            {
                'generate_forecast_form': form
            }
        )
