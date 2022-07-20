from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CovidModelsConfig(AppConfig):
    name = "covid19_panama.covid_models"
    verbose_name = _("Covid Models")
