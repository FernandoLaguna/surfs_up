# import is datetime, NumPy, and Pandas
import datetime as dt
import numpy as np
import pandas as pd

#Add the SQLAlchemy dependencies 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#add the code to import the dependencies that we need for Flask.
from flask import Flask, jsonify

#set up our database engine for the Flask application
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#create a session link from Python to our database
session = Session(engine)

# Set Up Flask
app = Flask(__name__)

# define the welcome route
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#Create precipitation route
@app.route("/api/v1.0/precipitation")

#Next, we will create the precipitation() function
def precipitation():
    #add the line of code that calculates the date one year ago from the most recent date in the database
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   #write a query to get the date and precipitation for the previous year.
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
    # create a dictionary with the date as the key and the precipitation as the value
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

#we'll create a new function called stations()
@app.route("/api/v1.0/stations")
# create a query that will allow us to get all of the stations in our database
def stations():
    results = session.query(Station.station).all()
    # Next, we will convert our unraveled results into a list. To convert the results to a list, 
    # we will need to use the list function, which is list(), 
    # and then convert that array into a list. Then we'll jsonify the list and return it as JSON.
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# create the routes. ¿Por qué dos rutas?
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# add parameters to our stats()function: a start parameter and an end parameter
def stats(start=None, end=None):
    #create a query to select the minimum, average, and maximum temperatures from our SQLite database. We'll start by just creating a list called sel
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    # Since we need to determine the starting and ending date, add an if-not statement to our code. This will help us accomplish a few things. 
    # We'll need to query our database using the list that we just made. Then, we'll unravel the results into a one-dimensional array and convert them to a list.
    # ¿Para qué necesitamos este con if not?
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    #create our next query, which will get our statistics data. 
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)