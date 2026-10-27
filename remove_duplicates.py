"""Order-preserving duplicate removal."""


def remove_duplicates(values: list) -> list:
    """Return first occurrences in original order.

    Values must be hashable.
    """
    seen = set()
    unique_values = []
    for value in values:
        if value not in seen:
            seen.add(value)
            unique_values.append(value)
    return unique_values
