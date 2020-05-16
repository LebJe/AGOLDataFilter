from flask import *

from typing import *

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import hashlib

import os

from arcgis.gis import GIS
from arcgis.mapping import WebMap

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

@app.route("/")
def index():
	credentials = getCredentials()

	return render_template("index.html", c=credentials)


@app.route("/automation/surveyData", methods=["POST"])
def surveyData():
	credentials = getCredentials()

	if credentials is not None:
		gis: GIS = GIS(credentials[0], credentials[1], credentials[3])

		wmItem = gis.content.get("14d876151e084ec591cd999b02374b32")

		wm: WebMap = WebMap(wmItem)

		wm.basemap = "dark-gray"

		wm.update()

		return ""
	else:
		"Missing Credentials", 404


@app.route("/updateCredentials", methods=["POST"])
def updateCredentials():
	url = request.form.get("url")
	username = request.form.get("username")
	password = request.form.get("password")

	res = db.execute("SELECT COUNT(*) FROM credentials").fetchone()

	if res[0] <= 0:
		print("insert")
		db.execute("INSERT INTO credentials(url, username, password) VALUES(:url, :username, :password)", {"url": url, "username": username, "password": password})
	else:
		print("update")
		db.execute("UPDATE credentials SET url = :url, username = :username, password = :password", {"url": url, "username": username,"password":  password})

	db.commit()

	return redirect("/")


def getCredentials() -> Tuple[str, str, str]:
	row = db.execute("SELECT url, username, password FROM credentials")

	result = row.fetchone()

	db.commit()

	if result:
		return (result.url, result.username, result.password)

	return None