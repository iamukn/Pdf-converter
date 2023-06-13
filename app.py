#!/usr/bin/python3

""" Flask app to serve the converter """
from flask import Flask, render_template, request, send_file
from mimetypes import guess_type
from Py_files.db import visitCount, counts
from Py_files.pdfToDocx import pwConverter
from Py_files.msWord import docxToPdf
import requests
from time import ctime
from werkzeug.utils import secure_filename

"""instance of the Flask is created"""
app = Flask(__name__)

""" handles the Weather request from weatherapi
    The key is temporary and should be renewed
    to avoid code breaks
"""
def weather():
    url = 'http://api.weatherapi.com/v1/current.json'
    key = '002cde86c6ee48209de205033230806'
    states = ["Lagos"]
    city = states[0]

    params = {
    "key":key,
    "q": "Lagos"
    }
    try:
        res = requests.get(url, params)
        body = res.json()
        return body
    except Exception:
        return "An error occured!"
state = weather()['location']['region']
temp = "{}°".format(weather()['current']['temp_c'])



""" handles the get request from the '/' route"""
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", deg=temp, location=state)

@app.route('/', methods=["GET"])
def home():

    """Landing page"""
    return render_template('home.html')

@app.route('/pdf', methods=["GET"])
def pdf():

    """Handles Visitors counts and convert counts"""
    visitCount()
    counter = counts()
    traffic = counter["Site_traffic"]
    converts = counter["Total_converts"]

    return render_template("index.html", deg=temp, location=state, visits=traffic, convert=converts)

""" Handles the get request from the '/docx' route"""
@app.route('/docx', methods=["GET"])
def docx():
    counter = counts()
    traffic = counter["Site_traffic"]
    converts = counter["Total_converts"]
    return render_template("docx.html", deg=temp, location=state, visits=traffic, convert=converts)


""" Handles the get request from the '/docx' route"""
@app.route('/about', methods=["GET"])
def about():
    counter = counts()
    traffic = counter["Site_traffic"]
    converts = counter["Total_converts"]
    return render_template("about.html", deg=temp, location=state, visits=traffic, convert=converts)

""" Handles the get request from the '/about' route"""
@app.route('/donate', methods=["GET"])
def donate():
    counter = counts()
    traffic = counter["Site_traffic"]
    converts = counter["Total_converts"]
    return render_template("donate.html", deg=temp, location=state, visits=traffic, convert=converts)

""" handles the post request from the pdf recieved"""

@app.route('/pdf2word', methods=['POST'])
def convert():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        pdf_file.save(secure_filename(pdf_file.filename))
        verify = guess_type(secure_filename(pdf_file.filename))[0]
        file_name = secure_filename(pdf_file.filename)
        new_name = secure_filename(pdf_file.filename).split('.pdf')
        rename = "{}.docx".format(new_name[0])

        if verify == "application/pdf":
            """ handles the conversion to docx from pdf"""

            pwConverter(file_name, rename)
            """ Handles the convert count increments """
            visitCount('converts')
            return send_file(rename)

        else:
            return render_template("pdf2doc.html", deg=temp, pdf="upload a valid pdf", location=state)

@app.route('/docx', methods=['POST'])
def docx_convert():
    if request.method == 'POST':
        word_file = request.files['Pdf2Word']
        verify = guess_type(word_file.filename)[0]
        if verify == "application/msword" or verify == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            word_file.save(secure_filename(word_file.filename))
            file_name = secure_filename(word_file.filename)
            new_name = secure_filename(word_file.filename).split('.doc')
            rename = "{}.pdf".format(new_name[0])
            docxToPdf(file_name, rename)
            visitCount('converts')
            return(send_file(rename))
        else:
            return render_template('doc2pdf.html',pdf='Please upload a valid docx', download='#', deg=temp, location=state)

if __name__ == "__main__":
    app.run(debug=False, port=5000, host='0.0.0.0')	
