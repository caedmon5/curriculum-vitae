#!/usr/bin/env python3
import re
from pathlib import Path

path = Path("CV.tex")  # adjust if needed

brace_balance = 0
line_where_negative = None

# Simple regexes to skip escaped braces and comments
escaped_brace_pattern = re.compile(r'\\[{}]')
comment_pattern = re.compile(r'(?<!\\)%.*$')

for lineno, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
    # Strip comments
    line = comment_pattern.sub("", raw_line)

    # Remove escaped braces like \{ and \}
    line = escaped_brace_pattern.sub("", line)

    # Count remaining { and }
    for ch in line:
        if ch == "{":
            brace_balance += 1
        elif ch == "}":
            brace_balance -= 1
            if brace_balance < 0 and line_where_negative is None:
                line_where_negative = lineno

print(f"Final brace balance: {brace_balance}")
if line_where_negative is not None:
    print(f"First time balance goes negative: line {line_where_negative}")
else:
    print("Brace balance never goes negative.")

if brace_balance != 0:
    print("There is a net mismatch between { and } somewhere.")
