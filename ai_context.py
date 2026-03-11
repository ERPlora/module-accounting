"""
AI context for the Accounting module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Accounting

### Models

**Account**
- `code` (CharField, max 20): chart of accounts code, e.g. "400", "700"
- `name` (CharField): account name
- `account_type` (CharField): one of `asset`, `liability`, `equity`, `income`, `expense`
- `parent` (FK self, nullable): parent account for hierarchical chart
- `balance` (Decimal 14,2): current balance (maintained externally)
- `is_active` (bool, default True)

**JournalEntry**
- `entry_number` (CharField, max 50): unique entry identifier
- `date` (DateField): accounting date
- `description` (TextField, optional)
- `status` (CharField, default `draft`): typically `draft` or `posted`
- `total_debit` / `total_credit` (Decimal 14,2): must balance (debit = credit)
- Related: `lines` (JournalLine set)

**JournalLine**
- `entry` (FK JournalEntry): parent entry
- `account` (FK Account): the account being debited/credited
- `description` (CharField, optional)
- `debit` (Decimal 14,2): amount on debit side (0 if credit)
- `credit` (Decimal 14,2): amount on credit side (0 if debit)
- Each line has either debit OR credit set, not both

### Key flows

**Create a journal entry:**
1. Create `JournalEntry` with `date`, `entry_number`, `status='draft'`
2. Add `JournalLine` records — one per account affected
3. Verify total_debit == total_credit before posting
4. Update `status` to `posted` once balanced

**Chart of accounts:**
- Accounts are hierarchical via `parent` FK
- Top-level types: asset, liability, equity, income, expense
- Query active accounts: `Account.objects.filter(is_active=True)`

### Relationships
- JournalEntry → JournalLine (one-to-many, related_name `lines`)
- Account → JournalLine (one-to-many)
- Account → Account (self-referential parent hierarchy)
- No direct FK to sales or invoicing — integration is handled via journal entries created by other modules
"""
