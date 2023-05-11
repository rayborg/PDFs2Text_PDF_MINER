#Converts all PDF files to text
import os
import glob
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def pdf_to_text(pdf_file, output_file):
    with open(pdf_file, 'rb') as file:
        parser = PDFParser(file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        
        with StringIO() as output_string:
            device = TextConverter(rsrcmgr, output_string, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
                
            extracted_text = output_string.getvalue()

        with open(output_file, 'w', encoding='utf-8') as output:
            output.write(extracted_text)

if __name__ == "__main__":
    papers_directory = 'Papers'

    # Create the output folder if it doesn't exist
    output_folder = 'TextPapers'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Iterate through all PDF files in the "Papers" directory
    for pdf_file in glob.glob(f"{papers_directory}/*.pdf"):
        # Derive output text file name from the PDF file name
        base_filename = os.path.splitext(os.path.basename(pdf_file))[0]
        output_file = os.path.join(output_folder, f"{base_filename}_output.txt")

        pdf_to_text(pdf_file, output_file)
