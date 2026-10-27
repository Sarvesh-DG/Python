"""Demonstrate abstract classes with concrete implementations."""
from abc import ABC, abstractmethod


class Person(ABC):
    """Represent a person whose gender label is provided by subclasses."""

    @abstractmethod
    def get_gender(self) -> str:
        """Return the implementation's gender label."""


class Male(Person):
    """Concrete person implementation."""

    def get_gender(self) -> str:
        return "Male"


class Female(Person):
    """Concrete person implementation."""

    def get_gender(self) -> str:
        return "Female"


def main() -> None:
    """Print the concrete implementations' labels."""
    for person in (Male(), Female()):
        print(person.get_gender())


if __name__ == "__main__":
    main()
