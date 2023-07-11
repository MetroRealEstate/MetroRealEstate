# PDF Applicant Name Extractor

This Python script extracts applicant names from a PDF file and filters out non-person or non-company names. It utilizes the `nameparser` library to parse and validate the names.

## Prerequisites

- Python 3.5 or above
- Required Python packages: `nameparser`

## Installation

1. Make sure you have Python 3.5 or above installed on your system.
2. Install the required Python package by running the following command:

`pip install PyPDF2`
`pip install nameparser`


## Usage

1. Place your PDF file in the same directory as the script.
2. Open the script file (`script.py`) and modify the following variables if needed:

- `applicant_regex`: The regular expression pattern to match applicant names. You can customize this pattern according to your specific needs.
- `pdf_file_path`: The path to your PDF file. Update this variable with the name of your PDF file.

3. Run the script by executing the following command: `python script.py`


4. The script will extract the applicant names from the PDF file and display the filtered names in the console.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments




