"""Flask app for Cupcakes"""

import os

from flask import Flask, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///cupcakes")

connect_db(app)

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

@app.get("/api/cupcakes")
def get_cupcakes_data():
    """Get and send data about all cupcakes.
    Return JSON: {cupcakes: [{id, flavor, size, rating, image_url}, ...]}"""

    cupcakes = Cupcake.query.all()
    cupcakes_serialized = [cupcake.serialize() for cupcake in cupcakes]

    return jsonify(cupcakes=cupcakes_serialized)


@app.get("/api/cupcakes/<int:cupcake_id>")
def get cupcake_data(cupcake_id):
    """Get and send data about cupcake.
    Return JSON: {cupcake: {id, flavor, size, rating, image_url}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake_serialized = cupcake.serialize()

    return jsonify(cupcake=cupcake_serialized)


