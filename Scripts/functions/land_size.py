import re

def find_land_sizes(text):
    # Regex pattern to match land sizes
    land_size_regex = r'(\d+(?:[.,]\d+)?(?:±)?)\s*(?:-)?\s*acre\s*(?:site)?'
    land_size_matches = re.findall(land_size_regex, text, re.I)
    land_sizes = list(set([size + ' acre' for size in land_size_matches])) if land_size_matches else ['-']
    return land_sizes
