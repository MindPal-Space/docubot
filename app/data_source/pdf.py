from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_file: str) -> str:
    """
    Function to get the text from a pdf file
    Args:
        pdf_file (str): the file path of the pdf file
    Returns:
        pdf_text (str): the text in the pdf file
    """
    
    assert pdf_file.split(".")[-1] == "pdf" #check the file path is pdf
    reader = PdfReader(pdf_file)
    pages = reader.pages
    pdf_text = ""
    
    for page in pages:
        pdf_text += page.extract_text() + " "

    return pdf_text