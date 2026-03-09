# Accounting

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `accounting` |
| **Version** | `1.0.0` |
| **Icon** | `calculator-outline` |
| **Dependencies** | None |

## Models

### `Account`

Account(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, code, name, account_type, parent, balance, is_active)

| Field | Type | Details |
|-------|------|---------|
| `code` | CharField | max_length=20 |
| `name` | CharField | max_length=255 |
| `account_type` | CharField | max_length=30, choices: asset, liability, equity, income, expense |
| `parent` | ForeignKey | → `accounting.Account`, on_delete=SET_NULL, optional |
| `balance` | DecimalField |  |
| `is_active` | BooleanField |  |

### `JournalEntry`

JournalEntry(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, entry_number, date, description, status, total_debit, total_credit)

| Field | Type | Details |
|-------|------|---------|
| `entry_number` | CharField | max_length=50 |
| `date` | DateField |  |
| `description` | TextField | optional |
| `status` | CharField | max_length=20 |
| `total_debit` | DecimalField |  |
| `total_credit` | DecimalField |  |

### `JournalLine`

JournalLine(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, entry, account, description, debit, credit)

| Field | Type | Details |
|-------|------|---------|
| `entry` | ForeignKey | → `accounting.JournalEntry`, on_delete=CASCADE |
| `account` | ForeignKey | → `accounting.Account`, on_delete=CASCADE |
| `description` | CharField | max_length=255, optional |
| `debit` | DecimalField |  |
| `credit` | DecimalField |  |

## Cross-Module Relationships

| From | Field | To | on_delete | Nullable |
|------|-------|----|-----------|----------|
| `Account` | `parent` | `accounting.Account` | SET_NULL | Yes |
| `JournalLine` | `entry` | `accounting.JournalEntry` | CASCADE | No |
| `JournalLine` | `account` | `accounting.Account` | CASCADE | No |

## URL Endpoints

Base path: `/m/accounting/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `journal/` | `journal` | GET |
| `reports/` | `reports` | GET |
| `accounts/` | `accounts_list` | GET |
| `accounts/add/` | `account_add` | GET/POST |
| `accounts/<uuid:pk>/edit/` | `account_edit` | GET |
| `accounts/<uuid:pk>/delete/` | `account_delete` | GET/POST |
| `accounts/<uuid:pk>/toggle/` | `account_toggle_status` | GET |
| `accounts/bulk/` | `accounts_bulk_action` | GET/POST |
| `journal_entries/` | `journal_entries_list` | GET |
| `journal_entries/add/` | `journal_entry_add` | GET/POST |
| `journal_entries/<uuid:pk>/edit/` | `journal_entry_edit` | GET |
| `journal_entries/<uuid:pk>/delete/` | `journal_entry_delete` | GET/POST |
| `journal_entries/bulk/` | `journal_entries_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `accounting.view_account` | View Account |
| `accounting.add_account` | Add Account |
| `accounting.change_account` | Change Account |
| `accounting.view_journalentry` | View Journalentry |
| `accounting.add_journalentry` | Add Journalentry |
| `accounting.change_journalentry` | Change Journalentry |
| `accounting.delete_journalentry` | Delete Journalentry |
| `accounting.view_reports` | View Reports |
| `accounting.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_account`, `add_journalentry`, `change_account`, `change_journalentry`, `view_account`, `view_journalentry`, `view_reports`
- **employee**: `add_account`, `view_account`, `view_journalentry`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Accounts | `calculator-outline` | `accounts` | No |
| Journal | `book-outline` | `journal` | No |
| Reports | `bar-chart-outline` | `reports` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_accounts`

List chart of accounts. Returns code, name, type, balance.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `account_type` | string | No | Filter: asset, liability, equity, income, expense |
| `is_active` | boolean | No | Filter by active status |

### `create_account`

Create a new account in the chart of accounts.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `code` | string | Yes | Account code (e.g., '4000') |
| `name` | string | Yes | Account name |
| `account_type` | string | Yes | Type: asset, liability, equity, income, expense |
| `parent_id` | string | No | Parent account ID |

### `list_journal_entries`

List journal entries with optional date/status filter.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | Filter by status |
| `date_from` | string | No | Start date (YYYY-MM-DD) |
| `date_to` | string | No | End date (YYYY-MM-DD) |
| `limit` | integer | No | Max results (default 20) |

### `create_journal_entry`

Create a journal entry with debit/credit lines (must balance).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `date` | string | Yes | Entry date (YYYY-MM-DD) |
| `description` | string | Yes | Entry description |
| `lines` | array | Yes |  |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  accounting/
    css/
    js/
  icons/
    icon.svg
templates/
  accounting/
    pages/
      account_add.html
      account_edit.html
      accounts.html
      dashboard.html
      index.html
      journal.html
      journal_entries.html
      journal_entry_add.html
      journal_entry_edit.html
      journal_entrys.html
      reports.html
      settings.html
    partials/
      account_add_content.html
      account_edit_content.html
      accounts_content.html
      accounts_list.html
      dashboard_content.html
      journal_content.html
      journal_entries_content.html
      journal_entries_list.html
      journal_entry_add_content.html
      journal_entry_edit_content.html
      journal_entrys_content.html
      journal_entrys_list.html
      panel_account_add.html
      panel_account_edit.html
      panel_journal_entry_add.html
      panel_journal_entry_edit.html
      reports_content.html
      settings_content.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
