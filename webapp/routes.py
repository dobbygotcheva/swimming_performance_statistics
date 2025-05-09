from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from . import data_utils, convert_utils
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Clear any existing session data
    session.clear()
    dates = data_utils.get_all_available_dates()
    logger.debug(f"Available dates: {dates}")
    return render_template('index.html', dates=dates)

@main.route('/get_swimmers/<date>')
def get_swimmers(date):
    """Get swimmers who have data for a specific date."""
    try:
        swimmers = data_utils.get_swimmers_for_date(date)
        return jsonify(swimmers)
    except Exception as e:
        logger.error(f"Error getting swimmers: {str(e)}", exc_info=True)
        return jsonify([])

@main.route('/get_events/<swimmer>/<date>')
def get_events(swimmer, date):
    """Get events a swimmer participated in on a specific date."""
    try:
        events = data_utils.get_events_for_swimmer_date(swimmer, date)
        return jsonify(events)
    except Exception as e:
        logger.error(f"Error getting events: {str(e)}", exc_info=True)
        return jsonify([])

@main.route("/showbarchart", methods=['POST'])
def show_bar_chart():
    try:
        # Store form data in session
        session['chosen_date'] = request.form.get('chosen_date')
        session['swimmer'] = request.form.get('swimmer')
        event = request.form.get('event')
        
        logger.debug(f"Form data received - Date: {session['chosen_date']}, Swimmer: {session['swimmer']}, Event: {event}")
        
        if not all([session['chosen_date'], session['swimmer'], event]):
            flash("Please fill in all fields", "warning")
            return redirect(url_for('main.index'))
        
        # Parse the event string correctly
        event_parts = event.split(" ")
        if len(event_parts) != 2:
            flash("Invalid event format", "warning")
            return redirect(url_for('main.index'))
            
        distance = event_parts[0].replace('m', '')  # Remove 'm' from distance
        stroke = event_parts[1]
        
        logger.debug(f"Looking for data: {distance}m {stroke}")
        
        # Extract age from the swimmer's data file
        age = data_utils.get_swimmer_age(session["swimmer"], distance, stroke)
        if not age:
            flash(f"No data found for {session['swimmer']} in {distance}m {stroke}", "warning")
            return redirect(url_for('main.index'))
        
        # Get times for the selected date
        data = data_utils.get_swimmers_times(
            session["swimmer"],
            age,
            distance,
            stroke,
            session['chosen_date']
        )
        
        logger.debug(f"Found data: {data}")
        
        if not data:
            flash(f"No data found for {session['swimmer']} on {session['chosen_date']} in {distance}m {stroke}", "warning")
            return redirect(url_for('main.index'))
            
        times = [time[0] for time in data]
        average_str, times_reversed, scaled = convert_utils.perform_conversions(times)
        
        # Calculate average in seconds for the chart
        average_seconds = sum(scaled) / len(scaled) if scaled else 0
        
        # Sort times from fastest to slowest for display
        sorted_data = sorted(zip(times_reversed, scaled), key=lambda x: x[1])
        
        header = f"{session['swimmer']} (Age {age}) {distance}m {stroke} - {session['chosen_date']}"
        
        logger.debug(f"Rendering chart with {len(times)} times")
        return render_template(
            "chart.html",
            title=header,
            data=sorted_data,
            average=average_str,
            average_seconds=average_seconds,
            convert_utils=convert_utils
        )
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('main.index')) 