from flask import Flask, render_template, redirect, url_for, request, session
import os
from routes.auth import AUTH_BLUEPRINT
from routes.historical import historical_bp
from routes.orders import orders_bp
from routes.streaming import streaming_bp
from routes.exit import exit_bp

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")  # Set a default secret key

# Register blueprints for different routes
app.register_blueprint(AUTH_BLUEPRINT)
app.register_blueprint(historical_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(streaming_bp)
app.register_blueprint(exit_bp)

@app.route('/')
def index():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)