""" The Pdf to Docx converter method"""
from pdf2docx import parse


def pwConverter(pdfFile, docxName):
    """ Converts Pdf to Docx.
    Arg:
        pdfFile:pdf file to be converted
        docxName: The name of the new docx file

    Returns:
        File converted
    """
    parse(pdfFile, docxName)
    return
