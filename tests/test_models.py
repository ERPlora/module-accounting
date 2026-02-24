"""Tests for accounting models."""
import pytest
from django.utils import timezone

from accounting.models import Account, JournalEntry


@pytest.mark.django_db
class TestAccount:
    """Account model tests."""

    def test_create(self, account):
        """Test Account creation."""
        assert account.pk is not None
        assert account.is_deleted is False

    def test_str(self, account):
        """Test string representation."""
        assert str(account) is not None
        assert len(str(account)) > 0

    def test_soft_delete(self, account):
        """Test soft delete."""
        pk = account.pk
        account.is_deleted = True
        account.deleted_at = timezone.now()
        account.save()
        assert not Account.objects.filter(pk=pk).exists()
        assert Account.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, account):
        """Test default queryset excludes deleted."""
        account.is_deleted = True
        account.deleted_at = timezone.now()
        account.save()
        assert Account.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, account):
        """Test toggling is_active."""
        original = account.is_active
        account.is_active = not original
        account.save()
        account.refresh_from_db()
        assert account.is_active != original


@pytest.mark.django_db
class TestJournalEntry:
    """JournalEntry model tests."""

    def test_create(self, journal_entry):
        """Test JournalEntry creation."""
        assert journal_entry.pk is not None
        assert journal_entry.is_deleted is False

    def test_soft_delete(self, journal_entry):
        """Test soft delete."""
        pk = journal_entry.pk
        journal_entry.is_deleted = True
        journal_entry.deleted_at = timezone.now()
        journal_entry.save()
        assert not JournalEntry.objects.filter(pk=pk).exists()
        assert JournalEntry.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, journal_entry):
        """Test default queryset excludes deleted."""
        journal_entry.is_deleted = True
        journal_entry.deleted_at = timezone.now()
        journal_entry.save()
        assert JournalEntry.objects.filter(hub_id=hub_id).count() == 0


