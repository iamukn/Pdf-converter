""" The Pdf to Docx converter method"""
from pdf2docx import parse

def pwConverter(pdfFile, docxName):
    """ Converts Pdf to Docx.
    Arg:
        x:pdf file to be converted
        
    Returns:
        File converted
    """
    parse(pdfFile,docxName)
    return
