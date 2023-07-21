import re

def find_building_sizes(text):
    # Regex pattern to match building sizes
    building_size_regex = r'\(?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\)?\s*(SQUARES?\s*FEETS?|sq.\s*ft|SF|SQUARES?\s*FooTS?)'
    building_size_match = re.findall(building_size_regex, text, re.I)
    building_sizes = list(set([size[0].strip('()') + ' SF' for size in building_size_match])) if building_size_match else ['-']
    return building_sizes
