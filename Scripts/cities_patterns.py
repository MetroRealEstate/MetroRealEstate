cities_paterns = {
    'MORENO VALLEY': r'(?s)PUBLIC HEARING ITEMS\s+(.*?)OTHER COMMISSION BUSINESS',
    'EASTVALE': r'(?s)Project No\.\s+(.*?)Notes:',
    'CORONA': r'(?s)PUBLIC HEARING\s+(.*?)That the Planning and Housing Commission',
    'COACHELA': r'(?s)PUBLIC HEARING CALENDAR \(QUASI-JUDICIAL\)(.*?)INFORMATIONAL:',
    'HEMET': r'(?s)PUBLIC HEARING(.*?)DEPARTMENT REPORTS',
    'INDIAN WELLS': r'(?s)PUBLIC HEARINGS(.*?)AYES',
    'LAKE ELSINORE': r'(?s)PUBLIC HEARING ITEM\(S\)(?=.*ID#)(.*?)BUSINESS ITEM\(S\)',
    'LA MIRADA': r'(?s)PUBLIC HEARING.*',
    'LA QUINTA': r'(?s)Project Information\s*\n(?=.*\bCASE NUMBER\b)(?=.*\bAPPLICANT\b)(?=.*\bREQUEST\b)(.*?)WEST:',
    'MALIBU': r'(?s)Continued Public Hearings(.*?)Old Business FLAGS GMI',
    'SAN GABRIEL': r'(?s)PUBLIC HEARING(.*?)COMMENTS FROM THE PLANNING MANAGER',
    'SANTA FE SPRINGS': r'(?s)PUBLIC HEARING(.*?)CONSENT ITEM',
    'WEST HOLLYWOOD': r'(?s)PUBLIC HEARINGS\.(.*?)NEW BUSINESS\.',
    'INDIO': r'PUBLIC HEARING ITEMS:(.*?)(?=ACTION ITEMS:)'
}