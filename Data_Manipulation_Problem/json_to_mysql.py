import argparse
import json
import os
import re
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def get_db_config():
    """Read database settings from environment variables."""
    required = ("DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME")
    config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME", "json_assignment"),
        "port": int(os.getenv("DB_PORT", "3306")),
    }
    env_names = {
        "DB_HOST": "DB_HOST",
        "DB_USER": "DB_USER",
        "DB_PASSWORD": "DB_PASSWORD",
        "DB_NAME": "DB_NAME",
    }
    missing = [name for name, env_name in env_names.items() if not os.getenv(env_name)]
    if missing:
        raise ValueError("Missing database environment variables: " + ", ".join(missing))
    return config


def load_json(file_path):
    """Read and validate the JSON dataset."""
    file_path = Path(file_path).expanduser()
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


def load_to_mysql(rows, db_config):
    """Load JSON records into MySQL using a transaction."""
    import mysql.connector

    connection = mysql.connector.connect(**db_config)
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
        cursor.execute("DELETE FROM json_to_sql_table")
        cursor.executemany("""
            INSERT INTO json_to_sql_table
            (id, name, email, postalZip, phone)
            VALUES (%s, %s, %s, %s, %s)
        """, rows)
        connection.commit()
        print("Records loaded:", len(rows))
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def retrieve_data(db_config):
    """Retrieve records from MySQL as a DataFrame."""
    import mysql.connector

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT id, name, email, postalZip, phone
            FROM json_to_sql_table
            ORDER BY id
        """)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return pd.DataFrame(rows, columns=columns)
    finally:
        cursor.close()
        connection.close()


def normalize_email(email):
    """Trim whitespace and replace the domain with gmail.com."""
    if not isinstance(email, str):
        raise ValueError(f"Invalid email: {email}")
    email = email.strip()
    if email.count("@") != 1:
        raise ValueError(f"Malformed email: {email}")
    local_part, domain = email.rsplit("@", 1)
    if not local_part or not domain:
        raise ValueError(f"Malformed email: {email}")
    return f"{local_part}@gmail.com"


def clean_postal_zip(value):
    """Keep digits from postal codes and return them as a string."""
    if value is None or pd.isna(value):
        raise ValueError("Missing postalZip")
    digits = re.sub(r"\D", "", str(value))
    if not digits:
        raise ValueError(f"No digits in postalZip: {value}")
    return digits


def encode_phone(phone):
    """
    Encode digit pairs as ASCII characters.
    A leading 1 on an 11-digit number is treated as country code.
    Any remaining unmatched final digit is ignored.
    Pair values below 65 map to the letter O.
    """
    if phone is None or pd.isna(phone):
        raise ValueError("Missing phone number")
    digits = re.sub(r"\D", "", str(phone))
    if not digits:
        raise ValueError(f"No digits in phone: {phone}")
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    digits = digits[:len(digits) // 2 * 2]
    encoded = []
    for index in range(0, len(digits), 2):
        value = int(digits[index:index + 2])
        encoded.append("O" if value < 65 else chr(value))
    return "".join(encoded)


def transform_data(df):
    """Normalize email, postal code and phone columns."""
    df = df.copy()
    df["email"] = df["email"].apply(normalize_email)
    df["postalZip"] = df["postalZip"].apply(clean_postal_zip)
    df["phone"] = df["phone"].apply(encode_phone)
    return df.rename(columns={"phone": "coded_phone_number"})


def main():
    parser = argparse.ArgumentParser(description="Transform JSON data and load it into MySQL.")
    parser.add_argument("input_file", nargs="?", type=Path,
                        default=Path(__file__).with_name("sample_data_for_assignment.json"))
    parser.add_argument("--output", type=Path, default=Path("transformed_output.csv"))
    args = parser.parse_args()

    _, rows = load_json(args.input_file)
    db_config = get_db_config()
    load_to_mysql(rows, db_config)
    transformed = transform_data(retrieve_data(db_config))
    transformed.to_csv(args.output, index=False)
    print(transformed.to_string(index=False))
    print(f"\nSaved: {args.output}")


if __name__ == "__main__":
    main()
