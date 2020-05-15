from flask import *

import os

from arcgis.gis import GIS
from arcgis.mapping import WebMap

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/automation/surveyData", methods=["POST"])
def surveyData():
	gis: GIS = GIS(os.environ.get("AGOL_URL"), os.environ.get("AGOL_USERNAME"), os.environ.get("AGOL_PASSWORD"))

	wmItem = gis.content.get("14d876151e084ec591cd999b02374b32")

	wm: WebMap = WebMap(wmItem)

	wm.basemap = "dark-gray"

	wm.update()

	return ""