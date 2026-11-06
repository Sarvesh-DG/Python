import argparse
import json
import re
from pathlib import Path


def split_sql_parameters(parameter_text):
    """Split procedure parameters on commas outside parentheses and quotes."""
    parts, current = [], []
    depth, quote, i = 0, None, 0
    while i < len(parameter_text):
        char = parameter_text[i]
        if quote:
            current.append(char)
            if char == quote:
                if i + 1 < len(parameter_text) and parameter_text[i + 1] == quote:
                    current.append(parameter_text[i + 1])
                    i += 1
                else:
                    quote = None
        elif char in ("'", '"', "`"):
            quote = char
            current.append(char)
        elif char == "(":
            depth += 1
            current.append(char)
        elif char == ")":
            depth -= 1
            current.append(char)
        elif char == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        i += 1
    if current and "".join(current).strip():
        parts.append("".join(current).strip())
    return parts


def parse_parameter(parameter):
    """Parse [IN|OUT|INOUT] name data_type, retaining precision/scale."""
    match = re.fullmatch(
        r"\s*(?:(INOUT|IN|OUT)\s+)?`?([A-Za-z_]\w*)`?\s+"
        r"([A-Za-z][A-Za-z0-9_]*(?:\s*\([^()]*\))?)\s*",
        parameter,
        re.IGNORECASE,
    )
    if not match:
        return None
    return {
        "mode": (match.group(1) or "IN").upper(),
        "name": match.group(2),
        "data_type": re.sub(r"\s+", "", match.group(3)).upper(),
    }


def _mask_comments_and_strings(sql):
    """Replace comments and string contents with spaces, preserving positions."""
    out = list(sql)
    i, n = 0, len(sql)
    while i < n:
        if sql.startswith("--", i) or sql[i] == "#":
            j = sql.find("\n", i)
            if j == -1:
                j = n
            for k in range(i, j):
                if out[k] != "\n":
                    out[k] = " "
            i = j
        elif sql.startswith("/*", i):
            j = sql.find("*/", i + 2)
            j = n if j == -1 else j + 2
            for k in range(i, j):
                if out[k] != "\n":
                    out[k] = " "
            i = j
        elif sql[i] in ("'", '"'):
            quote = sql[i]
            out[i] = " "
            i += 1
            while i < n:
                if sql[i] == "\\":
                    out[i] = " "
                    if i + 1 < n:
                        out[i + 1] = " "
                    i += 2
                elif sql[i] == quote:
                    out[i] = " "
                    i += 1
                    break
                else:
                    if out[i] != "\n":
                        out[i] = " "
                    i += 1
        else:
            i += 1
    return "".join(out)


def _matching_paren(text, open_index):
    depth = 0
    for i in range(open_index, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError("Unclosed parenthesis in procedure parameter list")


def _find_procedure_end(masked, body_start):
    """Find the procedure's matching END, ignoring END IF/CASE/LOOP tokens."""
    token_re = re.compile(
        r"\bBEGIN\b|\bEND\b(?:\s+(?:IF|CASE|WHILE|LOOP))?",
        re.IGNORECASE,
    )
    depth = 1
    for match in token_re.finditer(masked, body_start):
        token = match.group().upper()
        if token == "BEGIN":
            depth += 1
        elif token in ("END IF", "END CASE", "END WHILE", "END LOOP"):
            continue
        else:
            depth -= 1
            if depth == 0:
                return match.start(), match.end()
    raise ValueError("Could not find matching END for procedure body")

def _extract_tables(body):
    """Find table references while excluding SELECT ... INTO variable targets."""
    masked = _mask_comments_and_strings(body)
    found = set()
    patterns = [
        r"\b(?:FROM|JOIN)\s+`?([A-Za-z_]\w*)`?",
        r"\bUPDATE\s+`?([A-Za-z_]\w*)`?",
        r"\bINSERT\s+INTO\s+`?([A-Za-z_]\w*)`?",
        r"\bREPLACE\s+INTO\s+`?([A-Za-z_]\w*)`?",
        r"\bDELETE\s+FROM\s+`?([A-Za-z_]\w*)`?",
    ]
    for pattern in patterns:
        found.update(re.findall(pattern, masked, re.IGNORECASE))
    return sorted(found)


def extract_procedures(sql_text):
    """Extract stored procedures, parameters, table references and statements."""
    masked = _mask_comments_and_strings(sql_text)
    create_re = re.compile(
        r"\bCREATE\s+(?:DEFINER\s*=\s*[^\s]+\s+)?PROCEDURE\s+"
        r"`?([A-Za-z_]\w*)`?\s*\(",
        re.IGNORECASE,
    )
    procedures = []
    for create in create_re.finditer(masked):
        name = create.group(1)
        open_paren = masked.find("(", create.start())
        close_paren = _matching_paren(masked, open_paren)
        parameter_text = sql_text[open_paren + 1:close_paren]
        begin_match = re.search(r"\bBEGIN\b", masked[close_paren + 1:], re.IGNORECASE)
        if not begin_match:
            continue
        body_start = close_paren + 1 + begin_match.end()
        body_end_start, body_end = _find_procedure_end(masked, body_start)
        body = sql_text[body_start:body_end_start].strip()
        parameters = [
            parsed for item in split_sql_parameters(parameter_text)
            if (parsed := parse_parameter(item)) is not None
        ]
        statements = [
            part.strip() for part in re.split(r";", body) if part.strip()
        ]
        procedures.append({
            "procedure_name": name,
            "parameters": parameters,
            "tables": _extract_tables(body),
            "statements": statements,
            "body": body,
        })
    return procedures


def main():
    parser = argparse.ArgumentParser(
        description="Extract stored procedure information from a SQL file."
    )
    parser.add_argument("sql_file", type=Path, help="Input .sql file")
    parser.add_argument("-o", "--output", type=Path, help="Output JSON path")
    args = parser.parse_args()

    if args.sql_file.suffix.lower() != ".sql":
        parser.error("Input file must have a .sql extension")
    if not args.sql_file.is_file():
        parser.error(f"File not found: {args.sql_file}")

    try:
        procedures = extract_procedures(args.sql_file.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    if not procedures:
        parser.error("No supported stored procedures found")

    output_file = args.output or args.sql_file.with_suffix(".json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(procedures, indent=4), encoding="utf-8")
    print(f"Procedures extracted: {len(procedures)}")
    print(f"Output saved to: {output_file}")


if __name__ == "__main__":
    main()
