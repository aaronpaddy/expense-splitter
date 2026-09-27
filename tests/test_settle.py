from expense_splitter import Transfer, format_transfers, settle_up


def test_settle_up_produces_minimal_transfers():
    net = {"ann": 5000, "bob": -1000, "cy": -4000}
    transfers = settle_up(net)
    assert transfers == [
        Transfer("cy", "ann", 4000),
        Transfer("bob", "ann", 1000),
    ]


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
