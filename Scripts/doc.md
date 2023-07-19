# PDF Metro Data Tool

The PDF Metro Data Tool is a script that allows you to extract specific data from a PDF file and store it in an Excel spreadsheet. It provides a graphical user interface (GUI) for easy interaction.

## Features

1. **Select PDF File:** The tool allows you to select a PDF file using a file dialog.

2. **Search Data:** The tool searches for specific data within the selected PDF file, including meeting type, meeting date, project names, applicants, project locations, parcel numbers, building sizes, land sizes, proposals, existing/used information, propose zoning, and application status.

3. **Save Data in Template:** The extracted data is also saved in a pre-defined template file named "COPIA PLANTILLA.xlsx". The data is appended to the first available row in the template.

4. **Display Results:** The tool displays the extracted data in the console for easy verification.

## Usage

1. The executable file already have the necessary dependencies installed: `re`, `PyPDF2`, `openpyxl`, `tkinter`, `pdfplumber`.

2. Ensure that you have the following additional files in the same directory as the script:
   - `COPIA PLANTILLA.xlsx` template file.

3. Run the script using the executable file.

4. The graphical user interface (GUI) will appear.

5. Click the Search button to select a PDF file. This tool only grabs information from PDF files with selectable text inside. You can only select one file at a time. If you need to analyze multiple files, wait until the data collection is done.

6. The tool will search for the specified data within the PDF file and display the results in the console.

7. The extracted data will be appended to the template file "COPIA PLANTILLA.xlsx".

8. After the process is complete, a message will be displayed in the GUI with the total execution time.

9. You can use the tool again once the previous PDF is already done.

10. Validate or erase the information loaded in 'COPIA PLANTILLA' file.

## Additional Information

* The script uses regular expressions to search for specific patterns in the extracted text from the PDF file.

* The script assumes a specific format for the data, such as date formats, project name formats, parcel number formats, etc. Ensure that the PDF files being processed adhere to these formats for accurate results.

* The script relies on the availability and accuracy of the data within the PDF file. Inaccurate or missing data may lead to incorrect or incomplete results.

* The script includes pre-defined phrases that are excluded from the applicant names. Modify the `excluded_phrases.py` file to adjust the list of excluded phrases according to your requirements.

* The script uses the `pdfplumber` library to extract text from PDF files.

# Notes:

## There are some troubles you can find using this tool

- Some patterns of applicants with uppercase words are not recognized by the model. Some company names or real people's names that begin with a title, such as 'D.R. John,' are not recognized. Some documents may include a pattern in the redaction that this tool recognize as a name and surname, for example 'City Of'.

- Some locations may be incomplete or lack reference.

- Some 'Building Size' and 'Land Size' values are not recognized by the model, despipassing the RegEx recognition tests.

- The 'Current Application Status' only recognizes when the document specifies 'Accepted' or 'Rejected'.

- The propose zone only recognizes when the document specifies it. Still needs validation.

- The tool __only collect data if it's__ specified in the document. Using this tool dont't replace human validation.

- In some cities you need to use all the documents attached to the agenda and minutes to complement missing information. This tool can extract information of multiple documents (PDF only).

## Improvements for future versions:

- Enhancement in the filtering of relevant projects and their information (currently, data is collected indiscriminately, regardless of the size or importance of the project).
- Improvement in the algorithm for extracting applicant names (currently, there are phrases included as names due to the format).
- Enhancement in the extraction of project proposals (currently, some proposals are incomplete or not recognized due to their pattern within the document).
- Improvement in the extraction of project names (currently, all names that match the pattern are included in the results, regardless of their priority or size).
- Implementation of an automatic update system. This way, future updates with new improvements do not need to be downloaded manually.