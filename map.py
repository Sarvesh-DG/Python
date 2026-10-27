"""Utilities for mapping ranges to their squares."""


def square_numbers(start: int, end: int) -> list[int]:
    """Return squares for inclusive integers from start to end.

    An end lower than start returns an empty list.
    """
    return list(map(lambda x:x**2 ,range(start,end+1)))
