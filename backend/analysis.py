from textblob import TextBlob

class FeedbackAnalyzer:
    @staticmethod
    def get_sentiment_label(rating, comments):
        analysis = TextBlob(comments)
        polarity = analysis.sentiment.polarity
        if len(comments.strip()) < 5:
            if rating >= 4: return "Positive"
            if rating <= 2: return "Negative"
            return "Neutral"
        if polarity > 0.1: return "Positive"
        if polarity < -0.1: return "Negative"
        return "Neutral"

    @staticmethod
    def generate_suggestion(records):
        if not records: return "Waiting for more customer data."
        complaints = [r for r in records if r.get("feedback_type") == "Complaint"]
        high_priority = [r for r in records if r.get("priority") == "High"]
        avg_rating = sum(r.get("rating",0) for r in records)/len(records)
        if len(high_priority) > 2:
            return f"Critical: {len(high_priority)} high-priority issues detected."
        if avg_rating < 3.0:
            return "Trend Alert: Ratings are dipping."
        if len(complaints) > (len(records)*0.5):
            return "High volume of complaints. Review product/service."
        return "Performance stable. Keep encouraging compliments."
