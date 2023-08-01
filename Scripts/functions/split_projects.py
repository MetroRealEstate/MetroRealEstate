import re

def split_projects(city_text):
    corona_project_pattern = r'(?si)PUBLIC HEARING(.*?)(?:Attachments|OTHER COMMISSION BUSINESS)'
    #REVISAR POR QUÉ NO FUNCIONA
    moreno_project_pattern = r'Case: .+?(?=\n\d+\. |Case:|\Z)' 
    eastvale_project_pattern = r'Project No\..*?(.*?)Notes:'
    blythe_project_pattern = r'(?s)TENTATIVE PARCEL MAP \d+\.(.*?)(?:Tentative Parcel Map \d+\.|CONTINUED BUSINESS:)'
    projects_matches = []
    print("City text: " + city_text)

    if "Council District" in city_text or "Moreno Valley" in city_text:
        project_pattern = moreno_project_pattern
    elif "corona" in city_text.lower():
        project_pattern = corona_project_pattern
    elif "Eastvale" in city_text:
        project_pattern = eastvale_project_pattern
    elif "BLYTHE" in city_text:
        project_pattern = blythe_project_pattern
    else:
        return projects_matches
    
    matches = re.findall(project_pattern, city_text, re.IGNORECASE | re.DOTALL)
    projects_matches.extend(matches)
    projects_matches = list(set(projects_matches)) if projects_matches else ['-']
    print("Project Matches: " + str(projects_matches))
    
    return projects_matches
