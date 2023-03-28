from langchain.document_loaders import UnstructuredPowerPointLoader


def extract_text_from_pptx(pptx_file: str) -> str:
    """
    Function to extract text from pptx file
    Args:
        pptx_file (str): the filepath of pptx file
    Returns:
        pptx_text (str): the text in the pptx file
    """

    assert pptx_file.split(".")[-1] == "pptx"

    loader = UnstructuredPowerPointLoader(pptx_file)
    pages = loader.load()
    pptx_text = ""

    for page in pages:
        pptx_text += page.page_content + " "
    
    return pptx_text

