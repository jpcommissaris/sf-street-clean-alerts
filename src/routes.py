from flask import Blueprint, request, jsonify, current_app
from services import get_street_cleaning_info

api_bp = Blueprint("api", __name__)
app = current_app

type ReqBody = dict[str, float]


@api_bp.route("/api/next-cleaning", methods=["POST"])
def next_cleaning():
    body: ReqBody = request.get_json()
    app.logger.info(f"Received request body: {body}")
    lat, lon = body.get("latitude"), body.get("longitude")
    if lat is None or lon is None:
        app.logger.info(f"Not lat/long error")
        return (jsonify({"error": "latitude and longitude required"}), 400)

    info = get_street_cleaning_info(lat, lon)

    if not info:
        app.logger.info(f"Not info error")
        return (
            jsonify({"error": "No street cleaning info found for this location"}),
            404,
        )

    app.logger.info(f"INFO {info}")
    return jsonify(info)
