import re

def find_project_names(text):
    # Combined regex pattern to match project names
    project_name_regex = r'\b(?:PEN\d{2}-\d{4}|(?:PPM\d{4}-\d{4}|PM\s\d+|PC\s\d{2}-\d{4}|PP\d{4}-\d{4})|GPA\d{4}-\d{4}|PLN\d+-\d+|CUP\d{4}-\d{4}|\d{4}-\d{2}|\d{1,2}-\d{3}|No\. \d{6}|No\. \d{2}-\d{3}(?:-\d{1,4})?|No\. \d{2}-\d{2})\b'

    # Variable to store the matches of project names
    project_name_matches = []

    # Find all matches using the combined regex pattern
    matches = re.findall(project_name_regex, text, re.IGNORECASE)

    # Find the positions of 'Moreno Valley' and 'PUBLIC HEARING ITEMS'
    moreno_valley_pos = text.lower().find('moreno valley')
    hearing_start = text.find('PUBLIC HEARING ITEMS')
    hearing_end = text.find('OTHER COMMISSION BUSINESS')

    # Check if 'Moreno Valley' was found
    if moreno_valley_pos != -1:
        # Check if 'PUBLIC HEARING ITEMS' and 'OTHER COMMISSION BUSINESS' were found
        if hearing_start != -1 and hearing_end != -1:
            # Extract the text between 'PUBLIC HEARING ITEMS' and 'OTHER COMMISSION BUSINESS'
            text_between_hearing_and_commission = text[hearing_start + len('PUBLIC HEARING ITEMS'):hearing_end]

            # Find project names within the extracted text
            project_name_regex = r'\b(?:PEN\d{2}-\d{4}|(?:PPM\d{4}-\d{4}|PM\s\d+|PC\s\d{2}-\d{4}|PP\d{4}-\d{4})|GPA\d{4}-\d{4}|PLN\d+-\d+|CUP\d{4}-\d{4}|\d{4}-\d{2}|\d{1,2}-\d{3}|No\. \d{6}|No\. \d{2}-\d{3}(?:-\d{1,4})?|No\. \d{2}-\d{2})\b'
            project_names = re.findall(project_name_regex, text_between_hearing_and_commission, re.IGNORECASE)

    # Extend the list of matches
    project_name_matches.extend(matches)

    # Remove duplicates and assign value '-' if there are no matches
    project_names = list(set(project_name_matches)) if project_name_matches else ['-']

    return project_names
