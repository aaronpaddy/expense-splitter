"""Ways to divide a total among people."""

from __future__ import annotations

from collections.abc import Mapping, Sequence


def split_equally(total_cents: int, people: Sequence[str]) -> dict[str, int]:
    """Split total_cents evenly among people.

    Every cent is assigned to someone: when the total does not divide evenly,
    the leftover cents go one each to the first people in the given order, so
    the shares always add up to total_cents.
    """
    if not people:
        raise ValueError("people must not be empty")
    share = total_cents // len(people)
    return {person: share for person in people}


def split_by_weights(total_cents: int, weights: Mapping[str, int]) -> dict[str, int]:
    """Split total_cents in proportion to integer weights.

    Each share is rounded down, then the leftover cents go one each to the
    people with the largest weights, so the shares add up to total_cents.
    """
    total_weight = sum(weights.values())
    shares = {
        person: total_cents * weight // total_weight
        for person, weight in weights.items()
    }
    leftover = total_cents - sum(shares.values())
    by_weight = sorted(weights, key=lambda person: weights[person], reverse=True)
    for person in by_weight[:leftover]:
        shares[person] += 1
    return shares
