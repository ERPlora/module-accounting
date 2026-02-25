# Accounting Module

Chart of accounts, journal entries, balance and P&L.

## Features

- Hierarchical chart of accounts with parent-child relationships
- Five account types: Asset, Liability, Equity, Income, Expense
- Double-entry journal entries with debit/credit lines
- Journal entry status tracking (draft, posted)
- Balance and P&L reports
- Per-account balance tracking

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Accounting > Settings**

## Usage

Access via: **Menu > Accounting**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/accounting/dashboard/` | Overview of accounting metrics and recent activity |
| Accounts | `/m/accounting/accounts/` | Chart of accounts management |
| Journal | `/m/accounting/journal/` | Journal entries list and creation |
| Reports | `/m/accounting/reports/` | Balance sheet, P&L and other financial reports |
| Settings | `/m/accounting/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `Account` | Chart of accounts entry with code, name, type, parent, and balance |
| `JournalEntry` | Journal entry header with entry number, date, status, and totals |
| `JournalLine` | Individual debit/credit line within a journal entry |

## Permissions

| Permission | Description |
|------------|-------------|
| `accounting.view_account` | View accounts in the chart of accounts |
| `accounting.add_account` | Create new accounts |
| `accounting.change_account` | Edit existing accounts |
| `accounting.view_journalentry` | View journal entries |
| `accounting.add_journalentry` | Create new journal entries |
| `accounting.change_journalentry` | Edit journal entries |
| `accounting.delete_journalentry` | Delete journal entries |
| `accounting.view_reports` | Access financial reports |
| `accounting.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
