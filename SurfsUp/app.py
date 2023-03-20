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
        f"Precipitation:/api/v1.0/precipitation<br/>"
        f" Stations:/api/v1.0/stations<br/>"
        f"One Year Temperature:/api/v1.0/tobs<br/>"
        f"Temperature stat from the start date(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature stat from start to end dates(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    prcp = [Measurement.date,Measurement.prcp]
    queryresult = session.query(*prcp).all()
    session.close()

    precipitation = []
    for date, prcp in queryresult:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    stat = [Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation]
    queryresult = session.query(*stat).all()
    session.close()

    stations = []
    for station,name,lat,lon,elev in queryresult:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = elev
        stations.append(station_dict)

    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    lateststr = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latestdate = dt.datetime.strptime(lateststr, '%Y-%m-%d')
    querydate = dt.date(latestdate.year -1, latestdate.month, latestdate.day)
    dates = [Measurement.date,Measurement.tobs]
    queryresult = session.query(*dates).filter(Measurement.date >= querydate).all()
    session.close()

    tobs_all = []
    for date, tobs in queryresult:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobs_all.append(tobs_dict)

    return jsonify(tobs_all)

@app.route('/api/v1.0/<start>')
def start_date():
    session = Session(engine)
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()

    tobs_all1 = []
    for min,avg,max in query:
        tobs_dict1 = {}
        tobs_dict1["Min"] = min
        tobs_dict1["Average"] = avg
        tobs_dict1["Max"] = max
        tobs_all1.append(tobs_dict1)

    return jsonify(tobs_all1)

@app.route('/api/v1.0/<start>/<end>')
def start_end_date():
    session = Session(engine)
    query1 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= stop).all()
    session.close()

    tobs_all2 = []
    for min,avg,max in query1:
        tobs_dict2 = {}
        tobs_dict2["Min"] = min
        tobs_dict2["Average"] = avg
        tobs_dict2["Max"] = max
        tobs_all2.append(tobs_dict2)

    return jsonify(tobs_all2)

if __name__ == '__main__':
    app.run(debug=True)