#!/usr/bin/python3

""" Flask app to serve the converter """
from flask import Flask, render_template, request, send_file
from mimetypes import guess_type
from Py_files.db import visitCount, counts
from Py_files.pdfToDocx import pwConverter
from Py_files.msWord import docxToPdf
from Py_files.temp import temp_data
import requests
from time import ctime
from werkzeug.utils import secure_filename

"""instance of the Flask is created"""
app = Flask(__name__)

""" handles the Weather request from weatherapi
    The key is temporary and should be renewed
    to avoid code breaks
"""
# Holds the JSON data from the temp_data method
temperature = temp_data()
# Fetches the state name from the data
state = temperature['name']
# Fetches the temperature of the state
temp = temperature['main']['temp']
""" handles the 404 not found route"""


@app.errorhandler(404)
# A method that handles 404 errors and returns a 404.html as response
def not_found(e):

    return render_template("404.html", deg=temp, location=state)


""" Handles the get request from the '/' route"""


@app.route('/', methods=["GET"])
# A method that serves the landing page
def home():

    return render_template('home.html')


""" Handles the get request from the '/pdf' route"""


@app.route('/pdf', methods=["GET"])
# A method that serves the pdf to docx conversion page
def pdf():
    """Handles Visitors counts and convert counts"""
    # Increment the site visit count
    visitCount()
    # queries the database for the incremented data
    counter = counts()
    # gets the site_traffic data
    traffic = counter["Site_traffic"]
    # gets the total files converted data
    converts = counter["Total_converts"]
    # Returns an index.html with some datas to the client using jinja
    return render_template("index.html", deg=temp, location=state,
                           visits=traffic, convert=converts)


""" Handles the get request from the '/docx' route"""


@app.route('/docx', methods=["GET"])
# A method that serves the docx to pdf conversion page
def docx():
    # queries the database for the incremented data
    counter = counts()
    # gets the site visit traffic data
    traffic = counter["Site_traffic"]
    # gets the total_files converted data
    converts = counter["Total_converts"]
    # Returns a docx.html with some datas to the client using jinja
    return render_template("docx.html", deg=temp, location=state,
                           visits=traffic, convert=converts)


""" Handles the get request from the '/docx' route"""


@app.route('/about', methods=["GET"])
# A method that serves the about page
def about():
    # Queries the database for the incremented data
    counter = counts()
    # Gets the site visit traffic data
    traffic = counter["Site_traffic"]
    # Gets the total_files converted data
    converts = counter["Total_converts"]
    # Returns an about.html with some datas to the client using jinja
    return render_template("about.html", deg=temp, location=state,
                           visits=traffic, convert=converts)


""" Handles the get request from the '/about' route"""


@app.route('/donate', methods=["GET"])
# A method that serves the donate page
def donate():
    # queries the database for the incremented data
    counter = counts()
    # gets the site visit traffic data
    traffic = counter["Site_traffic"]
    # gets the total_files converted data
    converts = counter["Total_converts"]
    # returns an donate.html with some datas to the client using jinja
    return render_template("donate.html", deg=temp, location=state,
                           visits=traffic, convert=converts)


""" handles the post request from the pdf recieved"""


@app.route('/pdf2word', methods=['POST'])
# A method that receives the payload from client and converts pdf to docx
def convert():
    # checks to see if the method is a POST request
    if request.method == 'POST':
        # gets the file with a key pdf_file and assigns it to a variable
        pdf_file = request.files['pdf_file']
        # saves the assigned pdf file to the server using its secure filename
        pdf_file.save(secure_filename(pdf_file.filename))
        # gets the filename for verification
        verify = guess_type(secure_filename(pdf_file.filename))[0]
        file_name = secure_filename(pdf_file.filename)
        # creates a temporary docx filename which will
        # be given to the converted docx file
        new_name = secure_filename(pdf_file.filename).split('.pdf')
        rename = "{}.docx".format(new_name[0])

        # checks if the file received is a pdf file
        if verify == "application/pdf":
            """ handles the conversion to docx from pdf"""
            # handles the convertion of pdf to docx by passing
            # the filename and newname as arguments
            pwConverter(file_name, rename)
            # increments the conversion count on the database
            visitCount('converts')
            # returns the converted file to the client
            return send_file(rename)

        else:
            # return a pdf2doc.html informing the client
            # that "They should upload a valid pdf"
            return render_template("pdf2doc.html", deg=temp,
                                   pdf="upload a valid pdf", location=state)


""" Route that handles post requests for the conversion of docx to pdf"""


@app.route('/docx', methods=['POST'])
# Method that handles the docx to pdf conversion
def docx_convert():
    # Checks if the method is a POST method
    if request.method == 'POST':
        # Gets the file from the request with the key Pdf2Word
        word_file = request.files['Pdf2Word']
        # Checks to see if the file is a docx file
        verify = guess_type(word_file.filename)[0]
        if verify == "application/msword" or verify == "application/vnd.\
                openxmlformats-officedocument.wordprocessingml.document":
            # Saves the file to the server
            word_file.save(secure_filename(word_file.filename))
            # Gets the filename of the uploaded file
            file_name = secure_filename(word_file.filename)
            # Creates a new name with .pdf extension
            # which the converted file will inherit
            new_name = secure_filename(word_file.filename).split('.doc')
            rename = "{}.pdf".format(new_name[0])
            # A method that takes the filename and new name as argument
            # and converts the docx to pdf
            docxToPdf(file_name, rename)
            # Increments the conversion count on the database
            visitCount('converts')
            # Returns the converted file to the client
            return (send_file(rename))
        else:
            # Returns a doc2pdf.html page with a message
            # "Please upload a valid docx"
            return render_template('doc2pdf.html',
                                   pdf='Please upload a valid docx',
                                   deg=temp, location=state)


# Checks if the file is called by its name
if __name__ == "__main__":
    # Runs the app on port 5000
    app.run(debug=False, port=5000, host='0.0.0.0')
