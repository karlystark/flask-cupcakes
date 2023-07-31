"""Flask app for Cupcakes"""

import os

from flask import Flask, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, Cupcake, DEFAULT_IMAGE_URL

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
def get_cupcake_data(cupcake_id):
    """Get and send data about cupcake.
    Return JSON: {cupcake: {id, flavor, size, rating, image_url}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake_serialized = cupcake.serialize()

    return jsonify(cupcake=cupcake_serialized)


@app.post("/api/cupcakes")
def create_cupcake():
    """Receives JSON cupcake data and adds Cupcake instance to database.
    Accepts JSON: {cupcake: {flavor, size, rating, image_url}}
    Return JSON: {cupcake: {id, flavor, size, rating, image_url}} """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]

    if request.json["image_url"] == "":
        image_url = None
    else:
        image_url = request.json["image_url"]

    new_cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image_url=image_url
    )

    db.session.add(new_cupcake)
    db.session.commit()

    cupcake_serialized = new_cupcake.serialize()

    return (jsonify(cupcake=cupcake_serialized), 201)


@app.patch("/api/cupcakes/<int:cupcake_id>")
def update_cupcake_data(cupcake_id):
    """Recieve JSON cupcake data and updates cupcake instance
    Accept (but doesn't require all): {cupcake: {flavor, size, rating, image_url}}
    Return JSON: {cupcake: {id, flavor, size, rating, image_url}}
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image_url = request.json["image_url"]

    if flavor != "":
        cupcake.flavor = flavor

    if size != "":
        cupcake.size = size

    if rating != None:
        cupcake.rating = rating

    if request.json["image_url"] != "":
        cupcake.image_url = image_url

    db.session.commit()

    cupcake_serialized = cupcake.serialize()

    return jsonify(cupcake=cupcake_serialized)


@app.delete("/api/cupcakes/<int:cupcake_id>")
def delete_cupcake(cupcake_id):
    """Delete cupcake from database.
    Return JSON: {deleted: [cupcake-id]}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(deleted=[cupcake_id])





