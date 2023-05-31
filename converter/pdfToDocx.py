""" The Pdf to Docx converter method"""
from pdf2docx import parse

def pwConverter(x, y):
    res = parse(x,y)
    return send_file(y, as_attachment=True)
