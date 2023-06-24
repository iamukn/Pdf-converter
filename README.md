PDF TO WORD AND WORD TO PDF CONVERTER
=======================================

This web application aims to provide a seamless means of conversion of documents from pdf to docx and vice versa
Our long term goal is to provide an open source solution to document conversion across various file formats and extensions

Author
========
Ndukwe, Ukaegbu Kingsley <n.u.kingsley@gmail.com>

HOW TO USE
============================================

To use this application, simply run the app.py python file which will serve the html on your local host port 5000

You'll need to modify the SQL functionality of the db.py file located in the Py_files directory with the necessary SQL information and desired database name.

After the flask app runs, you can now surf the web pages using localhost:5000

Running on an Application server (Gunicorn)
=======================================================
To run this app via an application server, you have to run the "run.sh" shell script using "./run.sh"
The app will create a gunicorn instance which will listen on port 5000


