import re
import PyPDF2
from openpyxl import load_workbook, Workbook
from tkinter import Tk, Label, Button, filedialog
from tkinter.ttk import Progressbar
import time
import os
import pdfplumber
from excluded_phrases import excluded_phrases
from saveintemplate import save_in_template
from db import save_data_to_mongodb

# Variables globales
pdf_path = ''
pdf_name = ''
start_time = 0

# Función para buscar la primera fecha y el nombre del proyecto en un archivo PDF y guardarlos en Excel


def buscar_datos_en_pdf():
    global pdf_path, pdf_name, start_time

    # Abrir el archivo PDF
    with pdfplumber.open(pdf_path) as pdf:
        # Crear un libro de Excel y seleccionar la primera hoja
        workbook = Workbook()
        sheet = workbook.active

        # Escribir encabezados en Excel
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
        sheet['M1'] = 'comments'

        # Variables para almacenar los resultados
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

        # Después de extraer el texto del PDF
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

        # Verificar si la frase "PLANNING COMMISSION" está presente en cualquier variante
        meeting_regex = r'PLANNING COMMISSION|Planning and Housing Commission'
        meeting_match = re.search(meeting_regex, text, re.I | re.M)
        if meeting_match: meeting_type = "Planning Commission Regular Meeting"
        else: meeting_type = "-"

        date_regex = r'\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}(?:st|nd|rd|th)?,? \d{2,4}\b'

        # Buscar todas las fechas en el PDF
        all_dates = re.findall(date_regex, text)

        # Obtener la primera fecha encontrada en el documento
        meeting_date = all_dates[0] if all_dates else '-'

        # Buscar los nombres de proyecto que coincidan con el regex según el contenido del documento
        if "Moreno Valley" in text:
            project_name_regex = r'PEN\d{2}-\d{4}'
        elif "City of Corona" in text or "Corona City" in text:
            project_name_regex = r'(?:PPM\d{4}-\d{4}|PM\s\d+|PP\d{4}-\d{4})|GPA\d{4}-\d{4}|CUP\d{4}-\d{4}'
        elif "City of Lake Elsinore" in text:
            project_name_regex = r'\d{4}-\d{2}'
        else:
            project_name_regex = r''  # Define un regex vacío si no se cumple ninguna condición

        project_name_matches = re.findall(project_name_regex, text)
        project_names = list(set(project_name_matches)) if project_name_matches else ['-']

        # Buscar la información de parcela en el formato "{###-###-###}"
        parcel_number_regex = r"\d\d\d-\d\d\d-\s?\d\d\d"
        parcel_number_matches = re.findall(parcel_number_regex, text)
        parcel_numbers = list(set(parcel_number_matches)) if parcel_number_matches else []

        # Buscar todas las ubicaciones que coincidan con coordenadas o cualquier nombre en cualquier formato que represente un lugar físico
        location_regex = r'Location:\s*(.*?)\s*[\n\r]'
        location_matches = re.findall(location_regex, text, re.I | re.M)
        site_regex = r'Project Site:\s*(.*?)\s*[\n\r]'
        site_matches = re.findall(site_regex, text, re.I | re.M)
        located_regex = r'located at\s*([\w\d\s.-]+)'
        located_matches = re.findall(located_regex, text, re.I | re.M)
        located_on_regex = r'located on\s*([\w\d\s.-]+)'
        located_on_matches = re.findall(located_on_regex, text, re.I | re.M)
        locations = []
        for location in location_matches:
            if re.search(r'(\d+(\.\d+)?),\s*(\d+(\.\d+)?)', location):
                # Si la ubicación coincide con coordenadas, se agrega a la lista de ubicaciones
                locations.append(location)
            else:
                # Si la ubicación no coincide con coordenadas, se verifica si contiene algún nombre que represente un lugar físico
                if re.search(r'\b[A-Za-z\s]+\b', location):
                    locations.append(location)

        for location in site_matches:
            if re.search(r'(\d+(\.\d+)?),\s*(\d+(\.\d+)?)', location):
                # Si la ubicación coincide con coordenadas, se agrega a la lista de ubicaciones
                locations.append(location)
            else:
                # Si la ubicación no coincide con coordenadas, se verifica si contiene algún nombre que represente un lugar físico
                if re.search(r'\b[A-Za-z\s]+\b', location):
                    locations.append(location)

        for location in located_matches:
            if re.search(r'(\d+(\.\d+)?),\s*(\d+(\.\d+)?)', location):
                # Si la ubicación coincide con coordenadas, se agrega a la lista de ubicaciones
                locations.append(location)
            else:
                # Si la ubicación no coincide con coordenadas, se verifica si contiene algún nombre que represente un lugar físico
                if re.search(r'\b[A-Za-z\s]+\b', location):
                    locations.append(location)

        for location in located_on_matches:
            if re.search(r'(\d+(\.\d+)?),\s*(\d+(\.\d+)?)', location):
                # Si la ubicación coincide con coordenadas, se agrega a la lista de ubicaciones
                locations.append(location)
            else:
                # Si la ubicación no coincide con coordenadas, se verifica si contiene algún nombre que represente un lugar físico
                if re.search(r'\b[A-Za-z\s]+\b', location):
                    locations.append(location)
                    
        project_locations = list(set(locations)) if locations else ['-']

        # Buscar el estado de la aplicación ("Approved" o "Approval") en cualquier formato o coincidencia
        application_status_regex = r'\b(APPROVED|APPROVAL)\b'
        application_status_match = re.search(application_status_regex, text)

        if application_status_match:
            application_status = "APPROVED"
        else:
            application_status = '-'

        # Buscar los nombres de solicitantes

        applicant_regex = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b(?:\sDevelopment Group)?'
        applicant_matches = re.findall(applicant_regex, text)
        applicants = list({match for match in applicant_matches if match not in excluded_phrases}) or ['-']

        # Buscar el tamaño del edificio con el formato si no se encuentra en el formato anterior
        building_size_regex = r'\(?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\)?\s*(SQUARES?\s*FEETS?|sq.\s*ft|SF|SQUARES?\s*FooTS?)'
        building_size_match = re.findall(building_size_regex, text, re.I)
        building_sizes = [
            size[0].strip('()') + ' SF' for size in building_size_match] if building_size_match else ['-']

        # Buscar los tamaños de tierra en acres en los formatos "2.6 acre", "33.57-acre" o "18.49- acre site"
        land_size_regex = r'(\d+(?:\.\d+)?)\s*(?:-)?\s*acre\s*(?:site)?'
        land_size_matches = re.findall(land_size_regex, text, re.I)
        land_sizes = [size + ' acre' for size in land_size_matches] if land_size_matches else ['-']

        # Buscar las propuestas después de "Proposal" y guardar el texto hasta el primer punto
        moreno_proposal_regex = r'(?:Proposal|Proposed Project|Proposal: |Proposed Project: )\b([^.:]*\d+(?:\.\d+)?[^.]*)\.'
        corona_proposal_regex = r'PUBLIC HEARING\s*-\s*([^*]+?)\bApplicant:'
        elsinore_proposal_regex = r'\bID#\s\d{2}-\d{3}\b\s*((?:(?!(?:Attachments\b|.*\bcoronavirus\b)).)*)'

        proposal_matches = re.findall(moreno_proposal_regex, text, re.S)
        if not proposal_matches:
            proposal_matches = re.findall(corona_proposal_regex, text, re.S)
        if not proposal_matches:
            proposal_matches = [match.group(1).strip() for match in re.finditer(elsinore_proposal_regex, text, re.S | re.IGNORECASE) if 'coronavirus' not in match.group(1).lower()]

        captura = proposal_matches[0] if proposal_matches else '-'
        proposals = proposal_matches if proposal_matches else ['-']

        # Buscar la disponibilidad del terreno

        existing_used = []
        # Buscar la palabra "existing" seguida de la frase completa hasta el primer punto
        existing_regex = r'(?i)\bexisting\b[^.]*'
        existing_matches = re.findall(existing_regex, text)
        existing_used = existing_matches if existing_matches else ['-']

        # Buscar las propuestas de zonificación
        propose_zoning_regex = r'(?i)\b(?:proposal|PUBLIC HEARING)\b.*?\b(Construction|subdivide|Expansion|Merge|Remodel|Subdivition(?:\s+and)?(?:\s+Construction)?|Development|Demolition(?:\s+and\s+construction)?)\b'
        propose_zoning_matches = re.findall(propose_zoning_regex, text, re.I | re.S | re.M)
        propose_zoning = propose_zoning_matches if propose_zoning_matches else '-'

        # Escribir los resultados en Excel
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

        # Guardar el archivo de Excel
        excel_path = f'{pdf_name}_results.xlsx'
        workbook.save(excel_path)

        # Guardar los datos en la primera fila libre del archivo "COPIA PLANTILLA"

        # Crear una lista con los datos recolectados

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

        # Llamada a la función para guardar en la plantilla de excel los datos

        save_in_template(data, 'COPIA PLANTILLA.xlsx')

        # Llamada a la función para guardar los datos en MongoBD

        save_data_to_mongodb({
            'meeting_type': meeting_type,
            'meeting_date': meeting_date,
            'project_names': project_names,
            'applicants': applicants,
            'project_locations': project_locations,
            'parcel_numbers': parcel_numbers,
            'building_sizes': building_sizes,
            'land_sizes': land_sizes,
            'proposals': proposals,
            'existing_used': existing_used,
            'propose_zoning': propose_zoning,
            'application_status': application_status
        })

        # Mostrar mensaje de finalización y tiempo total de ejecución
        lbl_mensaje.config(
            text=f'La búsqueda ha finalizado. Tiempo total: {time.time() - start_time:.2f} segundos')

        # Abrir el archivo Excel después de guardarlo
        os.startfile(excel_path)

        # Mostrar resultados en consola
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

    # Habilitar el botón de búsqueda después de completar la tarea
    btn_buscar.config(state='normal')

# Función para seleccionar un archivo PDF


def seleccionar_pdf():
    global pdf_path, pdf_name, start_time

    # Abrir el diálogo de selección de archivos
    pdf_path = filedialog.askopenfilename(filetypes=[('PDF Files', '*.pdf')])

    # Obtener el nombre del archivo PDF seleccionado
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Deshabilitar el botón de búsqueda mientras se ejecuta la tarea
    btn_buscar.config(state='disabled')

    # Mostrar mensaje de inicio de búsqueda
    lbl_mensaje.config(text='Buscando datos en el archivo PDF...')

    # Guardar el tiempo de inicio de ejecución
    start_time = time.time()

    # Llamar a la función para buscar los datos en el archivo PDF
    buscar_datos_en_pdf()


# Configuración de la interfaz gráfica
root = Tk()
root.title('Buscador de datos en PDF')
root.geometry('300x150')

lbl_instrucciones = Label(root, text='Seleccione un archivo PDF:')
lbl_instrucciones.pack(pady=10)

btn_buscar = Button(root, text='Buscar', command=seleccionar_pdf)
btn_buscar.pack()

lbl_mensaje = Label(root, text='')
lbl_mensaje.pack(pady=10)

root.mainloop()