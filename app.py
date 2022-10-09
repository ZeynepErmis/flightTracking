from flask_marshmallow import Marshmallow
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, render_template
from flask_cors import CORS
import json

DEBUG = True
app = Flask(__name__, template_folder='templates')
CORS(app, resources={r'/*': {'origins': '*'}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////workspace_intern/flightTracking/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Coordinates(db.Model):
    __tablename__ = 'coordinates'
    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(30))
    lat = db.Column(db.Float(10, 10), nullable=False)
    lng = db.Column(db.Float(10, 10), nullable=False)


class CoordinatesLatLng(db.Model):
    __tablename__ = 'coordinates_test'
    id = db.Column(db.Integer, primary_key=True)
    coordinates_id = db.Column(db.Integer, db.ForeignKey(
        'coordinates.id'), nullable=False)
    lat = db.Column(db.Float(10, 10), nullable=False)
    lng = db.Column(db.Float(10, 10), nullable=False)


class CoordinatesSchema(ma.Schema):
    class Meta:
        fields = ("id", "province")


class CoordinatesSchema_test(ma.Schema):
    class Meta:
        fields = ("id", "lat", "lng", "province")


coordinates_schema = CoordinatesSchema()
coordinates_schema = CoordinatesSchema(many=True)

coordinates_schema_test = CoordinatesSchema_test()
coordinates_schema_test = CoordinatesSchema_test(many=True)


@app.route("/showCoordinates", methods=['GET'])
def showCoordinates():
    myCoordinates = Coordinates.query.all()
    return myCoordinates


@app.route('/test')
def index():
    all_coordinates = Coordinates.query.all()
    data = coordinates_schema.dump(all_coordinates)
    return json.dumps(data, ensure_ascii=False)


@app.route('/test2')
def index2():
    all_coordinates2 = Coordinates.query.all()
    return coordinates_schema_test.dump(all_coordinates2)


@app.route("/test2/{id}")
def coordinatesLatAndLng(id):
    coordinates = Coordinates.query.where()


@app.route("/", methods=['POST', 'GET'])
def main_page():
    if request.method == 'POST':
        province = request.form['province']
        lat = request.form['lat']
        lng = request.form['lng']
        coordinates = Coordinates(province=province, lat=lat, lng=lng)
        db.session.add(coordinates)
        db.session.commit()
    allcoordinates = Coordinates.query.all()
    return render_template('home.html', coordinates=allcoordinates)


if __name__ == '__main__':
    app.run(debug=True)
