import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Link frm Python to the Database
session = Session(engine)

session.close()
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route('/')
def home():
return (
f"Routes:<br/>"
f"/api/v1.0/precipitation<br/>"
f"/api/v1.0/stations<br/>"
f"/api/v1.0/tobs<br/>"
f"/api/v1.0/<start><br/>"
f"/api/v1.0/<start>/<end><br/>"
)


@app.route("/api/v1.0/precipitation")
def precipitations():

session = Session(engine)
results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()
result_dict = dict(results)
session.close()

return jsonify(result_dict)


@app.route("/api/v1.0/stations")
def stations():

session = Session(engine)
stations = session.query(Measurement.station, func.count(Measurement.id)).group_by(Measurement.station).\
order_by(func.count(Measurement.id).desc()).all()

stations_dict = dict(stations)
session.close()

return jsonify(stations_dict)

@app.route("/api/v1.0/tobs")
def tobs():
session = Session(engine)

max_temp_observed = session.query(Measurement.station, Measurement.station).filter(Measurement.date >= '2016-08-23').all()

tobs_dict = dict(max_temp_observed)

session.close()

return jsonify(tobs_dict)

@app.route("/api/v1.0/<start><br/>")
def start(start):
session = Session(engine)

results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),
func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date >= start).all()

session.close()


tobs_all = []
for min, max, avg in results:
tobs_dict = {}
tobs_dict["Min"] = min
tobs_dict["Max"] = max
tobs_dict["Avg"] = avg
tobs_all.append(tobs_dict)

return jsonify(tobs_all)

@app.route("/api/v1.0/<start>/<end><br/>")
def start_end(start,end):
session = Session(engine)

results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),
func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

session.close()


tobs_all = []
for min, max, avg in results:
tobs_dict = {}
tobs_dict["Min"] = min
tobs_dict["Max"] = max
tobs_dict["Avg"] = avg
tobs_all.append(tobs_dict)

return jsonify(tobs_all)


if __name__ == "__main__":
app.run(debug=True)
