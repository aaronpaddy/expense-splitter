"""Core data types and money helpers.

All money is stored as integer cents so no arithmetic ever touches floats.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


def to_cents(amount: str | Decimal) -> int:
    """Convert a decimal amount such as "12.50" to integer cents.

    Halves round up, so "0.005" becomes 1 cent.
    """
    cents = (Decimal(amount) * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP)
    return int(cents)


#: Currency symbols for supported ISO 4217 currency codes.
CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "\u20ac",
    "GBP": "\u00a3",
}

DEFAULT_CURRENCY = "USD"


def format_cents(cents: int, currency: str = DEFAULT_CURRENCY) -> str:
    """Render integer cents as a currency string, e.g. 1250 -> "$12.50".

    Args:
        cents: The amount in integer cents.
        currency: An ISO 4217 currency code, e.g. "USD", "EUR" or "GBP".
            Defaults to "USD".

    Raises:
        ValueError: if the currency code isn't supported.
    """
    try:
        symbol = CURRENCY_SYMBOLS[currency.upper()]
    except KeyError:
        supported = ", ".join(sorted(CURRENCY_SYMBOLS))
        raise ValueError(
            f"unsupported currency {currency!r}; supported currencies: {supported}"
        ) from None
    sign = "-" if cents < 0 else ""
    dollars, remainder = divmod(abs(cents), 100)
    return f"{sign}{symbol}{dollars}.{remainder:02d}"


@dataclass(frozen=True)
class Expense:
    """One payment made on behalf of a group."""

    payer: str
    amount_cents: int
    participants: tuple[str, ...]
    description: str = ""


@dataclass(frozen=True)
class Transfer:
    """A payment one person should make to settle up."""

    sender: str
    receiver: str
    amount_cents: int
