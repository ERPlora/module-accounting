"""AI tools for the Accounting module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListAccounts(AssistantTool):
    name = "list_accounts"
    description = "List chart of accounts. Returns code, name, type, balance."
    module_id = "accounting"
    required_permission = "accounting.view_account"
    parameters = {
        "type": "object",
        "properties": {
            "account_type": {"type": "string", "description": "Filter: asset, liability, equity, income, expense"},
            "is_active": {"type": "boolean", "description": "Filter by active status"},
        },
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from accounting.models import Account
        qs = Account.objects.all()
        if args.get('account_type'):
            qs = qs.filter(account_type=args['account_type'])
        if 'is_active' in args:
            qs = qs.filter(is_active=args['is_active'])
        return {
            "accounts": [
                {"id": str(a.id), "code": a.code, "name": a.name, "account_type": a.account_type, "balance": str(a.balance), "is_active": a.is_active}
                for a in qs.order_by('code')
            ]
        }


@register_tool
class CreateAccount(AssistantTool):
    name = "create_account"
    description = "Create a new account in the chart of accounts."
    module_id = "accounting"
    required_permission = "accounting.add_account"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "code": {"type": "string", "description": "Account code (e.g., '4000')"},
            "name": {"type": "string", "description": "Account name"},
            "account_type": {"type": "string", "description": "Type: asset, liability, equity, income, expense"},
            "parent_id": {"type": "string", "description": "Parent account ID"},
        },
        "required": ["code", "name", "account_type"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from accounting.models import Account
        a = Account.objects.create(
            code=args['code'], name=args['name'], account_type=args['account_type'],
            parent_id=args.get('parent_id'),
        )
        return {"id": str(a.id), "code": a.code, "name": a.name, "created": True}


@register_tool
class ListJournalEntries(AssistantTool):
    name = "list_journal_entries"
    description = "List journal entries with optional date/status filter."
    module_id = "accounting"
    required_permission = "accounting.view_journalentry"
    parameters = {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Filter by status"},
            "date_from": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
            "date_to": {"type": "string", "description": "End date (YYYY-MM-DD)"},
            "limit": {"type": "integer", "description": "Max results (default 20)"},
        },
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from accounting.models import JournalEntry
        qs = JournalEntry.objects.all()
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        if args.get('date_from'):
            qs = qs.filter(date__gte=args['date_from'])
        if args.get('date_to'):
            qs = qs.filter(date__lte=args['date_to'])
        limit = args.get('limit', 20)
        return {
            "entries": [
                {"id": str(e.id), "entry_number": e.entry_number, "date": str(e.date), "description": e.description, "status": e.status, "total_debit": str(e.total_debit), "total_credit": str(e.total_credit)}
                for e in qs.order_by('-date')[:limit]
            ],
            "total": qs.count(),
        }


@register_tool
class CreateJournalEntry(AssistantTool):
    name = "create_journal_entry"
    description = "Create a journal entry with debit/credit lines (must balance)."
    module_id = "accounting"
    required_permission = "accounting.add_journalentry"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "date": {"type": "string", "description": "Entry date (YYYY-MM-DD)"},
            "description": {"type": "string", "description": "Entry description"},
            "lines": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "account_id": {"type": "string"},
                        "description": {"type": "string"},
                        "debit": {"type": "string", "description": "Debit amount"},
                        "credit": {"type": "string", "description": "Credit amount"},
                    },
                    "required": ["account_id"],
                },
            },
        },
        "required": ["date", "description", "lines"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from decimal import Decimal
        from accounting.models import JournalEntry, JournalLine
        total_debit = sum(Decimal(l.get('debit', '0')) for l in args['lines'])
        total_credit = sum(Decimal(l.get('credit', '0')) for l in args['lines'])
        if total_debit != total_credit:
            return {"error": f"Entry does not balance: debit={total_debit}, credit={total_credit}"}
        entry = JournalEntry.objects.create(
            date=args['date'], description=args['description'],
            total_debit=total_debit, total_credit=total_credit,
        )
        for line in args['lines']:
            JournalLine.objects.create(
                journal_entry=entry, account_id=line['account_id'],
                description=line.get('description', ''),
                debit=Decimal(line.get('debit', '0')),
                credit=Decimal(line.get('credit', '0')),
            )
        return {"id": str(entry.id), "entry_number": entry.entry_number, "created": True}
