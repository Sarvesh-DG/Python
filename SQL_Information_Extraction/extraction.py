
import argparse
import json
import re
from pathlib import Path


def extract_procedures(sql_text):
    """Extract stored procedure definitions and their metadata."""

    procedure_pattern = re.compile(
        r"""
        CREATE\s+PROCEDURE\s+
        `?([A-Za-z_]\w*)`?
        \s*\((.*?)\)
        \s*BEGIN
        (.*?)
        END
        \s*(?://|;)
        """,
        re.IGNORECASE | re.DOTALL | re.VERBOSE
    )

    parameter_pattern = re.compile(
        r"""
        (?:(INOUT|IN|OUT)\s+)?
        `?([A-Za-z_]\w*)`?
        \s+
        ([A-Za-z]+(?:\s*\([^)]*\))?)
        """,
        re.IGNORECASE | re.VERBOSE
    )

    procedures = []

    for match in procedure_pattern.finditer(sql_text):
        procedure_name = match.group(1)
        parameter_text = match.group(2).strip()
        procedure_body = match.group(3).strip()

        parameters = []

        if parameter_text:
            for parameter in parameter_text.split(","):
                parameter_match = parameter_pattern.fullmatch(
                    parameter.strip()
                )

                if parameter_match:
                    parameters.append({
                        "mode": (
                            parameter_match.group(1) or "IN"
                        ).upper(),
                        "name": parameter_match.group(2),
                        "data_type": re.sub(
                            r"\s+", "", parameter_match.group(3)
                        ).upper()
                    })

        statements = [
            statement.strip()
            for statement in procedure_body.split(";")
            if statement.strip()
        ]

        tables = sorted(set(
            re.findall(
                r"""
                \b(?:FROM|JOIN|UPDATE|INTO)
                \s+`?([A-Za-z_]\w*)`?
                """,
                procedure_body,
                re.IGNORECASE | re.VERBOSE
            )
        ))

        procedures.append({
            "procedure_name": procedure_name,
            "parameters": parameters,
            "tables": tables,
            "statements": statements,
            "body": procedure_body
        })

    return procedures


def main():
    """Read a SQL file and export extracted procedures to JSON."""

    parser = argparse.ArgumentParser(
        description="Extract stored procedure information from SQL."
    )

    parser.add_argument(
        "sql_file",
        type=Path,
        help="Path to the input SQL file"
    )

    args = parser.parse_args()

    if not args.sql_file.is_file():
        parser.error(f"File not found: {args.sql_file}")

    if args.sql_file.suffix.lower() != ".sql":
        parser.error("Input file must have a .sql extension")

    sql_text = args.sql_file.read_text(encoding="utf-8")

    procedures = extract_procedures(sql_text)

    if not procedures:
        parser.error("No supported stored procedures found")

    output_file = args.sql_file.with_suffix(".json")

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(
            procedures,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Procedures extracted: {len(procedures)}")
    print(f"Output saved to: {output_file}")


if __name__ == "__main__":
    main()
