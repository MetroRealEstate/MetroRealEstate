import re

def search_applicants(text, excluded_phrases=[]):
    moreno_matrix = r'(?s)(?<=PUBLIC HEARING ITEMS).*?(?=OTHER COMMISSION BUSINESS)'
    eastvale_regex = r'(?s)Project Description:(.*?)Planner:\s*([A-Z][a-z]+ [A-Z][a-z]+)\s*Notes:'
    # Search for applicant names
    applicant_regex = r"Applicant: ([A-Z][a-z]+ [A-Z][a-z]+)"
    applicant_matches = re.findall(applicant_regex, text, re.I | re.M)
    if not applicant_matches:
        applicant_regex = r"\b[A-Z][a-z]+ [A-Z][a-z]+\b(?:\sDevelopment Group)?"
        applicant_matches = re.findall(applicant_regex, text)
    if not applicant_matches:
        applicant_regex = r"Owner:\s*([^.,\n]+)"
        applicant_matches = re.findall(applicant_regex, text)

    if 'Moreno Valley' in text:
        # Extract the text between 'PUBLIC HEARING ITEMS' and 'OTHER COMMISSION BUSINESS'
        text_between_hearing_and_commission = re.findall(moreno_matrix, text)[0]

        # Search for applicant names within the extracted text
        applicant_matches_moreno = re.findall(applicant_regex, text_between_hearing_and_commission, re.I | re.M)
        if not applicant_matches_moreno:
            applicant_regex = r"\b[A-Z][a-z]+ [A-Z][a-z]+\b(?:\sDevelopment Group)?"
            applicant_matches_moreno = re.findall(applicant_regex, text_between_hearing_and_commission)
        if not applicant_matches_moreno:
            applicant_regex = r"Owner:\s*([^.,\n]+)"
            applicant_matches_moreno = re.findall(applicant_regex, text_between_hearing_and_commission)

        # Extend the applicant_matches list with the matches found in the Moreno Valley text
        applicant_matches.extend(applicant_matches_moreno)

    if 'Eastvale' in text:
        # Use the specific regex for Eastvale
        eastvale_matches = re.findall(eastvale_regex, text)
        if eastvale_matches:
            eastvale_text = eastvale_matches[0][0]
            eastvale_planner_name = eastvale_matches[0][1]

            # Use a modified regex to exclude ', Eastvale Resident'
            applicant_regex = r'(?<=Planner:)\s*((?!,?\s*Eastvale\s*Resident)\b[A-Z][a-z]+\b)\s*(\b[A-Z][a-z]+\b)'
            applicant_matches_eastvale = re.findall(applicant_regex, eastvale_text)

            # Extract only the first group (name and last name) from each tuple
            applicant_matches_eastvale = [f"{name} {last_name}" for name, last_name in applicant_matches_eastvale]

            # Remove the Planner's name from the list of applicants (if present)
            applicant_matches_eastvale = [name for name in applicant_matches_eastvale if name != eastvale_planner_name]

            # Extend the applicant_matches list with the matches found in the Eastvale text
            applicant_matches.extend(applicant_matches_eastvale)

    unique_applicants = list(set(applicant_matches))
    filtered_applicants = [applicant for applicant in unique_applicants if applicant not in excluded_phrases]
    applicants = filtered_applicants or ['-']
    return applicants
