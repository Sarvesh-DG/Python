# Week 1 Python Assignments — Improved

This cleaned version addresses the Week 1 review remarks while keeping the original assignment themes.

## What's improved
- PEP 8 formatting, clearer names, docstrings, and type annotations.
- Database connection settings are read from environment variables (`DB_USER`, `DB_PASSWORD`, etc.); no credentials are embedded in code.
- Employee records are streamed with `fetchmany()` and the cursor/connection are closed even when query execution fails.
- `anti_html.py` accepts a URL command-line argument and validates it before making an HTTP request.
- Tests cover typical behavior, boundary cases, invalid inputs, and error handling. Network and database calls are mocked.
- `.gitignore` excludes virtual environments, bytecode/cache files, local secrets, and the dataset.

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run tests
```powershell
python -m unittest discover -s tests -v
```

## Run examples
```powershell
python abc1.py
python anti_html.py https://example.com
python -c "from map import square_numbers; print(square_numbers(1, 5))"
python -c "from remove_duplicates import remove_duplicates; print(remove_duplicates([1, 2, 1]))"
python e.py
python t.py path\to\survey_results_public.csv
```

## MySQL assignment
1. Install/configure MySQL and ensure the `employees` database and `employees` table exist.
2. Set environment variables in the current PowerShell session (avoid typing real secrets into shared terminals):
```powershell
$env:DB_HOST = "localhost"
$env:DB_PORT = "3306"
$env:DB_USER = "your_user"
$env:DB_PASSWORD = "your_password"
$env:DB_NAME = "employees"
python fetch_employees.py
```
`fetch_employees()` expects a table named `employees`; adapt its SELECT statement if your schema differs. The program streams rows, but the exact returned columns depend on that schema.

## Git hygiene
This deliverable omits `.git`, both virtual environments, Python caches/bytecode, and the local CSV. In your repository, add/keep `.gitignore`, then untrack files already committed:
```powershell
git rm -r --cached __pycache__
git rm -r --cached .venv
git add .gitignore
git status
git commit -m "Improve Week 1 code quality and tests"
```
If any of those paths are absent, Git may report a path error; remove only paths that are actually tracked. If a virtual environment or secrets were committed before, `.gitignore` alone does not remove them from history. Rotate any exposed credentials.

## Notes
- The survey summary uses `errors="coerce"` so category text such as “Younger than 5 years” is treated as missing instead of causing a conversion exception.
- `remove_duplicates()` expects hashable values (such as strings, integers, and tuples).
