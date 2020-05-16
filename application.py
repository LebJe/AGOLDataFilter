from flask import *

from typing import *

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import hashlib

import os

from arcgis.gis import *
from arcgis.mapping import *
from arcgis.features import *
from arcgis.geocoding import *

def connect() -> scoped_session:
	if not os.environ.get("DATABASE_URL"):
		raise RuntimeError("Missing environment variable DATABASE_URL.")

	engine = create_engine(os.environ.get("DATABASE_URL") + "?sslmode=require")

	return scoped_session(sessionmaker(bind=engine))

# Database connection.
db: scoped_session = connect()

def prepareDB():
	with open("schema.sql", "r") as file:
		contents = file.read()

		db.execute(contents)

		db.commit()

app = Flask(__name__)

prepareDB()

@app.errorhandler(404)
def errorhandler(error):
	return render_template("errors/404.html")

@app.route("/")
def index():
	info = getInfo()

	message = request.args.get("message")

	return render_template("index.html", i=info, message=message)


@app.route("/automation/surveyData", methods=["POST"])
def surveyData():
	return updateFL()


@app.route("/startFilter")
def startFilter():
	return updateFL()


@app.route("/updateInfo", methods=["POST"])
def updateInfo():
	url = request.form.get("url")
	username = request.form.get("username")
	password = request.form.get("password")
	flURL = request.form.get("flURL")

	res = db.execute("SELECT COUNT(*) FROM info").fetchone()

	if res[0] <= 0:
		db.execute("INSERT INTO info(url, username, password, fl_url) VALUES(:url, :username, :password, :fl_url)", {"url": url, "username": username, "password": password, "fl_url": flURL})
	else:
		db.execute("UPDATE info SET url = :url, username = :username, password = :password, fl_url = :fl_url", {"url": url, "username": username,"password":  password, "fl_url": flURL})

	db.commit()

	return redirect("/")


def getInfo() -> Tuple[str, str, str, str]:
	row = db.execute("SELECT url, username, password, fl_url FROM info")

	result = row.fetchone()

	db.commit()

	if result:
		return (result.url, result.username, result.password, result.fl_url)

	return None

def updateFL():
	info = getInfo()

	if info is not None:
		try:
			gis: GIS = GIS(info[0], info[1], info[2])
		except:
			return render_template("errors/error.html", message="Invalid Credentials"), 401
		
		featureLayer: FeatureLayer = FeatureLayer(info[3], gis=gis)

		
		createField = True

		for field in featureLayer.properties["fields"]:
			if field["name"] == "state":
				createField = False

		
		if createField:
			newField = {
				"name": "state",
				"type": "esriFieldTypeString",
				"alias": "State",
				"length": 50,
				"nullable": True,
				"editable": True,
				"visible": True,
				"domain": None
			}

			updateDict = {"fields": [newField]}

			featureLayer.manager.add_to_definition(updateDict)

		fSet: FeatureSet = featureLayer.query()

		data: List[str] = []

		states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
				"Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
				"Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
				"Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
				"Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
				"North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
				"Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
				"Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

		for i in range(0, len(fSet.features)):
			geo = fSet.features[i].as_dict["geometry"]

			for state in states:

				s = geocode(state)[0]

				if geo["y"] <= s["extent"]["ymax"] and geo["y"] >= s["extent"]["ymin"] and geo["x"] >= s["extent"]["xmin"] and geo["x"] <= s["extent"]["xmax"]:
					fSet.features[i].as_dict["attributes"]["state"] = state

		featureLayer.edit_features(updates=fSet.features)

		return redirect("/?message=Filter Complete.")
	else:
		render_template("errors/error.html", message="Missing Credentials"), 403 