import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route('/')
def homepage():
    return(
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> (Input a start date YYY-MM-DD)<br/>"
        f"/api/v1.0/<start>/<end> (Input start and end dates)"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    dict = {}
    last_prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').all()
    for tuple in last_prcp:
        dict[tuple[0]] = dict[tuple[1]]
    session.close()
    return jsonify(dict)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    session.close()
    return()

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    session.close()
    return()

@app.route('/api/v1.0/<start>')
def startdate():
    session = Session(engine)
    session.close()
    return()

@app.route('/api/v1.0/<start>/<end>')
def startenddate():
    session = Session(engine)
    session.close()
    return()

if __name__ == '__main__':
    app.run(debug=True)