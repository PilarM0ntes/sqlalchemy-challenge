# Import Dependencies
import numpy as np
import datetime as dt
import sqlalchemy
import re
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from statistics import mean
from flask import Flask, jsonify

#####

#Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#####

# Flask setup
app = Flask(__name__)

# Flask routes:

# Home page: all routes available
@app.route("/")
def index():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2014-01-01<br/>"
        f"/api/v1.0/2015-03-01<br/>"
        f"/api/v1.0/2015-03-01/2016-03-01<br/>"
        f"/api/v1.0/2014-01-01/2015-01-01<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    prcp_dict = {'date':'precipitation'}
    for date, prcp in results:
        if prcp is not None:
            if float(prcp) != 0.0:
                prcp_dict[date] = prcp
    
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Get the stations information
    results = session.query(Station.station).all()
    session.close()

    # Return a JSON list of stations from the dataset.
    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query the dates and temperature observations of the most active station for the last year of data.
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
                group_by(Measurement.station).\
                order_by(func.count(Measurement.station).desc()).all()
    most_active = active_stations[0][0]
    max_date = session.query(func.max(Measurement.date)).\
            filter(Measurement.station == most_active).first()
    latest_date = dt.datetime.strptime(max_date[0], '%Y-%m-%d')
    start_date = latest_date.replace(day = latest_date.day -1, year = latest_date.year -1)
    
    final_query = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.station == most_active).\
            filter(Measurement.date > start_date).all()
    session.close()

    temp_list = [x[1] for x in final_query]
    # Return a JSON list of temperature observations (TOBS) for the previous year

    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def range_stats1(start):
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    #Check if the format is correct
    regex_pat = '^\d{4}-\d{2}-\d{2}'

    if re.search(regex_pat, start):
        # The format is valid
        # Create our session (link) from Python to the DB
        session = Session(engine)
        #Get the min and max dates
        min_date = session.query(Measurement.date).\
            group_by(Measurement.date).\
            order_by(Measurement.date.asc()).first()
        max_date = session.query(Measurement.date).\
            group_by(Measurement.date).\
            order_by(Measurement.date.desc()).first()
        #Checks if the entry date is in the database
        result = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date >= start).all()
        
        session.close()

        if len(result) == 0:
            # Return error if the date is not in the database
            return jsonify({"Error": f"Please enter a date [yyyy-mm-dd] that includes values within range: [{min_date[0]}] to [{max_date[0]}]"})
        else:
            print()
            temp_list = [float(x[1]) for x in result]
            temp_dict = {
                'a_response' : 'The temp stats for the given date range are:',
                'min_temp' : min(temp_list),
                'max_temp' : max(temp_list),
                'avg_temp' : round(mean(temp_list),2)
            }
            return jsonify(temp_dict)

    
    return jsonify({"Error": f"Entry format not valid: {start}. Please use yyyy-mm-dd"})

@app.route("/api/v1.0/<start>/<end>")
def range_stats2(start, end):
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    #Check if the format is correct
    regex_pat = '^\d{4}-\d{2}-\d{2}'

    if re.search(regex_pat, start) and re.search(regex_pat, end):
        # The format is valid
        # Create our session (link) from Python to the DB
        session = Session(engine)
        #Get the min and max dates within the database
        min_date = session.query(Measurement.date).\
            group_by(Measurement.date).\
            order_by(Measurement.date.asc()).first()
        max_date = session.query(Measurement.date).\
            group_by(Measurement.date).\
            order_by(Measurement.date.desc()).first()
        #Checks if the entry date is in the database
        result = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        
        session.close()

        if len(result) == 0:
            # Return error if the date is not in the database
            return jsonify({"Error": f"Please enter a date [yyyy-mm-dd] that includes values within range: [{min_date[0]}] to [{max_date[0]}]"})
        else:
            temp_list = [float(x[1]) for x in result]
            temp_dict = {
                'a_response' : 'The temp stats for the given date range are:',
                'min_temp' : min(temp_list),
                'max_temp' : max(temp_list),
                'avg_temp' : round(mean(temp_list),2)
            }
            return jsonify(temp_dict)


    return jsonify({"Error": f"Entry format not valid: {start} & {end}. Please use yyyy-mm-dd"})

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)