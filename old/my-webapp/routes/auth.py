python
from flask import Blueprint, render_template, request, redirect, url_for, flash
from smartapi.auth_core import login
import os
from dotenv import load_dotenv

AUTH_BLUEPRINT = Blueprint('auth', __name__)

# Load environment variables from .env.trading
ANGELALGO_PATH = r"C:\Users\user\projects\angelalgo"
env_file = ".env.trading"
env_path = os.path.join(ANGELALGO_PATH, env_file)
load_dotenv(env_path)

@AUTH_BLUEPRINT.route('/login', methods=['GET', 'POST'])
def login_route():
    client_id = os.getenv("CLIENT_ID")
    password = os.getenv("PASSWORD")

    # Mask the client ID and password for display
    client_id_masked = "*" * len(client_id) if client_id else ""
    password_masked = "*" * len(password) if password else ""

    if request.method == 'POST':
        totp = request.form.get("totp")
        smart_api, auth_token, refresh_token = login(totp)
        if smart_api:
            flash("Login Successful!", category="success")
            # Redirect to a dashboard that offers further options as buttons
            return redirect(url_for('routes.dashboard'))
        else:
            flash("Login Failed!", category="error")
    return render_template('login.html', client_id_masked=client_id_masked, password_masked=password_masked)
