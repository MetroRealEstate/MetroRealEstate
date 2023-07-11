# PDF Data Search Tool

The PDF Data Search Tool is a script that allows you to extract specific data from a PDF file and store it in an Excel spreadsheet. It provides a graphical user interface (GUI) for easy interaction.

## Features

1. __Select PDF File:__  The tool allows you to select a PDF file using a file dialog.

2. __Search Data:__ The tool searches for specific data within the selected PDF file, including meeting type, meeting date, project names, applicants, project locations, parcel numbers, building sizes, land sizes, proposals, existing/used information, propose zoning, and application status.

3. __Save Results:__ The extracted data is saved in an Excel spreadsheet. The tool creates a new workbook and writes the data to the first sheet. The Excel file is saved with the name "{PDF file name}_results.xlsx".

4. __Save Data in Template:__ The extracted data is also saved in a pre-defined template file named "COPIA PLANTILLA.xlsx". The data is appended to the first available row in the template.

5. __Save Data to MongoDB:__ The extracted data is saved to a MongoDB database using the provided `save_data_to_mongodb` function from the `db` module.

6. __Display Results:__ The tool displays the extracted data in the console for easy verification.

## Usage

1. Make sure you have the necessary dependencies installed: `re`, `PyPDF2`, `openpyxl`, `tkinter`, `pdfplumber`, and a MongoDB client.

2. Ensure that you have the following additional files in the same directory as the script:

* * `excluded_phrases.py`: Contains a list of excluded phrases for applicant names.
* * `saveintemplate.py`: Contains the `save_in_template` function for saving data in the template file.
* * `db.py`: Contains the `save_data_to_mongodb` function for saving data to MongoDB.

3. Run the script using a Python interpreter.

4. The graphical user interface (GUI) will appear.

5. Click the Search button to select a PDF file.

6. The tool will search for the specified data within the PDF file and display the results in the console.

7. The extracted data will be saved in an Excel spreadsheet named "{PDF file name}_results.xlsx".

8. The extracted data will also be appended to the template file "COPIA PLANTILLA.xlsx".

9. The extracted data will be saved to the MongoDB database using the provided `save_data_to_mongodb` function.

10. After the process is complete, a message will be displayed in the GUI with the total execution time.

11. The Excel file will automatically open after saving.

## Additional Information

* The script uses regular expressions to search for specific patterns in the extracted text from the PDF file.

* The script assumes a specific format for the data, such as date formats, project name formats, parcel number formats, etc. Ensure that the PDF files being processed adhere to these formats for accurate results.

* The script relies on the availability and accuracy of the data within the PDF file. Inaccurate or missing data may lead to incorrect or incomplete results.

* The script includes pre-defined phrases that are excluded from the applicant names. Modify the `excluded_phrases.py` file to adjust the list of excluded phrases according to your requirements.

* The script uses the `pdfplumber` library to extract text from PDF files. Ensure that you have the library installed or install it using `pip install pdfplumber`.

* The script requires a MongoDB client to be installed and a MongoDB database connection to be set up. Modify the `save_data_to`.

# The importance of saving the data in 3 files

The tool has been designed to store data in three different locations: 2 Excel files and a MongoDB database. This choice is based on the advantages and specific uses of each of these technologies.

The custom Excel file, generated using a predefined template, is ideal for storing data in a structured and easily accessible format. Using an Excel file allows for straightforward manipulation of the data, as it can be opened and modified using widely available applications such as _Microsoft Excel_ or _Google Sheets_. Additionally, the Excel file can be conveniently shared and distributed, facilitating collaboration and information exchange with other users.

On the other hand, the _MongoDB database_ offers a scalable and flexible solution for data storage. MongoDB is a __document-oriented NoSQL database__, which means it can store data in a _JSON-like_ format called _BSON_. This allows for storing data with a more flexible and dynamic structure, which is particularly useful when the data can vary in format or schema over time.

Using MongoDB also enables access and querying of the data through an _API_. By utilizing __MongoDB queries__, advanced searches and filters can be performed on the stored data. This provides the ability to perform analysis and obtain specific information based on user requirements.

In summary, the choice to store data in a custom _Excel_ file and a _MongoDB_ database, with access through an _API_, provides a powerful combination of structured storage and flexibility. The _Excel_ file allows for easy and accessible manipulation of the data, while the _MongoDB_ database enables scalable storage and advanced queries through an _API_. This allows users to leverage the strengths of both technologies to make the most out of the data generated by the tool.

## Tasks

* Add multiple formats for project names
* Improve recognition of applicant names to include only those within a project
* Enhance proposal collection to capture complete text
* Create a detector to determine if the land is vacant or occupied, and specify the occupation if not vacant
* Improve "Existing Used" detection. Currently, it doesn't detect when it's vacant.



* Incorporate all verified and translated changes into tool.py
* Package the script for use as an application


# Notes:

- Some patterns of applicants with uppercase words are not recognized by the model. Some company names or real people's names that begin with a title, such as 'D.R. John,' are not recognized.
- Some locations may be incomplete or lack reference
- Some 'Building Size' and 'Land Size' values are not recognized by the model, despipassing the RegEx recognition tests
- The 'Current Application Status' only recognizes when the document specifies 'Accepted' or 'Rejected'.
- The propose zone only recognizes when the document specifies it. Still needs validation.
- Project location in Lake Elsinore only appears in this format 'APNS 381-320-020 AND 023' in the files. Probably need manual validation.
- The tool __only collect data if it's__ specified in the document





