import re
from functions.excluded_phrases import excluded_phrases

def search_applicants(city_text):
    moreno_matrix = r'(?s)(?<=PUBLIC HEARING ITEMS).*?(?=OTHER COMMISSION BUSINESS)'
    eastvale_regex = r'Planner:\s*([A-Z][a-z]+(?: [A-Z][a-z]+)?)\s*Notes:'
    # Search for applicant names
    applicant_regex = r"Applicant: ([A-Z][a-z]+ [A-Z][a-z]+)"
    applicant_matches = re.findall(applicant_regex, city_text, re.I | re.M)
    if not applicant_matches:
        applicant_regex = r"Applicant:\s(?:([A-Z][a-z]+(?:\s[A-Z]\.\s?[A-Z][a-zA-Z]+)+|[A-Z][a-zA-Z]+))" #Ex: Applicant: Gregorio C. Cervantes
        applicant_matches = re.findall(applicant_regex, city_text)
    if not applicant_matches:
        applicant_regex = r"\b[A-Z][a-z]+ [A-Z][a-z]+\b(?:\sDevelopment Group)?"
        applicant_matches = re.findall(applicant_regex, city_text)
    if not applicant_matches:
        applicant_regex = r"Owner:\s*([^.,\n]+)"
        applicant_matches = re.findall(applicant_regex, city_text, re.I | re.M)
    if not applicant_matches:
        applicant_regex = r'Planner: ([A-Z][a-z]+ [A-Z][a-z]+)'

    if 'Moreno Valley' in city_text:
        # Extract the text between 'PUBLIC HEARING ITEMS' and 'OTHER COMMISSION BUSINESS'
        text_between_hearing_and_commission_match = re.search(moreno_matrix, city_text)
        if text_between_hearing_and_commission_match:
            text_between_hearing_and_commission = text_between_hearing_and_commission_match.group(0)
        else:
            text_between_hearing_and_commission = ""

        # Search for applicant names within the extracted text
        applicant_matches_moreno = re.findall(applicant_regex, text_between_hearing_and_commission, re.I | re.M)
        if applicant_matches_moreno:
            # Extend the applicant_matches list with the matches found in the Moreno Valley text
            applicant_matches.extend(applicant_matches_moreno)

    if 'Eastvale' in city_text:
        # Use the specific regex for Eastvale
        eastvale_matches = re.findall(eastvale_regex, city_text, re.M)
        if eastvale_matches:
            eastvale_text = eastvale_matches[0]

            # Use a modified regex to extract the applicant name after 'Planner:'
            applicant_regex = r'Planner:\s*([A-Z][a-z]+(?: [A-Z][a-z]+)?)\s*Notes:'
            applicant_match = re.search(applicant_regex, eastvale_text)

            # Check if the applicant name is found and add it to the list of applicant matches
            if applicant_match:
                eastvale_planner_name = applicant_match.group()
                applicant_matches.append(eastvale_planner_name)

    unique_applicants = list(set(applicant_matches))
    filtered_applicants = [applicant for applicant in unique_applicants if applicant not in excluded_phrases]
    applicants = filtered_applicants or ['-']
    return applicants
