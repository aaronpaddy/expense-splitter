# expense-splitter

A small Python library for splitting shared expenses fairly and working out who should pay whom. Think of a group trip: everyone pays for different things, and at the end you want the fewest, simplest payments that make everyone even.

All money is handled as **integer cents**, so results are exact and never touch floating point.

## Install

```bash
pip install -e .
```

Requires Python 3.11+. No runtime dependencies.

## Usage

```python
from expense_splitter import Expense, balances, format_cents, settle_up, to_cents

expenses = [
    Expense("ann", to_cents("90.00"), ("ann", "bob", "cy"), "dinner"),
    Expense("bob", to_cents("30.00"), ("ann", "bob", "cy"), "taxi"),
]

net = balances(expenses)
# {'ann': 5000, 'bob': -1000, 'cy': -4000}  (positive = is owed, negative = owes)

for transfer in settle_up(net):
    print(f"{transfer.sender} pays {transfer.receiver} {format_cents(transfer.amount_cents)}")
# cy pays ann $40.00
# bob pays ann $10.00
```

### API

| Function | What it does |
|---|---|
| `to_cents(amount)` | Convert `"12.50"` to `1250` (halves round up) |
| `format_cents(cents)` | Convert `1250` to `"$12.50"` |
| `split_equally(total_cents, people)` | Divide a total evenly among people |
| `split_by_weights(total_cents, weights)` | Divide a total in proportion to integer weights |
| `balances(expenses)` | Net amount each person is owed (positive) or owes (negative) |
| `settle_up(net_balances)` | Transfers that bring every balance to zero |

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

pytest
ruff check .
black --check .
mypy src
```

CI runs all four on every push and pull request.

## License

MIT
