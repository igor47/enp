import json

from flask import Blueprint, Response, request


api = Blueprint('api', __name__)

@api.route("/print_numbers", methods=["POST"])
def print_numbers() -> Response:
    """Prints submitted numbers as a PDF"""
    if not request.is_json:
        return Response(
            json.dumps({"error":f"JSON input expected; received '{request.mimetype}'"}),
            status=406,
            mimetype="application/json",
        )

    params = request.get_json()
    return Response(json.dumps(params), mimetype="application/json")
