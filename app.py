from flask import Flask, jsonify, render_template
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/api/v1.0/precipitation")
def normal():
    start_date = dt.datetime(2017,8,23)
    end_date =dt.date(2017,8,23)-dt.timedelta(days=365)
    p_results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= end_date).filter(Measurement.date <= start_date).\
    order_by(Measurement.date).all()
    p_dict= dict(p_results)
    return jsonify(p_dict)
@app.route("/api/v1.0/stations")
def normal1():
    s_results = session.query(Station.station).all()
    s_list= list(s_results)
    return jsonify(s_list)
@app.route("/api/v1.0/tobs")
def normal2():
    start_date = dt.datetime(2017,8,23)
    end_date =dt.date(2017,8,23)-dt.timedelta(days=365)
    temp_ob = session.query(Measurement.tobs).\
    filter(Measurement.date >= end_date).\
    filter(Measurement.date <= start_date).all()
    t_list = list(temp_ob)
    return jsonify(t_list)
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def normal3(start=None,end=None):
    def get_date(date1):
        year, month, day = map(int, date1.split('-'))
        converted_to_date= dt.datetime(year, month, day)
        return converted_to_date
    if start is not None and end is not None:
        start_date=get_date(start)
        end_date =get_date(end)
        agg_q=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        agg_list = list(agg_q)
        return jsonify(agg_list)
    elif start is not None and end is None:
        start_date=get_date(start)
        agg_q=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
          filter(Measurement.date >= start_date).all()
        agg_list = list(agg_q)
        return jsonify(agg_list)
if __name__ == "__main__":
    app.run(debug=True)




