from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from app.login import login

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    if request.method == 'POST':
        # Here you would handle the order placement logic
        order_details = request.form['order_details']
        # Assuming you have a function to place the order
        # place_order_function(order_details)
        flash('Order placed successfully!', 'success')
        return redirect(url_for('options'))

    return render_template('place_order.html')

if __name__ == '__main__':
    app.run(debug=True)