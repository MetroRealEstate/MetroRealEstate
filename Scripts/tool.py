import re
from tkinter import ttk
import PyPDF2
from openpyxl import load_workbook, Workbook
from tkinter import Tk, Label, Button, filedialog
from tkinter.ttk import Progressbar
import time
import os
import pdfplumber
from functions.application_status import find_application_status
from functions.building_size import find_building_sizes
from functions.excluded_phrases import excluded_phrases
from functions.existing_use import find_existing_used
from functions.land_size import find_land_sizes
from functions.locations import search_locations
from functions.parcel_numbers import find_parcel_numbers
from functions.project_name import find_project_names
from functions.proposals import search_proposals
from functions.propose_zoning import find_propose_zoning
from functions.saveintemplate import save_in_template
from functions.aplicant_names import search_applicants
from functions.split_projects import split_projects
import webbrowser
import pytesseract
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

# Global variables
pdf_path = ''
pdf_name = ''
start_time = 0
# Function to search for the first date and project name in a PDF file and save them in Excel

cities_paterns = {
    'MORENO VALLEY': r'(?s)PUBLIC HEARING ITEMS\s+(.*?)STAFF COMMENTS',
    'EASTVALE': r'(?s)Project No\..*?Notes:',
    'CORONA': r'(?s)PUBLIC HEARINGS(.*?)WRITTEN COMMUNICATIONS',
    'COACHELA': r'(?s)PUBLIC HEARING CALENDAR \(QUASI-JUDICIAL\)(.*?)INFORMATIONAL:',
    'HEMET': r'(?s)PUBLIC HEARING(.*?)DEPARTMENT REPORTS',
    'INDIAN WELLS': r'(?s)PUBLIC HEARINGS(.*?)AYES',
    'LAKE ELSINORE': r'(?s)PUBLIC HEARING ITEM\(S\)(?=.*ID#)(.*?)BUSINESS ITEM\(S\)',
    'LA MIRADA': r'PUBLIC HEARING(.*?)MOTION CARRIED BY',
    'LA QUINTA': r'(?s)Project Information\s*\n(?=.*\bCASE NUMBER\b)(?=.*\bAPPLICANT\b)(?=.*\bREQUEST\b)(.*?)WEST:',
    'MALIBU': r'(?s)Continued Public Hearings(.*?)Old Business',
    'SAN GABRIEL': r'(?s)PUBLIC HEARING(.*?)COMMENTS FROM THE PLANNING MANAGER',
    'SANTA FE SPRINGS': r'(?s)PUBLIC HEARING(.*?)CONSENT ITEM',
    'WEST HOLLYWOOD': r'(?s)PUBLIC HEARINGS\.(.*?)NEW BUSINESS\.',
    'INDIO': r'PUBLIC HEARING ITEMS:(.*?)(?=ACTION ITEMS:)',
    'REDLANDS': r'(?s)\bRESOLUTION NO\.\s*([\s\S]*?)\bWHEREAS\b(?!.*\bWHEREAS\b)'
}


