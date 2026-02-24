"""Tests for accounting views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('accounting:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('accounting:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('accounting:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestAccountViews:
    """Account view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('accounting:accounts_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('accounting:accounts_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('accounting:accounts_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('accounting:accounts_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('accounting:accounts_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('accounting:accounts_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('accounting:account_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('accounting:account_add')
        data = {
            'code': 'New Code',
            'name': 'New Name',
            'account_type': 'New Account Type',
            'balance': '100.00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, account):
        """Test edit form loads."""
        url = reverse('accounting:account_edit', args=[account.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, account):
        """Test editing via POST."""
        url = reverse('accounting:account_edit', args=[account.pk])
        data = {
            'code': 'Updated Code',
            'name': 'Updated Name',
            'account_type': 'Updated Account Type',
            'balance': '100.00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, account):
        """Test soft delete via POST."""
        url = reverse('accounting:account_delete', args=[account.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        account.refresh_from_db()
        assert account.is_deleted is True

    def test_toggle_status(self, auth_client, account):
        """Test toggle active status."""
        url = reverse('accounting:account_toggle_status', args=[account.pk])
        original = account.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        account.refresh_from_db()
        assert account.is_active != original

    def test_bulk_delete(self, auth_client, account):
        """Test bulk delete."""
        url = reverse('accounting:accounts_bulk_action')
        response = auth_client.post(url, {'ids': str(account.pk), 'action': 'delete'})
        assert response.status_code == 200
        account.refresh_from_db()
        assert account.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('accounting:accounts_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestJournalEntryViews:
    """JournalEntry view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('accounting:journal_entries_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('accounting:journal_entries_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('accounting:journal_entries_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('accounting:journal_entries_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('accounting:journal_entries_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('accounting:journal_entries_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('accounting:journal_entry_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('accounting:journal_entry_add')
        data = {
            'entry_number': 'New Entry Number',
            'date': '2025-01-15',
            'description': 'Test description',
            'status': 'New Status',
            'total_debit': '100.00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, journal_entry):
        """Test edit form loads."""
        url = reverse('accounting:journal_entry_edit', args=[journal_entry.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, journal_entry):
        """Test editing via POST."""
        url = reverse('accounting:journal_entry_edit', args=[journal_entry.pk])
        data = {
            'entry_number': 'Updated Entry Number',
            'date': '2025-01-15',
            'description': 'Test description',
            'status': 'Updated Status',
            'total_debit': '100.00',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, journal_entry):
        """Test soft delete via POST."""
        url = reverse('accounting:journal_entry_delete', args=[journal_entry.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        journal_entry.refresh_from_db()
        assert journal_entry.is_deleted is True

    def test_bulk_delete(self, auth_client, journal_entry):
        """Test bulk delete."""
        url = reverse('accounting:journal_entries_bulk_action')
        response = auth_client.post(url, {'ids': str(journal_entry.pk), 'action': 'delete'})
        assert response.status_code == 200
        journal_entry.refresh_from_db()
        assert journal_entry.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('accounting:journal_entries_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('accounting:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('accounting:settings')
        response = client.get(url)
        assert response.status_code == 302

