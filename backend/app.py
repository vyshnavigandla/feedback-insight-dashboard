import os
from flask import Flask, jsonify, render_template
from flask_cors import CORS

# This import now matches config.py exactly
from config import config_dict 
from routes import api_bp

# ----------------------------------
# App Initialization & Path Mapping
# ----------------------------------
app = Flask(
    __name__,
    template_folder='../frontend', 
    static_folder='../frontend',
    static_url_path=''
)

# ----------------------------------
# Configuration Setup
# ----------------------------------
env = os.getenv("FLASK_ENV", "development")

# Load settings from config_dict
if env in config_dict:
    app.config.from_object(config_dict[env])
else:
    app.config.from_object(config_dict["development"])

CORS(app)

# ----------------------------------
# Register Blueprints
# ----------------------------------
# This connects your feedback and analysis routes
app.register_blueprint(api_bp, url_prefix="/api")

# ----------------------------------
# Frontend Routing (Redirect to index)
# ----------------------------------
@app.route("/")
def index():
    """Serves the main index.html from the frontend folder."""
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    """Serves the dashboard.html from the frontend folder."""
    return render_template("dashboard.html")

@app.route('/favicon.ico')
def favicon():
    """Prevents 404 errors in terminal when browser asks for icon."""
    return '', 204

# ----------------------------------
# Main Execution
# ----------------------------------
if __name__ == "__main__":
    print("\n" + "="*40)
    print(f"🚀 PROJECT RUNNING IN {env.upper()} MODE")
    print(f"🔗 Feedback Form: http://127.0.0.1:5000")
    print(f"📈 Dashboard:     http://127.0.0.1:5000/dashboard")
    print("="*40 + "\n")
    
    # use_reloader=False helps avoid WinError 10038 on some Windows machines
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])