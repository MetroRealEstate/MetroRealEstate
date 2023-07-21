import re

def search_locations(text, max_locations=10):
    location_regex = r'Location:\s*(.*?)\s*[\n\r]'
    location_matches = re.findall(location_regex, text, re.I | re.M)
    site_regex = r'Project Site:\s*(.*?)\s*[\n\r]'
    site_matches = re.findall(site_regex, text, re.I | re.M)
    located_regex = r'located\s*at\s*([\w\d\s.-]+)'
    located_matches = re.findall(located_regex, text, re.I | re.M)
    located_on_regex = r'located on\s*([\w\d\s.-]+)'
    located_on_matches = re.findall(located_on_regex, text, re.I | re.M)
    located_in_regex = r'located in\s*([\w\d\s.-]+)'
    located_in_matches = re.findall(located_in_regex, text, re.I | re.M)

    locations = []
    location_count = 0

    for location in location_matches:
        if re.search(r'(\d+(\.\d+)?),\s*(\d+(\.\d+)?)', location):
            # If the location matches coordinates, add it to the locations list
            locations.append(location)
        else:
            # If the location doesn't match coordinates, check if it contains any name representing a physical place
            if re.search(r'\b[A-Za-z\s]+\b', location):
                locations.append(location)

        location_count += 1
        if location_count >= max_locations:
            break

    for location in site_matches:
        if re.search(r'(\d+(\.\d+)?),\s*(\d+(\.\d+)?)', location):
            # If the location matches coordinates, add it to the locations list
            locations.append(location)
        else:
            # If the location doesn't match coordinates, check if it contains any name representing a physical place
            if re.search(r'\b[A-Za-z\s]+\b', location):
                locations.append(location)

        location_count += 1
        if location_count >= max_locations:
            break

    for location in located_matches:
        if re.search(r'(\d+(\.\d+)?),\s*(\d+(\.\d+)?)', location):
            # If the location matches coordinates, add it to the locations list
            locations.append(location)
        else:
            # If the location doesn't match coordinates, check if it contains any name representing a physical place
            if re.search(r'\b[A-Za-z\s]+\b', location):
                locations.append(location)

        location_count += 1
        if location_count >= max_locations:
            break

    for location in located_on_matches:
        if re.search(r'(\d+(\.\d+)?),\s*(\d+(\.\d+)?)', location):
            locations.append(location)
        else:
            if re.search(r'\b[A-Za-z\s]+\b', location):
                locations.append(location)

        location_count += 1
        if location_count >= max_locations:
            break

    for location in located_in_matches:
        if re.search(r'(\d+(\.\d+)?),\s*(\d+(\.\d+)?)', location):
            locations.append(location)
        else:
            if re.search(r'\b[A-Za-z\s]+\b', location):
                locations.append(location)

        location_count += 1
        if location_count >= max_locations:
            break

    return list(set(locations)) if locations else ['-']
