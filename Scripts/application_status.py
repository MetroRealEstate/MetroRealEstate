import re

def find_application_status(text):
    # Regex pattern to match application status ("APPROVED", "APPROVAL", or "APPROVE")
    application_status_regex = r'\b(APPROVED|APPROVAL|APPROVE)\b'
    application_status_match = re.search(application_status_regex, text, re.I)

    if application_status_match:
        application_status = "APPROVED"
    else:
        application_status = '-'

    return application_status
