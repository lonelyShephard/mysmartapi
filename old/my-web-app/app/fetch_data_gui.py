import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.login import login

fetch_data_bp = Blueprint('fetch_data', __name__)

@fetch_data_bp.route('/fetch_data', methods=['GET', 'POST'])
def fetch_data():
    if request.method == 'POST':
        # Logic to fetch historical data
        # This is a placeholder for the actual data fetching logic
        historical_data = {"data": "Sample historical data"}
        return render_template('options.html', historical_data=historical_data)
    
    return render_template('options.html')