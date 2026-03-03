from django.utils.translation import gettext_lazy as _

MODULE_ID = 'accounting'
MODULE_NAME = _('Accounting')
MODULE_VERSION = '1.0.0'
MODULE_ICON = 'calculator-outline'
MODULE_DESCRIPTION = _('Chart of accounts, journal entries, balance and P&L')
MODULE_AUTHOR = 'ERPlora'
MODULE_CATEGORY = 'finance'

MENU = {
    'label': _('Accounting'),
    'icon': 'calculator-outline',
    'order': 45,
}

NAVIGATION = [
    {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Accounts'), 'icon': 'calculator-outline', 'id': 'accounts'},
{'label': _('Journal'), 'icon': 'book-outline', 'id': 'journal'},
{'label': _('Reports'), 'icon': 'bar-chart-outline', 'id': 'reports'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
]

DEPENDENCIES = []

PERMISSIONS = [
    'accounting.view_account',
'accounting.add_account',
'accounting.change_account',
'accounting.view_journalentry',
'accounting.add_journalentry',
'accounting.change_journalentry',
'accounting.delete_journalentry',
'accounting.view_reports',
'accounting.manage_settings',
]

ROLE_PERMISSIONS = {
    "admin": ["*"],
    "manager": [
        "add_account",
        "add_journalentry",
        "change_account",
        "change_journalentry",
        "view_account",
        "view_journalentry",
        "view_reports",
    ],
    "employee": [
        "add_account",
        "view_account",
        "view_journalentry",
    ],
}
