from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, send_from_directory
import data_utils, convert_utils
import logging
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='static')
app.secret_key = "YouWillNeverGuessMySecretKey"

# Route handlers
@app.get("/")
def index():
    """Display the app's main (index) page."""
    dates = data_utils.get_all_available_dates()
    return render_template("index.html", title="Swimming Times Statistics", dates=dates)

@app.get("/get_swimmers/<date>")
def get_swimmers(date):
    """Get swimmers who have data for a specific date."""
    try:
        logger.debug(f"Getting swimmers for date: {date}")
        if date not in data_utils.SESSION_DATES:
            logger.warning(f"Invalid date requested: {date}")
            return jsonify([])
            
        swimmers = data_utils.get_swimmers_for_date(date)
        logger.debug(f"Found swimmers: {swimmers}")
        
        if not swimmers:
            logger.warning("No swimmers found!")
            return jsonify([])
            
        response = jsonify(swimmers)
        logger.debug(f"Sending response: {swimmers}")
        return response
    except Exception as e:
        logger.error(f"Error getting swimmers: {str(e)}", exc_info=True)
        return jsonify([])

@app.get("/get_events/<swimmer>/<date>")
def get_events(swimmer, date):
    """Get events a swimmer participated in on a specific date."""
    try:
        logger.debug(f"Getting events for swimmer: {swimmer}, date: {date}")
        if date not in data_utils.SESSION_DATES:
            logger.warning(f"Invalid date requested: {date}")
            return jsonify([])
            
        events = data_utils.get_events_for_swimmer_date(swimmer, date)
        logger.debug(f"Found events: {events}")
        
        if not events:
            logger.warning(f"No events found for {swimmer}!")
            return jsonify([])
            
        response = jsonify(events)
        logger.debug(f"Sending response: {events}")
        return response
    except Exception as e:
        logger.error(f"Error getting events: {str(e)}", exc_info=True)
        return jsonify([])

@app.post("/show_bar_chart")
def show_bar_chart():
    """Display the swimmer's times as a bar chart."""
    try:
        # Get and validate form data
        chosen_date = request.form.get('chosen_date')
        swimmer = request.form.get('swimmer')
        event = request.form.get('event')
        
        logger.debug(f"Form data received - Date: {chosen_date}, Swimmer: {swimmer}, Event: {event}")
        
        if not all([chosen_date, swimmer, event]):
            flash("Please fill in all fields", "warning")
            return redirect(url_for('index'))
        
        # Parse the event string
        event_parts = event.split(" ")
        if len(event_parts) != 2:
            flash("Invalid event format", "warning")
            return redirect(url_for('index'))
            
        distance = event_parts[0].replace('m', '')
        stroke = event_parts[1]
        
        logger.debug(f"Looking for data: {distance}m {stroke}")
        
        # Get swimmer's age for the event
        age = data_utils.get_swimmer_age(swimmer, distance, stroke)
        if not age:
            flash(f"No data found for {swimmer} in {distance}m {stroke}", "warning")
            return redirect(url_for('index'))
        
        # Get times for the selected date
        times_data = data_utils.get_swimmers_times(
            swimmer,
            age,
            distance,
            stroke,
            chosen_date
        )
        
        logger.debug(f"Found data: {times_data}")
        
        if not times_data:
            flash(f"No data found for {swimmer} on {chosen_date} in {distance}m {stroke}", "warning")
            return redirect(url_for('index'))
            
        # Process times data
        times = [time[0] for time in times_data]
        average_str, times_reversed, scaled = convert_utils.perform_conversions(times)
        
        # Calculate average in seconds for the chart
        average_seconds = sum(scaled) / len(scaled) if scaled else 0
        
        # Sort times from fastest to slowest for display
        sorted_data = sorted(zip(times_reversed, scaled), key=lambda x: x[1])
        
        # Prepare chart header
        header = f"{swimmer} (Age {age}) {distance}m {stroke} - {chosen_date}"
        
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
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5001) 