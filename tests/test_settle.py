from collections import defaultdict
from collections.abc import Mapping

from expense_splitter import Transfer, settle_up


def apply_transfers(
    net_balances: Mapping[str, int], transfers: list[Transfer]
) -> dict[str, int]:
    """Apply transfers to a copy of net_balances and return the result."""
    result: dict[str, int] = defaultdict(int, net_balances)
    for transfer in transfers:
        result[transfer.sender] += transfer.amount_cents
        result[transfer.receiver] -= transfer.amount_cents
    return dict(result)


def test_one_debtor_paying_one_creditor():
    net_balances = {"ann": 500, "bob": -500}
    transfers = settle_up(net_balances)
    assert transfers == [Transfer("bob", "ann", 500)]


def test_several_debtors_and_creditors():
    net_balances = {
        "ann": 700,
        "bob": 300,
        "cy": -400,
        "dee": -600,
    }
    transfers = settle_up(net_balances)
    assert apply_transfers(net_balances, transfers) == {
        "ann": 0,
        "bob": 0,
        "cy": 0,
        "dee": 0,
    }
    assert sum(t.amount_cents for t in transfers) == 1000


def test_balances_already_zero_returns_empty_list():
    assert settle_up({}) == []
    assert settle_up({"ann": 0, "bob": 0}) == []


def test_transfers_bring_every_balance_to_zero():
    net_balances = {"ann": 1000, "bob": 500, "cy": -300, "dee": -1200}
    transfers = settle_up(net_balances)
    result = apply_transfers(net_balances, transfers)
    assert all(value == 0 for value in result.values())


def test_output_is_deterministic_when_amounts_tie():
    net_balances = {
        "zed": 500,
        "ann": 500,
        "bob": -500,
        "amy": -500,
    }
    transfers = settle_up(net_balances)
    # Ties broken alphabetically: creditors ann before zed, debtors amy before bob.
    assert transfers == [
        Transfer("amy", "ann", 500),
        Transfer("bob", "zed", 500),
    ]
