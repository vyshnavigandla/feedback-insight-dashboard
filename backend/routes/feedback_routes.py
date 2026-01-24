from flask import Blueprint, request, jsonify
from database import db_manager

feedback_bp = Blueprint("feedback_bp", __name__)

@feedback_bp.route("/submit", methods=["POST"])
def submit():
    data = request.json
    try:
        result = db_manager.insert_feedback(data)
        return jsonify({"status": "success", "message": "Feedback stored successfully", "id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@feedback_bp.route("/all", methods=["GET"])
def get_all():
    try:
        records = db_manager.get_all_feedback()
        for r in records:
            r["_id"] = str(r["_id"])
            if "timestamp" in r: r["timestamp"] = r["timestamp"].isoformat()
        return jsonify(records), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
