"""
Accounting Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import Account, JournalEntry, JournalLine

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('accounting', 'dashboard')
@htmx_view('accounting/pages/index.html', 'accounting/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_accounts': Account.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_journal_entries': JournalEntry.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# Account
# ======================================================================

ACCOUNT_SORT_FIELDS = {
    'name': 'name',
    'code': 'code',
    'account_type': 'account_type',
    'parent': 'parent',
    'is_active': 'is_active',
    'balance': 'balance',
    'created_at': 'created_at',
}

def _build_accounts_context(hub_id, per_page=10):
    qs = Account.objects.filter(hub_id=hub_id, is_deleted=False).order_by('name')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'accounts': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'name',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_accounts_list(request, hub_id, per_page=10):
    ctx = _build_accounts_context(hub_id, per_page)
    return django_render(request, 'accounting/partials/accounts_list.html', ctx)

@login_required
@with_module_nav('accounting', 'accounts')
@htmx_view('accounting/pages/accounts.html', 'accounting/partials/accounts_content.html')
def accounts_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = Account.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(code__icontains=search_query) | Q(name__icontains=search_query) | Q(account_type__icontains=search_query))

    order_by = ACCOUNT_SORT_FIELDS.get(sort_field, 'name')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['name', 'code', 'account_type', 'parent', 'is_active', 'balance']
        headers = ['Name', 'Code', 'Account Type', 'self', 'Is Active', 'Balance']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='accounts.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='accounts.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'accounting/partials/accounts_list.html', {
            'accounts': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'accounts': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def account_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        name = request.POST.get('name', '').strip()
        account_type = request.POST.get('account_type', '').strip()
        balance = request.POST.get('balance', '0') or '0'
        is_active = request.POST.get('is_active') == 'on'
        obj = Account(hub_id=hub_id)
        obj.code = code
        obj.name = name
        obj.account_type = account_type
        obj.balance = balance
        obj.is_active = is_active
        obj.save()
        return _render_accounts_list(request, hub_id)
    return django_render(request, 'accounting/partials/panel_account_add.html', {})

@login_required
def account_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Account, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.code = request.POST.get('code', '').strip()
        obj.name = request.POST.get('name', '').strip()
        obj.account_type = request.POST.get('account_type', '').strip()
        obj.balance = request.POST.get('balance', '0') or '0'
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.save()
        return _render_accounts_list(request, hub_id)
    return django_render(request, 'accounting/partials/panel_account_edit.html', {'obj': obj})

@login_required
@require_POST
def account_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Account, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_accounts_list(request, hub_id)

@login_required
@require_POST
def account_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Account, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_accounts_list(request, hub_id)

@login_required
@require_POST
def accounts_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = Account.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_accounts_list(request, hub_id)


# ======================================================================
# JournalEntry
# ======================================================================

JOURNAL_ENTRY_SORT_FIELDS = {
    'entry_number': 'entry_number',
    'status': 'status',
    'total_credit': 'total_credit',
    'total_debit': 'total_debit',
    'date': 'date',
    'description': 'description',
    'created_at': 'created_at',
}

def _build_journal_entries_context(hub_id, per_page=10):
    qs = JournalEntry.objects.filter(hub_id=hub_id, is_deleted=False).order_by('entry_number')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'journal_entries': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'entry_number',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_journal_entries_list(request, hub_id, per_page=10):
    ctx = _build_journal_entries_context(hub_id, per_page)
    return django_render(request, 'accounting/partials/journal_entries_list.html', ctx)

@login_required
@with_module_nav('accounting', 'journal')
@htmx_view('accounting/pages/journal_entries.html', 'accounting/partials/journal_entries_content.html')
def journal_entries_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'entry_number')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = JournalEntry.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(entry_number__icontains=search_query) | Q(description__icontains=search_query) | Q(status__icontains=search_query))

    order_by = JOURNAL_ENTRY_SORT_FIELDS.get(sort_field, 'entry_number')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['entry_number', 'status', 'total_credit', 'total_debit', 'date', 'description']
        headers = ['Entry Number', 'Status', 'Total Credit', 'Total Debit', 'Date', 'Description']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='journal_entries.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='journal_entries.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'accounting/partials/journal_entries_list.html', {
            'journal_entries': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'journal_entries': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def journal_entry_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        entry_number = request.POST.get('entry_number', '').strip()
        date = request.POST.get('date') or None
        description = request.POST.get('description', '').strip()
        status = request.POST.get('status', '').strip()
        total_debit = request.POST.get('total_debit', '0') or '0'
        total_credit = request.POST.get('total_credit', '0') or '0'
        obj = JournalEntry(hub_id=hub_id)
        obj.entry_number = entry_number
        obj.date = date
        obj.description = description
        obj.status = status
        obj.total_debit = total_debit
        obj.total_credit = total_credit
        obj.save()
        return _render_journal_entries_list(request, hub_id)
    return django_render(request, 'accounting/partials/panel_journal_entry_add.html', {})

@login_required
def journal_entry_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(JournalEntry, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.entry_number = request.POST.get('entry_number', '').strip()
        obj.date = request.POST.get('date') or None
        obj.description = request.POST.get('description', '').strip()
        obj.status = request.POST.get('status', '').strip()
        obj.total_debit = request.POST.get('total_debit', '0') or '0'
        obj.total_credit = request.POST.get('total_credit', '0') or '0'
        obj.save()
        return _render_journal_entries_list(request, hub_id)
    return django_render(request, 'accounting/partials/panel_journal_entry_edit.html', {'obj': obj})

@login_required
@require_POST
def journal_entry_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(JournalEntry, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_journal_entries_list(request, hub_id)

@login_required
@require_POST
def journal_entries_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = JournalEntry.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_journal_entries_list(request, hub_id)


@login_required
@permission_required('accounting.manage_settings')
@with_module_nav('accounting', 'settings')
@htmx_view('accounting/pages/settings.html', 'accounting/partials/settings_content.html')
def settings_view(request):
    return {}

