from flask import Blueprint, render_template, request, redirect, url_for
from app.fetch_data_gui import fetch_historical_data
from app.place_order_gui import place_order
from app.websocket_stream import start_live_stream
from app.exit_smartapi import exit_application

options_bp = Blueprint('options', __name__)

@options_bp.route('/options', methods=['GET', 'POST'])
def options():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'historical_data':
            return fetch_historical_data()
        elif action == 'place_order':
            return place_order()
        elif action == 'live_stream':
            return start_live_stream()
        elif action == 'exit':
            exit_application()
            return redirect(url_for('login.login'))  # Redirect to login after exit

    return render_template('options.html')