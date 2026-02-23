"""
Accounting Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('accounting', 'dashboard')
@htmx_view('accounting/pages/dashboard.html', 'accounting/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('accounting', 'accounts')
@htmx_view('accounting/pages/accounts.html', 'accounting/partials/accounts_content.html')
def accounts(request):
    """Accounts view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('accounting', 'journal')
@htmx_view('accounting/pages/journal.html', 'accounting/partials/journal_content.html')
def journal(request):
    """Journal view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('accounting', 'reports')
@htmx_view('accounting/pages/reports.html', 'accounting/partials/reports_content.html')
def reports(request):
    """Reports view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('accounting', 'settings')
@htmx_view('accounting/pages/settings.html', 'accounting/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

