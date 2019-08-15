from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt

# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

# reflect the table
Base.prepare(engine, reflect = True)

# Saving references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Creating our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all avaliable API routes"""
    return(
          f"Welcome to the Weather API!<br/>"
          f"Avaliable Routes:"
          f"/api/v1.0/precipitation<br/>"
          f"/api/v1.0/stations<br/>"
          f"/api/v1.0/tobs<br/>"
          f"/api/v1.0/<start><br/>"
          f"/api/v1.0/<start>/<end>")

@app.route("/api/v1.0/precipitation")
def percipitation():
    """Return a list of all passenger names"""
    session = Session(engine)
    date_prcp_query = session.query(Measurement.date, Measurement.prcp).all()
    prcp_list = []
    for date, prcp in date_prcp_query:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)


@app.route("/api/v1.0/station_names")
def station_names():
    """Return a list of all passenger names"""
    station_list = []
    station_names = session.query(Measurement.station).distinct().all()
    for x in station_names:
        station_dict = {}
        station_dict["Station Name"] = x
        station_list.append(station_dict)
    return jsonify(station_list)
    


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON of TObs for the previous year"""
    prev_year = dt.date(2017,8,23)- dt.timedelta(days=365)
    tobs_list = []
    date_prcp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date == prev_year).all()
    for tobs in date_prcp:
        tobs_dict = {}
        tobs_dict["TObs"] = tobs
        tobs_list.append(tobs_dict)  
    return jsonify(tobs_list)

@app.route("/api/v1.0/date/<start>/<end>")
def calc_temps(start, end):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX for dates between the start and end date inclusive.
    """
    start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    start_end_list = []
    for min_tobs, avg_tobs, max_tobs in start_end:
        start_end_dict = {}
        start_end_dict["TMIN"] = min_tobs
        start_end_dict["TAVG"] = avg_tobs
        start_end_dict["TMAX"] = max_tobs
        start_end_list.append(start_end_dict)
    return jsonify(start_end_list)

# CREATE A FILE FOR THE 
        
if __name__ == "__main__":
    app.run(debug=True)