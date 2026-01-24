from datetime import datetime

class FeedbackModel:
    def __init__(self, name=None, email=None, order_id=None, product_name=None, 
                 feedback_type=None, priority=None, rating=None, satisfaction=None, comments=""):
        self.name = name or "Anonymous"
        self.email = email
        self.order_id = order_id
        self.product_name = product_name
        self.feedback_type = feedback_type
        self.rating = self.validate_rating(rating)
        
        # AUTO-VALIDATION: Priority is set based on Rating if not provided
        # 1-2 stars = High, 3 = Medium, 4-5 = Low
        if not priority:
            if self.rating <= 2: self.priority = "High"
            elif self.rating == 3: self.priority = "Medium"
            else: self.priority = "Low"
        else:
            self.priority = priority if priority in ["Low", "Medium", "High"] else "Low"

        self.satisfaction = satisfaction
        self.comments = comments
        
        # Formatted for Plotly: "YYYY-MM-DD HH:MM:SS"
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def validate_rating(value):
        try:
            rating = int(value)
            if 1 <= rating <= 5: 
                return rating
            return 3  # Default to 3 if out of range
        except (ValueError, TypeError):
            return 0

    def to_dict(self):
        """Returns the model data as a dictionary for MongoDB insertion."""
        return {
            "name": self.name,
            "email": self.email,
            "order_id": self.order_id,
            "product_name": self.product_name,
            "feedback_type": self.feedback_type,
            "priority": self.priority,
            "rating": self.rating,
            "satisfaction": self.satisfaction,
            "comments": self.comments,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_request(cls, data):
        """Validates incoming JSON and creates a model instance."""
        required_fields = ["product_name", "feedback_type", "rating", "satisfaction"]
        errors = [f"{f} is missing" for f in required_fields if not data.get(f)]
        
        if errors:
            return None, errors
            
        instance = cls(
            name=data.get("name"),
            email=data.get("email"),
            order_id=data.get("order_id"),
            product_name=data.get("product_name"),
            feedback_type=data.get("feedback_type"),
            priority=data.get("priority"),
            rating=data.get("rating"),
            satisfaction=data.get("satisfaction"),
            comments=data.get("comments", "")
        )
        return instance, []