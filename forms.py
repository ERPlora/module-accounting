from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Account, JournalEntry

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['code', 'name', 'account_type', 'parent', 'balance', 'is_active']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'account_type': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'parent': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'balance': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['entry_number', 'date', 'description', 'status', 'total_debit', 'total_credit']
        widgets = {
            'entry_number': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'date': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'status': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'total_debit': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'total_credit': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
        }

