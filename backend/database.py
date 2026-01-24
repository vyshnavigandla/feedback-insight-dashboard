from pymongo import MongoClient
from datetime import datetime
from config import config_dict
import os

env = os.getenv("FLASK_ENV", "development")
config = config_dict[env]

class Database:
    def __init__(self):
        self.client = MongoClient(config.MONGO_URI)
        self.db = self.client[config.DB_NAME]
        self.collection = self.db[config.COLLECTION_NAME]

    def insert_feedback(self, data):
        doc = {
            "name": data.get("name", "Anonymous"),
            "email": data.get("email", ""),
            "order_id": data.get("order_id", ""),
            "product_name": data.get("product_name"),
            "feedback_type": data.get("feedback_type"),
            "priority": data.get("priority", "Low"),
            "rating": int(data.get("rating")),
            "satisfaction": data.get("satisfaction"),
            "comments": data.get("comments", ""),
            "timestamp": datetime.utcnow()
        }
        return self.collection.insert_one(doc)

    def get_all_feedback(self):
        return list(self.collection.find().sort("timestamp", -1))

    def get_stats(self):
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "avgRating": {"$avg": "$rating"},
                    "total": {"$sum": 1},
                    "highPriority": {"$sum": {"$cond": [{"$eq": ["$priority", "High"]}, 1, 0]}}
                }
            }
        ]
        result = list(self.collection.aggregate(pipeline))
        if not result:
            return {"avgRating": 0, "total": 0, "highPriority": 0}
        return result[0]

db_manager = Database()
