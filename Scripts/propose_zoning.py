import re

def find_propose_zoning(text):
    # Regex pattern to match propose zoning
    propose_zoning_regex = r'(?i)(?:\bremodel\b|(?!\b(?:proposal|PUBLIC HEARING)\b).*?\b(Construction|subdivide|Expansion|Merge|Remodel|remodel of|Subdivition(?:\s+and)?(?:\s+Construction)?|Development|Demolition(?:\s+and\s+construction)?)\b)'
    propose_zoning_matches = re.findall(propose_zoning_regex, text, re.I | re.S | re.M)
    propose_zoning = propose_zoning_matches if propose_zoning_matches else ['-']
    return propose_zoning
