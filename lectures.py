import re

def format_cvitems(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    total = len(lines)
    result = []

    for i, line in enumerate(lines):
        num = total - i
        # Optional: extract flags like (risc) and move to front
        flags_match = re.search(r'\(([risc]+)\)', line)
        if flags_match:
            flags = flags_match.group(1)
            line = re.sub(r'\s*\([risc]+\)', '', line)  # remove flags from end
        else:
            flags = ''

        formatted = f"\\cvitem{{[{num}]}}{{{flags} {line}}}".strip()
        result.append(formatted)
    
    return '\n\n'.join(result)

# Example usage
output = format_cvitems('lectures.txt')
with open('lectures_output.tex', 'w') as f:
    f.write(output)
