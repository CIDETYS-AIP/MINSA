from django.urls import path
from covid19_panama.covid_models.views import (
    ARIMAView, SIRView, GenerateForecastView
)

from covid19_panama.covid_models.graphs.views import (
    ARIMAChartView,
    SIRChartDailyCasesView,
    SIRChartDailyDeathsView,
    SIRChartDailyTestsView
)

app_name = "covid_models"

urlpatterns = [
    path("arima", ARIMAView.as_view(), name='arima_model'),
    path("sir", SIRView.as_view(), name='sir_model'),
    path("arimaChart", ARIMAChartView.as_view(), name='arima_chart'),
    path("sirChartDailyCases", SIRChartDailyCasesView.as_view(), name='sir_chart_daily_cases'),
    path('sirChartDailyDeaths', SIRChartDailyDeathsView.as_view(), name='sir_chart_daily_deaths'),
    path('sirChartDailyTests', SIRChartDailyTestsView.as_view(), name='sir_chart_daily_tests'),
    path("generateForecast", GenerateForecastView.as_view(), name='generate_forecast'),
]
