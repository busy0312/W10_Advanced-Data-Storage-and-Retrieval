import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"For the code belows, you can put start date in the end, such as 2010-08-01<br/>"
        f"/api/v1.0/<start><br/>"
        f"For the code belows, you can put start date and end date in the end, such as 2018-08-01/2019-01-01<br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
     # Create our session (link) from Python to the DB
    session=Session(engine)
    results=session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date).all()
    session.close()
    precp=[]
    for date,prcp in results:
        precp_dict={}
        precp_dict['date']=date
        precp_dict['precipitation']=prcp
        precp.append(precp_dict)

    return jsonify(precp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Station.station,Station.name,Station.latitude,Station.longitude).all()
    session.close()

     # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, name, latitude, longitude in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    last_year=dt.date(2017,8,23) - dt.timedelta(days=365)
    results=session.query(Measurement.station,func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.station=='USC00519281').all()  
    session.close()

    tem=[]
    for station,max,min,avg in results:
        tem_dict={}
        tem_dict['station']=station
        tem_dict['max_temp']=max
        tem_dict['min_temp']=min
        tem_dict['avg_temp']=avg
        tem.append(tem_dict)

    return jsonify(tem)


@app.route("/api/v1.0/<start>")
def start_date(start):
    session=Session(engine)
    Started=session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()

    temp2=[]
    for max,min,avg in Started:
        temp_dict2={}
        temp_dict2['max_temp']=max
        temp_dict2['min_temp']=min
        temp_dict2['avg_temp']=avg
        temp2.append(temp_dict2)

    return jsonify(temp2)


@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start,end):
    session=Session(engine)
    Start_end=session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    temp3=[]
    for max,min,avg in Start_end:
        temp_dict3={}
        temp_dict3['max_temp']=max
        temp_dict3['min_temp']=min
        temp_dict3['avg_temp']=avg
        temp3.append(temp_dict3)

    return jsonify(temp3)


if __name__ == '__main__':
    app.run(debug=True)