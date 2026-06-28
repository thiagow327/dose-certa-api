from flask import redirect
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info
from werkzeug.utils import redirect

from database.db import db

info = Info(title="Dose Certa API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

@app.get("/")
def index():
    return redirect("/openapi")



