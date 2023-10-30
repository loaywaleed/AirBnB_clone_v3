#!/usr/bin/python3
"""states route module"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.state import City
from flask import abort, jsonify, request


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def get_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["GET"])
def get_city_state(state_id):
    lst = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    for city in cities:
        lst.append(city.to_dict())
    return jsonify(lst)


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_city(city_id=None):
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    storage.delete(cities)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["POST"])
def create_city_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    state_id = {"state_id": state.id}
    new_state = City(**data, **state_id)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def update_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    city.name = data.get("name", city.name)
    city.save()
    return jsonify(city.to_dict()), 200
