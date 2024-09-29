from flask import Blueprint, render_template, request
from app import app
from datetime import datetime
from .sshlogin import generate_synthetic_logs, save_logs, generate_daily_activity_logs

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/analyse')
def analyse():
    return render_template('analyse.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Check if the user clicked on 'Submit' button for option1 (SSH Login)
    if 'manualGen' in request.form and request.form.get('dropdown') == 'option1':
        # Get the user input
        timestamp_str = request.form.get('timestamp')
        host_name = request.form.get('hostName')
        source_ip = request.form.get('sourceIP')
        user_acc = request.form.get('userAcc')
        event_outcome = request.form.get('eventOutcome')
        num_logs = int(request.form.get('NumLogs'))

        # Convert the starting timestamp to a datetime object
        start_timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S')

        # Generate synthetic logs
        logs = generate_synthetic_logs(start_timestamp, host_name, source_ip, user_acc, event_outcome, num_logs)

        # Save logs to a file
        save_logs(logs)

        return "SSH Logs generated successfully!"
    
    if 'quickGen' in request.form and request.form.get('dropdown') == 'option1':
        # Generate daily activity logs for 10 users with random brute force attacks and off-hours login attempts
        logs = generate_daily_activity_logs()
        save_logs(logs)
        return "Daily network activity logs generated successfully!"

    return "No valid option selected!"
