import re

def search_proposals(city_text):
    moreno_proposal_regex = r'(?:Proposal|Proposed Project|Proposal: |Proposed Project: )\b([^.:]*\d+(?:\.\d+)?[^.]*)\.'
    moreno_alt_regex = r'Proposal (.+?(?=\n\d+\. |Case:|\Z))'
    corona_proposal_regex = r'\b[A-Za-z]?+\d+(?:[-.]\d+)*\b\s*([^*]+?)\bApplicant:'
    elsinore_proposal_regex = r'\bID#\s\d{2}-\d{3}\b\s*((?:(?!(?:Attachments\b|.*\bcoronavirus\b)).)*)'
    hemet_proposal_regex = r'\b\d+\.[A-Z]\.(.*?)Recommendation:'
    stfe_proposal_regex = r'PUBLIC HEARING(?:(?!PUBLIC HEARING|CONSENT ITEM).)*'
    malibu_proposal_regex = r'Recommended Action:((?:(?!\().)*?)(?=\s*\([^)]*\)|(?:(?:\.\s*){4}))'
    gabriel_proposal_regex = r'The proposed project\s.([^\.]+\.[^\.]+\.[^\.]+\.[^\.]+(?:\.[^\.]+)?)'
    puente_proposal_regex = r'CONSIDERATION\s+(.*?)(?=\n\n|[A-Z]{2,})'
    blythe_proposal_regex = r'PUBLIC HEARING:(.*?\..*?\..*?\.)'
    eastvale_proposal_regex = r'Project\s*\n\s*Description:\s*(.*?)\s*\n\s*Planner:'
    redlands_proposal_regex = r'(?s)WHEREAS\b(.*?)\b(?=\nWHEREAS\b.*\nWHEREAS\b|$)'
    coachella_proposal_regex = r'(?s)(SUBJECT:.*?\bSTAFF RECOMMENDATION:)'

    proposals = re.findall(moreno_proposal_regex, city_text, re.S)
    
    if not proposals:
        moreno_alt_matches = re.findall(moreno_alt_regex, city_text, re.S | re.M | re.I)
        proposals = [match.strip() for match in moreno_alt_matches]
    if not proposals:
        corona_matches = re.findall(corona_proposal_regex, city_text, re.S | re.M)
        proposals = [match.strip() for match in corona_matches]
    if not proposals:
        proposals = [match.group(1).strip() for match in re.finditer(elsinore_proposal_regex, city_text, re.S | re.IGNORECASE) if 'coronavirus' not in match.group(1).lower()]
    if not proposals:
        coachella_matches = re.findall(coachella_proposal_regex, city_text, re.S | re.M)
        proposals = [match.strip() for match in coachella_matches]
    if not proposals:
        hemet_matches = re.findall(hemet_proposal_regex, city_text, re.S | re.M | re.I)
        proposals = [match.strip() for match in hemet_matches]
    if not proposals:
        stfe_matches = re.findall(stfe_proposal_regex, city_text, re.S | re.I | re.M | re.U)
        proposals = [match.strip() for match in stfe_matches]
    if not proposals:
        malibu_matches = re.findall(malibu_proposal_regex, city_text, re.S | re.I | re.M)
        proposals = [match.strip() for match in malibu_matches]
    
    if 'San Gabriel' in city_text:
        gabriel_matches = re.findall(gabriel_proposal_regex, city_text, re.I | re.M)
        proposals = [match.strip() for match in gabriel_matches]
    if 'La Puente' in city_text:
        puente_matches = re.findall(puente_proposal_regex, city_text, re.M)
        proposals = [match.strip() for match in puente_matches]
    if 'Blythe' in city_text:
        blythe_matches = re.findall(blythe_proposal_regex, city_text, re.M | re.S)
        proposals = [match.strip() for match in blythe_matches]
    if 'Eastvale' in city_text:
        eastvale_matches = re.findall(eastvale_proposal_regex, city_text, re.M)
        proposals = [match.strip() for match in eastvale_matches]
    if 'Redlands' in city_text:
        redlands_match = re.findall(redlands_proposal_regex, city_text)
        proposals = [match.strip() for match in redlands_match]
    

    # Función para verificar si las palabras 'demolish', 'build' o 'develop' están presentes en el resultado
    def check_keywords_in_proposal(proposal):
        keywords = ['demolish', 'build', 'develop']
        return any(keyword in proposal.lower() for keyword in keywords)

    # Excluir resultados que contengan las palabras 'cannabis' o 'signage' en cualquier forma (mayúsculas o minúsculas),
    # a menos que también se encuentren las palabras 'demolish', 'build' o 'develop' en el resultado.
    proposals = [proposal for proposal in proposals if ('cannabis' not in proposal.lower() and 'signage' not in proposal.lower()) or check_keywords_in_proposal(proposal)]

    return proposals if proposals else ['-']
