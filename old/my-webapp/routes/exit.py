from flask import Blueprint, redirect, url_for, session, flash

exit_bp = Blueprint('exit', __name__)

@exit_bp.route('/exit', methods=['POST'])
def exit_application():
    session.clear()  # Clear the session data
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('auth.login'))  # Redirect to the login page