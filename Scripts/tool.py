import re
import PyPDF2
from openpyxl import load_workbook, Workbook
from tkinter import Tk, Label, Button, filedialog
from tkinter.ttk import Progressbar
import time
import os
import pdfplumber
from application_status import find_application_status
from building_size import find_building_sizes
from excluded_phrases import excluded_phrases
from existing_use import find_existing_used
from land_size import find_land_sizes
from locations import search_locations
from parcel_numbers import find_parcel_numbers
from project_name import find_project_names
from proposals import search_proposals
from propose_zoning import find_propose_zoning
from saveintemplate import save_in_template
from aplicant_names import search_applicants
import webbrowser

# Global variables
pdf_path = ''
pdf_name = ''
start_time = 0
# Function to search for the first date and project name in a PDF file and save them in Excel

def search_data():
    global pdf_path, pdf_name, start_time 

    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        # Create an Excel workbook and select the first sheet
        workbook = Workbook()
        sheet = workbook.active

        # Write headers in Excel
        sheet['A1'] = 'Meeting type'
        sheet['B1'] = 'Meeting Date'
        sheet['C1'] = 'Project Name'
        sheet['D1'] = 'Applicant'
        sheet['E1'] = 'Project Location'
        sheet['F1'] = 'Parcel'
        sheet['G1'] = 'Building Size'
        sheet['H1'] = 'Land Size'
        sheet['I1'] = 'Propose Project'
        sheet['J1'] = 'Existing Used'
        sheet['K1'] = 'Propose Zoning'
        sheet['L1'] = 'Current Application Status'
        sheet['M1'] = 'Comments'

        # Variables to store the results
        meeting_type = ''
        meeting_date = ''
        project_names = []
        parcel_numbers = []
        project_locations = []
        building_sizes = []
        land_sizes = []
        application_status = ''
        applicants = []
        proposals = []

        meeting_type = ''

        # After extracting the text from the PDF
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

        # Check if the phrase "PLANNING COMMISSION" is present in any variant

        meeting_regex = r'PLANNING COMMISSION|Planning and Housing Commission'
        meeting_match = re.search(meeting_regex, text, re.I | re.M)
        if meeting_match: meeting_type = "Planning Commission Regular Meeting"
        else: meeting_type = "-"

        date_regex = r'\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}(?:st|nd|rd|th)?,? \d{2,4}\b|\b[A-Z]{3}\d{2}-\d{5}\b'

        # Find all dates in the PDF

        all_dates = re.findall(date_regex, text)

        # Get the first date found in the document

        meeting_date = all_dates[0] if all_dates else '-'

        # Search for project names that match the regex based on the document content

        project_names = find_project_names(text)

        # Search for parcel information in the format "{###-###-###}"

        parcel_numbers = find_parcel_numbers(text)

        # Search for all locations that match coordinates or any name in any format representing a physical place

        project_locations = search_locations(text)                   

        # Search for the application status ("Approved" or "Approval") in any format or variation

        application_status = find_application_status(text)

        #Search for applicants names

        applicants = search_applicants(text, excluded_phrases)

        # Search for building size with the format if not found in the previous format

        building_sizes = find_building_sizes(text)

        # Search for land sizes in acres with the formats "2.6 acre", "33.57-acre", or "18.49- acre site"

        land_sizes = find_land_sizes(text)

        # Search for proposals after "Proposal" and save the text until the first period

        proposals = search_proposals(text)

        captura = proposals[0] if proposals else '-'

        # Search for existing use

        existing_used = find_existing_used(text)

        # Search for propose zoning

        propose_zoning = find_propose_zoning(text)

        # Write the results to Excel

        sheet['A2'] = meeting_type
        sheet['B2'] = meeting_date
        sheet['C2'] = '; '.join(project_names)
        sheet['D2'] = ', '.join(applicants)
        sheet['E2'] = '; '.join(project_locations)
        sheet['F2'] = '; '.join(parcel_numbers)
        sheet['G2'] = '; '.join(building_sizes)
        sheet['H2'] = '; '.join(land_sizes)
        sheet['I2'] = '; '.join(proposals)
        sheet['J2'] = '; '.join(existing_used)
        sheet['K2'] = '; '.join(propose_zoning)
        sheet['L2'] = application_status

        # Save the Excel file

        excel_path = f'{pdf_name}_results.xlsx'
        workbook.save(excel_path)

        # Save the data in the first empty row of the "COPIA PLANTILLA" file

        # Create a list with the collected data

        data = [
            meeting_type,
            meeting_date,
            '; '.join(project_names),
            '; '.join(applicants),
            '; '.join(project_locations),
            '; '.join(parcel_numbers),
            '; '.join(building_sizes),
            '; '.join(land_sizes),
            '; '.join(proposals),
            '; '.join(existing_used),
            '; '.join(propose_zoning),
            application_status,
        ]

        #Call the function to save the data in the excel template
        
        save_in_template(data, 'COPIA PLANTILLA.xlsx')

        # Display completion message and total execution time
        lbl_message.config(
            text=f'The search has been finished. Total time: {time.time() - start_time:.2f} segundos')

        # Open the Excel file after saving
        os.startfile(excel_path)

       # Display results in the console
        print(f"Meeting Type: {meeting_type}")
        print(f"Meeting Date: {meeting_date}")
        print(f"Project Names: {project_names}")
        print(f"Applicants: {applicants}")
        print(f"Project Locations: {project_locations}")
        print(f"Parcel Numbers: {parcel_numbers}")
        print(f"Building Sizes: {building_sizes}")
        print(f"Land Sizes: {land_sizes}")
        print(f"Proposals: {proposals}")
        print(f"Application Status: {application_status}")
        print(f"Existing / Used: {existing_used}")
        print(f"Propose Zoning: {propose_zoning}")
        print("Results saved to Excel file.")

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
root.geometry('300x150')


# Documentation link label with hyperlink

lbl_instructions = Label(root, text='Select a PDF file:')
lbl_instructions.pack(pady=10)

btn_search = Button(root, text='Search', command=select_pdf)
btn_search.pack()

lbl_message = Label(root, text='')
lbl_message.pack(pady=10)

lbl_documentation = Label(root, text="For more information read the Documentation", fg="blue", cursor="hand2", underline=270)
lbl_documentation.pack(pady=5)
lbl_documentation.bind("<Button-1>", lambda e: open_documentation())

root.mainloop()