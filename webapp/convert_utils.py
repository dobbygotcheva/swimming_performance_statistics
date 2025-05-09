import json
import statistics

CONVERSIONS = {
    "Free": "freestyle",
    "Back": "backstroke",
    "Breast": "breaststroke",
    "Fly": "butterfly",
    "IM": "individual medley",
}

def convert2range(value, from_min, from_max, to_min, to_max):
    """Convert a value from one range to another."""
    # Figure out how 'wide' each range is
    from_span = from_max - from_min
    to_span = to_max - to_min

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - from_min) / float(from_span)

    # Convert the 0-1 range into a value in the right range.
    return to_min + (value_scaled * to_span)

def time_to_seconds(time_str):
    """Convert a time string (e.g., '1:23.45') to seconds."""
    if ':' in time_str:
        minutes, seconds = time_str.split(':')
        return float(minutes) * 60 + float(seconds)
    return float(time_str)

def seconds_to_time(seconds):
    """Convert seconds to a time string format."""
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    if minutes > 0:
        return f"{minutes}:{remaining_seconds:05.2f}"
    return f"{remaining_seconds:.2f}"

def time_difference(time1, time2):
    """Calculate the difference between two times and format with + or - sign."""
    seconds1 = time_to_seconds(time1)
    seconds2 = time_to_seconds(time2)
    diff = seconds2 - seconds1  # Positive when time2 is slower
    sign = '+' if diff > 0 else ''
    return f"{sign}{diff:.2f}"

def perform_conversions(times):
    """Process a list of swim times."""
    if not times:
        return "N/A", [], []
        
    # Convert times to seconds for calculations
    times_in_seconds = [time_to_seconds(time) for time in times]
    
    # Calculate average
    average_seconds = sum(times_in_seconds) / len(times_in_seconds)
    average_str = seconds_to_time(average_seconds)
    
    # Sort times from fastest to slowest
    sorted_times = sorted(zip(times, times_in_seconds), key=lambda x: x[1])
    times_reversed = [time[0] for time in sorted_times]
    scaled = [time[1] for time in sorted_times]
    
    return average_str, times_reversed, scaled 