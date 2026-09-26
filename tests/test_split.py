import pytest

from expense_splitter import split_by_weights, split_equally


def test_split_equally_when_total_divides_evenly():
    assert split_equally(900, ["ann", "bob", "cy"]) == {
        "ann": 300,
        "bob": 300,
        "cy": 300,
    }


def test_split_equally_rejects_empty_group():
    with pytest.raises(ValueError):
        split_equally(900, [])


def test_split_by_weights_exact_proportions():
    assert split_by_weights(1000, {"ann": 1, "bob": 3}) == {"ann": 250, "bob": 750}


def test_split_by_weights_distributes_leftover_to_largest_weights():
    shares = split_by_weights(100, {"ann": 1, "bob": 1, "cy": 1})
    assert sum(shares.values()) == 100
