"""Stream employee records from MySQL in batches."""
import os
from collections.abc import Iterator
from typing import Any
from dotenv import load_dotenv

load_dotenv()

def fetch_employees(batch_size: int = 1000) -> Iterator[tuple[Any, ...]]:
    """Yield employee rows using environment-configured MySQL credentials.

    Required: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME.
    DB_PORT is optional (defaults to 3306).
    """
    if not isinstance(batch_size, int) or isinstance(batch_size, bool) or batch_size <= 0:
        raise ValueError("batch_size must be a positive integer")

    config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME", "employees"),
        "port": int(os.getenv("DB_PORT", "3306")),
    }
    if not config["user"] or config["password"] is None:
        raise RuntimeError("Set DB_USER and DB_PASSWORD environment variables.")

    import mysql.connector

    connection = mysql.connector.connect(**config)
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employees")
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield from rows
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def main() -> None:
    """Print employees as they are fetched."""
    for employee in fetch_employees():
        print(employee)


if __name__ == "__main__":
    main()
