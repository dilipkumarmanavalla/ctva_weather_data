from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String)
    date = db.Column(db.Date)
    max_temp = db.Column(db.Integer)
    min_temp = db.Column(db.Integer)
    precipitation = db.Column(db.Integer)

class WeatherStats(db.Model):
    __tablename__ = 'weather_stats'
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String)
    year = db.Column(db.Integer)
    avg_max_temp = db.Column(db.Float)
    avg_min_temp = db.Column(db.Float)
    total_precipitation = db.Column(db.Float)