import re

def find_parcel_numbers(text):
    # Regex pattern to match parcel numbers in the format "###-###-###"
    parcel_number_regex = r"\d\d\d-\d\d\d-\s?\d\d\d|(APNs?:\s*\d+(?:-\d+)+)|(APN.?s?\s*\d+(?:-\d+)+)|(Assessor’s Parcel Number\s*\d+(?:-\d+)+)|\b(?:Assessor’s\s+)?Parcel\s+Number:\s*(\d(?:\s*-?\s*\d+)*(?:\s*and\s*\d(?:\s*-?\s*\d+)*)*)\b|\bAssessor\s*Parcel\s*Number:\s*(\d+-\d+-\d+)\b|\bAPN\s*(\d+-\d+-\d+)\b|Assessor’s Parcel Number ((?:\d+-\n)*\d+-\d+)|(APN?\s#\s*\d+(?:-\d+)+)|APN:\s*((?:\d{3}‐\d{3}‐\d{3}(?:,\s*|\s+and\s+))+\d{3}‐\d{3}‐\d{3})"
    parcel_number_matches = re.findall(parcel_number_regex, text)

    if not parcel_number_matches:
        # Check for Tract number format "Tract Map ###"
        pattern = r"Tract(?:\s+Map)?\s+(\d+)"
        match = re.search(pattern, text, re.I)
        if match:
            tract_number = match.group(1)
            parcel_numbers = ['Tract No. ' + tract_number]
        else:
            # Use \d{4}-\d{3}-\d{3} pattern to find parcel numbers in "APN: ###-###-###" format
            parcel_number_regex = r"APN:([\s\S]*?)\d{4}-\d{3}-?\s?\d{3}"
            parcel_number_matches = re.findall(parcel_number_regex, text, re.M)
            if parcel_number_matches:
                parcel_numbers = list(set(parcel_number_matches))
            else:
                parcel_numbers = ["-"]
    else:
        parcel_numbers = list(set(parcel_number_matches))
    
    # Convert any tuples in parcel_numbers to strings
    parcel_numbers = [str(item).replace("('", "").replace("', '", "").replace("')", "") for item in parcel_numbers]

    return parcel_numbers
