import re

def find_parcel_numbers(text):
    # Regex pattern to match parcel numbers in the format "###-###-###"
    parcel_number_regex = r"\d\d\d-\d\d\d-\s?\d\d\d"
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
                parcel_numbers = []
    else:
        parcel_numbers = list(set(parcel_number_matches))

    return parcel_numbers
