def itemize(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines: return ""
    result = [r"\begin{itemize}"] + [rf"\item {line}" for line in lines] + [r"\end{itemize}"]
    return "\n".join(result) + "\n"

def tabulize(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines: return ""
    columns_count = len(lines[0].split("\t"))
    param = "|" + "c|" * columns_count
    result = [r"\begin{table}", rf"\begin{{tabular}}{{{param}}}", r"\hline"]
    for line in lines:
        row_content = " & ".join(line.split("\t"))
        result.append(rf"{row_content} \\ \hline")
    result.extend([r"\end{tabular}", r"\end{table}"])
    return "\n".join(result) + "\n"

def tabbing(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines: return ""
    columns_count = len(lines[0].split("\t"))
    result = [r"\begin{tabbing}"]
    header = (r"\hspace{4cm}\=" * columns_count) + r"\kill"
    result.append(header)
    for line in lines:
        row_content = r" \> ".join(line.split("\t"))
        result.append(rf"{row_content} \\")
    result.append(r"\end{tabbing}")
    return "\n".join(result) + "\n"
