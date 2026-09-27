from decimal import Decimal

import pytest

from expense_splitter import format_cents, to_cents


def test_to_cents_whole_and_fractional_amounts():
    assert to_cents("12.50") == 1250
    assert to_cents("3") == 300
    assert to_cents(Decimal("0.99")) == 99


def test_to_cents_rounds_halves_up():
    assert to_cents("0.005") == 1
    assert to_cents("0.004") == 0


def test_format_cents():
    assert format_cents(1250) == "$12.50"
    assert format_cents(5) == "$0.05"
    assert format_cents(0) == "$0.00"


def test_format_cents_negative():
    assert format_cents(-1250) == "-$12.50"


def test_format_cents_eur():
    assert format_cents(1250, "EUR") == "\u20ac12.50"


def test_format_cents_gbp():
    assert format_cents(1250, "GBP") == "\u00a312.50"


def test_format_cents_currency_code_is_case_insensitive():
    assert format_cents(1250, "eur") == "\u20ac12.50"


def test_format_cents_negative_with_currency():
    assert format_cents(-1250, "EUR") == "-\u20ac12.50"


def test_format_cents_unsupported_currency_raises():
    with pytest.raises(ValueError, match="unsupported currency"):
        format_cents(1250, "JPY")
