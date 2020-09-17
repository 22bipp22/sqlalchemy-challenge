import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/enter start date as yyyy-mm-dd<br/>"
        f"/api/v1.0/enter start date as yyyy-mm-dd/enter end date as yyyy-mm-dd"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation values"""
    # Query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

 # Create a dictionary from the row data and append to a list of all_prcp values
    all_prcps = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        
        all_prcps.append(prcp_dict)
    
    return jsonify(all_prcps)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station names"""
    # Query all Stations
    results = session.query(Station.station).all()

    session.close()
   
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the most active station"""
       
    station = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == station[0]).filter(Measurement.date > '2016-08-23').all()
    
    session.close()


    # session = Session(engine)

    

    # session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
   
    all_temps = list(np.ravel(results))

    return jsonify(all_temps)    


@app.route("/api/v1.0/<start_date>")
def calc_temps(start_date):
     
    # Returns:
    #     TMIN, TAVE, and TMAX
    # """
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date>=start_date).all()
    # return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    #     filter(Measurement.date >= '2017-08-20').all()
        
        #.filter(Measurement.date <= end_date).all()

    session.close()

   
    all_temps = list(np.ravel(results))

    return jsonify(all_temps)  

@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps2(start_date,end_date):
     
    # Returns:
    #     TMIN, TAVE, and TMAX
    # """
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date>=start_date).filter(Measurement.date<=end_date).all()
    # return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    #     filter(Measurement.date >= '2017-08-20').all()
        
        #.filter(Measurement.date <= end_date).all()

    session.close()

   
    all_temps = list(np.ravel(results))

    return jsonify(all_temps)  
if __name__ == '__main__':
    app.run(debug=True)
