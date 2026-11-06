# SQL Information Extraction

Extracts stored procedure names, parameter metadata, table references, statements, and body text into JSON.

## Run
```bash
python extraction.py sample_stored_procedure.sql
```
Optional output path:
```bash
python extraction.py sample_stored_procedure.sql --output output/procedures.json
```

## Tests
From this folder:
```bash
python -m unittest -v
```

The parser handles nested parentheses in parameter declarations (for example `DECIMAL(10,2)`), IN/OUT/INOUT modes, multiple procedures, comments, and nested `BEGIN ... END` blocks. It is a focused parser for common MySQL stored-procedure syntax, not a complete MySQL grammar.
