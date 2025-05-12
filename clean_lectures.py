import re

# Set the name to bold
your_name = "O'Donnell, Daniel Paul"
your_variants = [
    "Daniel Paul O’Donnell", "Daniel Paul O'Donnell", "O’Donnell, Daniel Paul", "O'Donnell, Daniel Paul",
    "Daniel P. O’Donnell", "Daniel P. O'Donnell"
]

# List of student authors (Lastname, Firstname format)
student_authors = {
    "Pafumi, Davide",
    "Onuh, Frank",
    "Khalid, AKM Iftekhar",
    "Pearce, Morgan Slayde",
    "Esau, Paul",
    "Viejou, Carey",
    "Chow, Sylvia",
    "McKinnon, Jarret",
    "Parsons, Reed",
    "Singh, Gurpreet",
    "Bay, Jessica",
    "Dering, Emma",
    "Hobma, Heather",
    "Gal, Matt",
    "Grandfield, Virgil",
    "Devine, Kelaine",
    "Ayers, Gillian"
}

def format_author(name):
    """Reformats a name to Lastname, Firstname and adds asterisk if student."""
    name = name.strip().replace("  ", " ")
    parts = name.split()
    if len(parts) < 2:
        return name
    if ',' in name:
        lastname, firstname = [x.strip() for x in name.split(",", 1)]
    else:
        firstname = " ".join(parts[:-1])
        lastname = parts[-1]
    formatted = f"{lastname}, {firstname}"
    if formatted in student_authors:
        formatted += "*"
    return formatted

def process_entry(entry):
    # Bold your name (all variants)
    for variant in your_variants:
        entry = re.sub(re.escape(variant), r'\\textbf{' + your_name + r'}', entry)

    # Find the part with author list (before first . after the flag)
    match = re.match(r"(\\cvitem\{\[\d+\]\}\{ ?[risc]* )(.*?)(\.\s)", entry)
    if match:
        head, authors_raw, rest = match.groups()
        authors = [a.strip() for a in re.split(",| and ", authors_raw)]
        formatted_authors = ", ".join([format_author(a) for a in authors])
        new_entry = head + formatted_authors + rest + entry[match.end():]
        return new_entry
    return entry

def clean_tex_file(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    processed = [process_entry(line.strip()) for line in lines if line.strip()]
    
    with open(output_file, 'w') as f:
        f.write("\n\n".join(processed))

    print(f"✅ Processed {len(processed)} entries. Output saved to {output_file}")

# Example usage
clean_tex_file("lectures_output.tex", "lectures_cleaned.tex")
