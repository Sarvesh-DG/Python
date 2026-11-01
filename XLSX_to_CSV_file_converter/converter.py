
import argparse
import re
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd


def get_google_sheet_id(url):
    """Extract the spreadsheet ID from a Google Sheets URL."""
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9_-]+)", url)

    if not match:
        raise ValueError("Invalid Google Sheets URL")

    return match.group(1)


def load_workbook(input_source):
    """Load a local XLSX file or download a Google Sheets workbook."""
    if input_source.startswith(("http://", "https://")):
        sheet_id = get_google_sheet_id(input_source)

        download_url = (
            f"https://docs.google.com/spreadsheets/d/"
            f"{sheet_id}/export?format=xlsx"
        )

        request = Request(
            download_url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urlopen(request, timeout=30) as response:
            workbook_data = response.read()

        return pd.ExcelFile(BytesIO(workbook_data)), sheet_id

    file_path = Path(input_source).expanduser()

    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.suffix.lower() != ".xlsx":
        raise ValueError("Input file must be an .xlsx file")

    return pd.ExcelFile(file_path), file_path.stem


def convert_to_csv(input_source):
    """Convert every worksheet into a separate CSV file."""
    workbook, output_name = load_workbook(input_source)

    output_dir = Path(output_name)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        for sheet_name in workbook.sheet_names:
            df = pd.read_excel(
                workbook,
                sheet_name=sheet_name,
                header=0
            )

            safe_sheet_name = re.sub(
                r'[<>:"/\\|?*\x00-\x1f]',
                "_",
                sheet_name
            ).strip(" .")

            if not safe_sheet_name:
                safe_sheet_name = "sheet"

            output_file = output_dir / f"{safe_sheet_name}.csv"

            df.to_csv(output_file, index=False, encoding="utf-8-sig")

            print(f"Converted: {sheet_name} -> {output_file}")

    finally:
        workbook.close()

    print(f"\nConversion completed: {output_dir.resolve()}")


def main():
    """Parse command-line arguments and run the converter."""
    parser = argparse.ArgumentParser(
        description="Convert XLSX or Google Sheets worksheets to CSV."
    )

    parser.add_argument(
        "input",
        help="Local XLSX file path or Google Sheets URL"
    )

    args = parser.parse_args()

    try:
        convert_to_csv(args.input)
    except Exception as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
