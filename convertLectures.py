import re

def format_cvitems(file_path, start_number):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    total = len(lines)
    result = []

    for i, line in enumerate(lines):
        num = start_number - i
        # Optional: extract flags (r, i, s, c) in parentheses
        flags_match = re.search(r'\(([risc]+)\)', line)
        flags = flags_match.group(1) if flags_match else ''
        formatted = f"\\cvitem{{[{num}]}}{{{flags} {line}}}"
        result.append(formatted)
    
    return '\n\n'.join(result)

# Example usage
output = format_cvitems('lectures.txt', 127)  # adjust 127 to your top number
with open('lectures_output.tex', 'w') as f:
    f.write(output)
