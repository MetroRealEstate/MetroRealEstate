import re

def find_building_sizes(text):
    # Regex pattern to match building sizes
    building_size_regex = r'\(?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\)?\s*(SQUARES?\s*FEETS?|sq.\s*ft|SF|SQUARES?\s*FooTS?)|\b(\d+)\s*-?\s*unit\b|(\d{1,3}(?:,\d{3})+)(?:-(?:square\s*)-?foot)|\b(\d+\s*[-]?[\s-]*s\.f\.)|\(?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\)?\s*(?:square\s*)-?foot'
    building_size_match = re.findall(building_size_regex, text, re.I)
    building_sizes = []
    for size in building_size_match:
        for i in range(len(size)):
            if size[i]:
                if i == 0:
                    building_sizes.append(size[i].strip('()') + ' SF')
                elif i == 2:
                    building_sizes.append(size[i] + ' unit')

    return building_sizes if building_sizes else ['-']
