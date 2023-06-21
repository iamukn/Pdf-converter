from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import json

""" Creates and engine, a Session and also login to the \
        count table in mysql database """


with open('pword.txt', 'r') as p:
    password = p.read()
    pas = password.split('\n')

""" Creates an engine """


engine = create_engine("mysql://iamukn:{}@localhost/count".format(pas[0]),
                       echo=False)


""" Creates a session that binds to the engine"""
Session = sessionmaker(bind=engine)


""" Creates an instance of the Session """
session = Session()

Base = declarative_base()

"""Creates a table called 'visits' using the python Class """


class visits(Base):

    __tablename__ = "visits"
    # creates Id, site_visit and file_converts column
    id = Column(Integer, primary_key=True)
    site_visit = Column(Integer)
    file_converts = Column(Integer)

# pdfConverter = visits(site_visit=0, file_converts=0)
# session.add(pdfConverter)
# session.commit()
# Base.metadata.create_all(engine)


""" Queries the database & updates the visit count """


def visitCount(x="visits"):
    try:
        data = session.query(visits)
        """iterate through to increment the site visit data"""

        for i in data:
            if x == "visits":
                i.site_visit += 1
                session.commit()
                return

            elif x == "converts":
                i.file_converts += 1
                session.commit()
                return
            else:
                return ("internal error 404")
    except Exception:
        return "An increment error occured"


""" retrieving the convert counts and site visit from the databases"""


def counts():
    try:
        data = session.query(visits)
        """iterate through the file convert data from the table"""

        for i in data:
            # creates an object using the queried data
            res = {
                'Site_traffic': i.site_visit,
                'Total_converts': i.file_converts
                }
            return res
    except Exception:
        # Returns an error if the try block fails
        return "An increment error occured!!!"
