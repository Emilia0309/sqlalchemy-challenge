#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os

cwd = os.getcwd()
print(cwd)


# In[7]:


import os
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Set up the database using absolute path
##database_path = "/Users/acenyong/Downloads/Starter_Code-14/Resources/hawaii.sqlite"
database_path = "Downloads/Starter_Code-14/Resources/hawaii.sqlite"

engine = create_engine(f"sqlite:///{database_path}")

Base = automap_base()
Base.prepare(engine, reflect=True)

# Create session
session = Session(engine)

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    """List all available routes."""
    return jsonify({
        'routes': [
            '/api/v1.0/precipitation',
            '/api/v1.0/stations',
            '/api/v1.0/tobs',
            '/api/v1.0/<start>',
            '/api/v1.0/<start>/<end>'
        ]
    })

@app.route('/api/v1.0/precipitation')
def precipitation():
    """Return precipitation data for the last 12 months."""
    most_recent_date = session.query(func.max(Base.classes.measurement.date)).scalar()
    one_year_ago = datetime.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)

    results = session.query(
        Base.classes.measurement.date,
        Base.classes.measurement.prcp
    ).filter(Base.classes.measurement.date >= one_year_ago).all()

    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def stations():
    """Return a list of stations."""
    results = session.query(Base.classes.station.name).all()
    stations_list = [result[0] for result in results]
    return jsonify(stations=stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    """Return temperature observations for the most-active station for the previous year."""
    most_active_station = session.query(Base.classes.measurement.station).\
        group_by(Base.classes.measurement.station).\
        order_by(func.count(Base.classes.measurement.id).desc()).first()[0]

    most_recent_date = session.query(func.max(Base.classes.measurement.date)).scalar()
    one_year_ago = datetime.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)

    results = session.query(
        Base.classes.measurement.date,
        Base.classes.measurement.tobs
    ).filter(Base.classes.measurement.date >= one_year_ago).\
    filter(Base.classes.measurement.station == most_active_station).all()

    temps = [{"date": date, "temperature": temp} for date, temp in results]
    return jsonify(temps=temps)

@app.route('/api/v1.0/<start>')
def start(start):
    """Return TMIN, TAVG, and TMAX for a specified start date."""
    results = session.query(
        func.min(Base.classes.measurement.tobs),
        func.avg(Base.classes.measurement.tobs),
        func.max(Base.classes.measurement.tobs)
    ).filter(Base.classes.measurement.date >= start).all()

    return jsonify({
        'TMIN': results[0][0],
        'TAVG': results[0][1],
        'TMAX': results[0][2]
    })

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    """Return TMIN, TAVG, and TMAX for a specified start-end range."""
    results = session.query(
        func.min(Base.classes.measurement.tobs),
        func.avg(Base.classes.measurement.tobs),
        func.max(Base.classes.measurement.tobs)
    ).filter(Base.classes.measurement.date >= start).filter(Base.classes.measurement.date <= end).all()

    return jsonify({
        'TMIN': results[0][0],
        'TAVG': results[0][1],
        'TMAX': results[0][2]
    })

@app.route('/api/v1.0/station_measurements')
def station_measurements():
    """Return combined station and measurement data."""
    results = session.query(
        Base.classes.station.name,
        Base.classes.measurement.date,
        Base.classes.measurement.tobs
    ).join(Base.classes.measurement, Base.classes.station.station == Base.classes.measurement.station).all()

    station_data = [
        {
            "station": station_name,
            "date": date,
            "temperature": temp
        }
        for station_name, date, temp in results
    ]

    return jsonify(station_data)

if __name__ == '__main__':
    app.run(debug=True)



# In[13]:





# In[ ]:




