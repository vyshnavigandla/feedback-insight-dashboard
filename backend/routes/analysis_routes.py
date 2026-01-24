from flask import Blueprint, jsonify
from database import db_manager
from analysis import FeedbackAnalyzer

analysis_bp = Blueprint("analysis_bp", __name__)

@analysis_bp.route("/stats", methods=["GET"])
def get_insights():
    try:
        records = db_manager.get_all_feedback()
        if not records: return jsonify({"message":"No data available"}), 200
        total = len(records)
        avg_rating = round(sum(r.get("rating",0) for r in records)/total,1)
        ai_suggestion = FeedbackAnalyzer.generate_suggestion(records)
        sentiment = "Positive" if avg_rating>=4 else "Neutral" if avg_rating>=2.5 else "Negative"
        return jsonify({
            "total": total,
            "avgRating": avg_rating,
            "ai_suggestion": ai_suggestion,
            "sentiment": sentiment,
            "records": records
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
