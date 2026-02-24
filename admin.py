from django.contrib import admin

from .models import Account, JournalEntry, JournalLine

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'account_type', 'parent', 'balance', 'created_at']
    search_fields = ['code', 'name', 'account_type']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['entry_number', 'date', 'status', 'total_debit', 'created_at']
    search_fields = ['entry_number', 'description', 'status']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(JournalLine)
class JournalLineAdmin(admin.ModelAdmin):
    list_display = ['entry', 'account', 'description', 'debit', 'credit', 'created_at']
    search_fields = ['description']
    readonly_fields = ['created_at', 'updated_at']

