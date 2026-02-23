from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

ACCOUNT_TYPE = [
    ('asset', _('Asset')),
    ('liability', _('Liability')),
    ('equity', _('Equity')),
    ('income', _('Income')),
    ('expense', _('Expense')),
]

class Account(HubBaseModel):
    code = models.CharField(max_length=20, verbose_name=_('Code'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    account_type = models.CharField(max_length=30, choices=ACCOUNT_TYPE, verbose_name=_('Account Type'))
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default='0', verbose_name=_('Balance'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta(HubBaseModel.Meta):
        db_table = 'accounting_account'

    def __str__(self):
        return self.name


class JournalEntry(HubBaseModel):
    entry_number = models.CharField(max_length=50, verbose_name=_('Entry Number'))
    date = models.DateField(verbose_name=_('Date'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    status = models.CharField(max_length=20, default='draft', verbose_name=_('Status'))
    total_debit = models.DecimalField(max_digits=14, decimal_places=2, default='0', verbose_name=_('Total Debit'))
    total_credit = models.DecimalField(max_digits=14, decimal_places=2, default='0', verbose_name=_('Total Credit'))

    class Meta(HubBaseModel.Meta):
        db_table = 'accounting_journalentry'

    def __str__(self):
        return str(self.id)


class JournalLine(HubBaseModel):
    entry = models.ForeignKey('JournalEntry', on_delete=models.CASCADE, related_name='lines')
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, verbose_name=_('Description'))
    debit = models.DecimalField(max_digits=14, decimal_places=2, default='0', verbose_name=_('Debit'))
    credit = models.DecimalField(max_digits=14, decimal_places=2, default='0', verbose_name=_('Credit'))

    class Meta(HubBaseModel.Meta):
        db_table = 'accounting_journalline'

    def __str__(self):
        return str(self.id)