def search_data():
    global pdf_path, pdf_name, start_time

    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        # Create an Excel workbook and select the first sheet
        workbook = Workbook()
        sheet = workbook.active

        

        text = ""

        # Variables to store the results

        # Project Block
        project_block = [
            # {
            #     'meeting_type': '',
            #     'meeting_date': '',
            #     'project_names': '',
            #     'parcel_numbers': '',
            #     'project_locations': '',
            #     'building_sizes': '',
            #     'land_sizes': '',
            #     'application_status': '',
            #     'applicants': '',
            #     'proposals': ''
            # }
        ]

        # After extracting the text from the PDF

        for page in pdf.pages:
            text += page.extract_text()

        # If the extracted text is empty, use OCR
        if not text.strip():
            # Convert the PDF to images
            images = convert_from_path(pdf_path)
            text = ""

            # Perform OCR on each image
            for img in images:
                img_text = pytesseract.image_to_string(img, lang='eng')
                text += img_text + " "  # Concatenate text from all images

        # Find the city name in the text
        city_name = None
        for city, pattern in cities_paterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                city_name = city
                break

        if not city_name:
            lbl_message.config(text="City not recognized in the document.")
            # Set the city pattern to a default pattern that matches the entire text
            city_pattern = r'(?s).*'
        else:
            # Get the relevant pattern for the identified city
            city_pattern = cities_paterns[city_name]

        # Extract the relevant portion of the document based on the city's pattern
        city_text_matches = re.findall(
            city_pattern, text, re.IGNORECASE | re.DOTALL)
        if not city_text_matches:
            lbl_message.config(text=f"No relevant data found for {city_name}.")
            return

        # Combine all matches into a single string
        city_text = ' '.join(city_text_matches)

        # Check if the phrase "PLANNING COMMISSION" is present in any variant

        meeting_regex = r'PLANNING COMMISSION|Planning and Housing Commission'
        meeting_match = re.search(meeting_regex, text, re.I | re.M)
        if meeting_match:
            meeting_type = "Planning Commission Regular Meeting"
        else:
            meeting_type = "-"

        date_regex = r'\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}(?:st|nd|rd|th)?,? \d{2,4}\b|\b[A-Z]{3}\d{2}-\d{5}\b'

        # Find all dates in the PDF

        date = re.findall(date_regex, text)

        # Get the first date found in the document

        meeting_date = date[0] if date else '-'

        # Search for project names that match the regex based on the document content

        projects_substring = split_projects(city_text)
        
        for project in projects_substring:
            print(project)

            project_data = {}

            # Completar el resto del código para obtener los datos del proyecto
            
            project_data["meeting_type"] = meeting_type
            project_data["meeting_date"] = meeting_date
            project_data["project_names"] = ','.join(find_project_names(project))
            project_data["applicant"] = ','.join(search_applicants(project))
            project_data["project_locations"] = ','.join(search_locations(project))
            project_data["parcel_numbers"] = ','.join(find_parcel_numbers(project))
            project_data["building_sizes"] = ','.join(find_building_sizes(project))
            project_data["land_sizes"] = ','.join(find_land_sizes(project))
            proposals = search_proposals(project)
            project_data["captura"] = '; '.join(proposals) if proposals else '-'
            project_data["existing_used"] = ','.join(find_existing_used(project))
            project_data["propose_zoning"] = ','.join(find_propose_zoning(project))
            project_data["application_status"] = find_application_status(project)
            
            # Paso 3: Agrega el diccionario a la lista
            project_block.append(project_data)

        # Verificar si project_block está vacío y agregar un diccionario vacío si es necesario
        if not project_block:
            project_block.append({})

        # Write the results to Excel
        # Write headers in Excel
        for project in project_block:
            print(project)
        headers = list(project_block[0].keys())
        sheet.append(headers)
        # sheet['A2'] = meeting_type
        # sheet['B2'] = meeting_date
        # sheet['C2'] = '; '.join(project_names)
        # sheet['D2'] = ', '.join(applicants)
        # sheet['E2'] = '; '.join(project_locations)
        # sheet['F2'] = '; '.join(parcel_numbers)
        # sheet['G2'] = '; '.join(building_sizes)
        # sheet['H2'] = '; '.join(land_sizes)
        # sheet['I2'] = captura
        # sheet['J2'] = '; '.join(existing_used)
        # sheet['K2'] = '; '.join(propose_zoning)
        # sheet['L2'] = application_status
        for item in project_block:
            row_data = list(item.values())
            sheet.append(row_data)
        # Save the Excel file

        excel_path = f'{pdf_name}_results.xlsx'
        workbook.save(excel_path)

        # Save the data in the first empty row of the "COPIA PLANTILLA" file

        # Create a list with the collected data

      
        # data = [
        #     meeting_type,
        #     meeting_date,
        #     '; '.join(project_names),
        #     '; '.join(applicants),
        #     '; '.join(project_locations),
        #     '; '.join(parcel_numbers),
        #     '; '.join(building_sizes),
        #     '; '.join(land_sizes),
        #     '; '.join(proposals),
        #     '; '.join(existing_used),
        #     '; '.join(propose_zoning),
        #     application_status,
        # ] 

        # Call the function to save the data in the excel template

        #save_in_template(data, 'COPIA PLANTILLA.xlsx')

        # Display completion message and total execution time
        lbl_message.config(
            text=f'The search has been finished. Total time: {time.time() - start_time:.2f} segundos')

        # Open the Excel file after saving
        os.startfile(excel_path)

    #    # Display results in the console
    #     print(f"Meeting Type: {meeting_type}")
    #     print(f"Meeting Date: {meeting_date}")
    #     print(f"Project Names: {project_names}")
    #     print(f"Applicants: {applicants}")
    #     print(f"Project Locations: {project_locations}")
    #     print(f"Parcel Numbers: {parcel_numbers}")
    #     print(f"Building Sizes: {building_sizes}")
    #     print(f"Land Sizes: {land_sizes}")
    #     print(f"Proposals: {proposals}")
    #     print(f"Application Status: {application_status}")
    #     print(f"Existing / Used: {existing_used}")
    #     print(f"Propose Zoning: {propose_zoning}")
    #     print(f"template text {city_text}")
    #     print("Results saved to Excel file.")

    

    # Enable the search button after completing the task
    btn_search.config(state='normal')

# Function to select a PDF file


def select_pdf():
    global pdf_path, pdf_name, start_time, lbl_message

    # Open the file selection dialog
    pdf_path = filedialog.askopenfilename(filetypes=[('PDF Files', '*.pdf')])

    # Get the name of the selected PDF file
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Disable the search button while the task is running
    btn_search.config(state='disabled')

    # Display start search message
    lbl_message.config(text='Searching data in the file...')

    # Save the start time of execution
    start_time = time.time()

    # Call the function to search for data in the PDF file
    search_data()


def open_documentation():
    url = "https://kyrkematias.github.io/Metro-Data-Tool-Doc/"
    webbrowser.open_new(url)


# GUI configuration
root = Tk()
root.title('Data Tool')
root.geometry('400x250')
root.configure(bg='white')

# Documentation link label with hyperlink
style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 12), background='white')
style.configure('TButton', font=('Helvetica', 14, 'bold'),
                background='#007BFF', foreground='white')

lbl_instructions = ttk.Label(root, text='Select a PDF file:')
lbl_instructions.pack(pady=30)

btn_search = ttk.Button(root, text='Search', command=select_pdf)
btn_search.pack()
style.configure('TButton', foreground='#555555')

lbl_message = ttk.Label(root, text='')
lbl_message.pack(pady=20)

lbl_documentation = Label(root, text="For more information read the Documentation",
                          fg="blue", cursor="hand2", underline=270, font=('Verdana', 10))
lbl_documentation.pack(pady=5)
lbl_documentation.bind("<Button-1>", lambda e: open_documentation())

root.mainloop()
