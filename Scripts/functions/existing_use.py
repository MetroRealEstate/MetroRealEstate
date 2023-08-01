import re

def find_existing_used(text):
    # Regex pattern to match existing uses
    existing_regex = r'(?i)\bexisting\b[^.]*'
    existing_matches = re.findall(existing_regex, text)
    existing_used = existing_matches if existing_matches else ['-']
    return existing_used
