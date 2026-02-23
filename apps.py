from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounting'
    label = 'accounting'
    verbose_name = _('Accounting')

    def ready(self):
        pass
