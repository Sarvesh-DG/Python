
import json
import re
from pathlib import Path

import mysql.connector
import pandas as pd


INPUT_FILE = Path("sample_data_for_assignment.json")

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "json_assignment",
}


def load_json(file_path):
    """Read and validate the JSON dataset."""
    with file_path.open("r", encoding="utf-8") as file:
        json_data = json.load(file)

    cols = json_data["cols"]
    rows = json_data["data"]

    required_cols = ["id", "name", "email", "postalZip", "phone"]

    if cols != required_cols:
        raise ValueError(f"Unexpected columns: {cols}")

    for index, row in enumerate(rows):
        if len(row) != len(cols):
            raise ValueError(f"Invalid row at index {index}")

    if not rows:
        raise ValueError("JSON contains no records")

    ids = [row[0] for row in rows]

    if any(value is None for value in ids):
        raise ValueError("ID cannot be NULL")

    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate IDs found")

    return cols, rows


def load_to_mysql(rows):
    """Load JSON records into the MySQL table."""
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS json_to_sql_table (
                id INT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(255),
                postalZip VARCHAR(20),
                phone VARCHAR(30)
            )
        """)

        insert_query = """
            INSERT INTO json_to_sql_table
            (id, name, email, postalZip, phone)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute("DELETE FROM json_to_sql_table")
        cursor.executemany(insert_query, rows)

        connection.commit()

        print("Records loaded:", len(rows))

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def retrieve_data():
    """Retrieve MySQL records and return a pandas DataFrame."""
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT id, name, email, postalZip, phone
            FROM json_to_sql_table
            ORDER BY id
        """)

        retrieved_rows = cursor.fetchall()

        column_names = [
            column[0] for column in cursor.description
        ]

        return pd.DataFrame(
            retrieved_rows,
            columns=column_names
        )

    finally:
        cursor.close()
        connection.close()


def normalize_email(email):
    """Replace the email domain with gmail.com."""
    if not isinstance(email, str):
        raise ValueError(f"Invalid email: {email}")

    email = email.strip()

    if email.count("@") != 1:
        raise ValueError(f"Malformed email: {email}")

    local_part, domain = email.rsplit("@", 1)

    if not local_part or not domain:
        raise ValueError(f"Malformed email: {email}")

    return local_part + "@gmail.com"


def clean_postal_zip(value):
    """Remove non-digits from a postal code and convert it to int."""
    if value is None or pd.isna(value):
        raise ValueError("Missing postalZip")

    digits = re.sub(r"\D", "", str(value))

    if not digits:
        raise ValueError(f"No digits in postalZip: {value}")

    return int(digits)


def encode_phone(phone):
    """Encode phone digit pairs into ASCII characters."""
    if phone is None or pd.isna(phone):
        raise ValueError("Missing phone number")

    digits = re.sub(r"\D", "", str(phone))

    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]

    if not digits:
        raise ValueError(f"No digits in phone: {phone}")

    if len(digits) % 2 != 0:
        raise ValueError(f"Odd number of digits in phone: {phone}")

    encoded = []

    for index in range(0, len(digits), 2):
        pair = digits[index:index + 2]
        ascii_value = int(pair)

        if ascii_value < 65:
            encoded.append("O")
        else:
            encoded.append(chr(ascii_value))

    return "".join(encoded)


def transform_data(df):
    """Normalize emails, clean postal codes, and encode phone numbers."""
    df = df.copy()

    df["email"] = df["email"].apply(normalize_email)
    df["postalZip"] = df["postalZip"].apply(clean_postal_zip)
    df["phone"] = df["phone"].apply(encode_phone)

    df.rename(
        columns={"phone": "coded_phone_number"},
        inplace=True
    )

    return df


def main():
    """Run the JSON-to-MySQL data manipulation pipeline."""
    _, rows = load_json(INPUT_FILE)

    load_to_mysql(rows)

    df = retrieve_data()
    df = transform_data(df)

    print("\nFinal transformed DataFrame:\n")
    print(df.to_string(index=False))

    print("\nDataFrame shape:", df.shape)

    df.to_csv("transformed_output.csv", index=False)

    print("\nSaved transformed_output.csv")


if __name__ == "__main__":
    main()
