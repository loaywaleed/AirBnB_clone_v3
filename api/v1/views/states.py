#!/usr/bin/python3
"""states route module"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, jsonify, request


@app_views.route("/states", strict_slashes=False, methods=["GET"])
@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def get_states(state_id=None):
    lst = []
    if state_id is None:
        states = storage.all(State)
        for state in states.values():
            lst.append(state.to_dict())
        return jsonify(lst)
    else:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_states(state_id=None):
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    storage.delete(states)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    """update state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    state.name = data.get("name", state.name)
    state.save()
    return jsonify(state.to_dict()), 200
