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


def test_split_equally_distributes_leftover_cents_to_first_people():
    assert split_equally(100, ["ann", "bob", "cy"]) == {
        "ann": 34,
        "bob": 33,
        "cy": 33,
    }


@pytest.mark.parametrize("total_cents", range(0, 20))
@pytest.mark.parametrize("group_size", range(1, 7))
def test_split_equally_shares_sum_to_total(total_cents, group_size):
    people = [f"person{i}" for i in range(group_size)]
    shares = split_equally(total_cents, people)
    assert sum(shares.values()) == total_cents


def test_split_by_weights_exact_proportions():
    assert split_by_weights(1000, {"ann": 1, "bob": 3}) == {"ann": 250, "bob": 750}


def test_split_by_weights_distributes_leftover_to_largest_weights():
    shares = split_by_weights(100, {"ann": 1, "bob": 1, "cy": 1})
    assert sum(shares.values()) == 100
