import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

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
def precipitation():
    """Return the precipitation data for the last year"""
    # Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()

    # Dict with date as the key and prcp as the value
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


@app.route("/api/v1.0/station_names")
def stations():
    """Return a list of stations."""
    results = session.query(Station.station).all()

    # Unravel results into a 1D array and convert to a list
    stations = list(np.ravel(results))
    return jsonify(stations)

    


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON of TObs for the previous year"""
    # Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
   # Query the primary station for all tobs from the last year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    
     # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))

    # Return the results
    return jsonify(temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    # Select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        # calculate TMIN, TAVG, TMAX for dates greater than start
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        # Unravel results into a 1D array and convert to a list
        temps = list(np.ravel(results))
        return jsonify(temps)

    # calculate TMIN, TAVG, TMAX with start and stop
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps)

        
if __name__ == "__main__":
    app.run(debug=True)