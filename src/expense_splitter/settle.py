"""Work out who owes whom."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Mapping

from expense_splitter.models import Expense, Transfer, format_cents
from expense_splitter.split import split_equally


def balances(expenses: Iterable[Expense]) -> dict[str, int]:
    """Net balance per person, in cents.

    Positive means the person is owed money; negative means they owe money.
    """
    net: dict[str, int] = defaultdict(int)
    for expense in expenses:
        net[expense.payer] += expense.amount_cents
        shares = split_equally(expense.amount_cents, expense.participants)
        for person, share in shares.items():
            net[person] -= share
    return dict(net)


def settle_up(net_balances: Mapping[str, int]) -> list[Transfer]:
    """Return transfers that bring every balance to zero.

    Greedy: the biggest debtor pays the biggest creditor until one of them is
    square, then moves on. Ties are broken alphabetically so output is stable.
    """
    creditors = sorted(
        ((person, amount) for person, amount in net_balances.items() if amount > 0),
        key=lambda pair: (-pair[1], pair[0]),
    )
    debtors = sorted(
        ((person, -amount) for person, amount in net_balances.items() if amount < 0),
        key=lambda pair: (-pair[1], pair[0]),
    )
    credit_left = [amount for _, amount in creditors]
    debt_left = [amount for _, amount in debtors]

    transfers: list[Transfer] = []
    i = j = 0
    while i < len(creditors) and j < len(debtors):
        pay = min(credit_left[i], debt_left[j])
        transfers.append(Transfer(debtors[j][0], creditors[i][0], pay))
        credit_left[i] -= pay
        debt_left[j] -= pay
        if credit_left[i] == 0:
            i += 1
        if debt_left[j] == 0:
            j += 1
    return transfers


def format_transfers(transfers: Iterable[Transfer]) -> list[str]:
    """Render transfers as human-readable lines like "cy pays ann $40.00"."""
    lines = []
    for transfer in transfers:
        amount = format_cents(transfer.amount_cents)
        lines.append(f"{transfer.sender} pays {transfer.receiver} {amount}")
    return lines
