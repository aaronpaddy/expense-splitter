from collections import defaultdict

import pytest

from expense_splitter import Transfer, format_transfers, settle_up


def apply_transfers(
    net_balances: dict[str, int], transfers: list[Transfer]
) -> dict[str, int]:
    """Apply transfers to a copy of net_balances and return the result."""
    result = defaultdict(int, net_balances)
    for transfer in transfers:
        result[transfer.sender] += transfer.amount_cents
        result[transfer.receiver] -= transfer.amount_cents
    return dict(result)


def test_settle_up_produces_minimal_transfers():
    net = {"ann": 5000, "bob": -1000, "cy": -4000}
    transfers = settle_up(net)
    assert transfers == [
        Transfer("cy", "ann", 4000),
        Transfer("bob", "ann", 1000),
    ]


def test_settle_up_one_debtor_one_creditor():
    net = {"ann": 1000, "bob": -1000}
    transfers = settle_up(net)
    assert transfers == [Transfer("bob", "ann", 1000)]


def test_settle_up_several_debtors_and_creditors():
    net = {"ann": 3000, "bob": 2000, "cy": -1000, "dan": -4000}
    transfers = settle_up(net)
    assert transfers == [
        Transfer("dan", "ann", 3000),
        Transfer("dan", "bob", 1000),
        Transfer("cy", "bob", 1000),
    ]


def test_settle_up_all_zero_balances_returns_empty_list():
    net = {"ann": 0, "bob": 0, "cy": 0}
    assert settle_up(net) == []


def test_settle_up_empty_input_returns_empty_list():
    assert settle_up({}) == []


def test_settle_up_clears_all_balances():
    net = {"ann": 5000, "bob": -1000, "cy": -4000, "dan": 3000, "eve": -3000}
    transfers = settle_up(net)
    result = apply_transfers(net, transfers)
    assert all(balance == 0 for balance in result.values())


def test_settle_up_is_deterministic_on_ties():
    net = {"zed": 1000, "ann": 1000, "bob": -1000, "yan": -1000}
    transfers = settle_up(net)
    assert transfers == [
        Transfer("bob", "ann", 1000),
        Transfer("yan", "zed", 1000),
    ]


def test_settle_up_raises_when_balances_do_not_sum_to_zero():
    net = {"ann": 100, "bob": -40}
    with pytest.raises(ValueError, match="sum to zero"):
        settle_up(net)


def test_format_transfers_renders_readable_lines():
    transfers = [
        Transfer("cy", "ann", 4000),
        Transfer("bob", "ann", 1000),
    ]
    assert format_transfers(transfers) == [
        "cy pays ann $40.00",
        "bob pays ann $10.00",
    ]


def test_format_transfers_empty_input_returns_empty_list():
    assert format_transfers([]) == []


def test_format_transfers_with_currency():
    transfers = [Transfer("cy", "ann", 1250)]
    assert format_transfers(transfers, "EUR") == ["cy pays ann \u20ac12.50"]


def test_format_transfers_unsupported_currency_raises():
    transfers = [Transfer("cy", "ann", 1250)]
    with pytest.raises(ValueError, match="unsupported currency"):
        format_transfers(transfers, "JPY")
