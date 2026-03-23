def csv_to_python_table(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines: return ""
    tablename = lines[0].split()[0] if lines[0] else "Table"
    if len(lines) == 2:
        fieldsnames = [f"'{field.strip()}'" for field in lines[1].split("\t")]
        return f"{tablename} = ({', '.join(fieldsnames)})\n"
    return f"{tablename} = {{}}\n"
