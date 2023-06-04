#!/usr/bin/python3
import subprocess

""" Converts docx files to pdf using the subprocess \
library which runs its command on the command line"""

def docxToPdf(docx_path, pdf_path):
    """Converts doc/docx to pdf
    Args:
        docx_path: Path to the MsWord file
        pdf_path: Path to save the Pdf file
    Return:
        Returns 0
    """
    subprocess.call(["unoconv", '-f', 'pdf', '-o', pdf_path, docx_path])
