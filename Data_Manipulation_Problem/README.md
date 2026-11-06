# Data Manipulation

Reads and validates the supplied JSON records, loads them into MySQL, retrieves them, normalizes email/postal-code values, and encodes phone digit pairs.

## Configuration
Copy `.env.example` to `.env` and set `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME`. Do not commit `.env`.

## Run
Install dependencies:
```bash
pip install pandas mysql-connector-python python-dotenv
```
Run from this folder:
```bash
python json_to_mysql.py
```
Or pass a JSON file and output path:
```bash
python json_to_mysql.py sample_data_for_assignment.json --output transformed_output.csv
```

## Phone encoding rules implemented
- Remove non-digit characters.
- For an 11-digit number beginning with `1`, remove the leading country-code digit.
- Encode complete two-digit groups as ASCII characters.
- Map each pair value below 65 to `O`.
- Ignore a final unmatched digit if the digit count is odd.

## Tests
The tests do not connect to MySQL:
```bash
python -m unittest -v
```
