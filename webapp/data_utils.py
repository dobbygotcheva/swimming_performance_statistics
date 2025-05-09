import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Constants
DATA_DIR_NAME = 'swimdata2'
SESSION_DATES = [
    "2024-01-15",  # First session
    "2024-01-22",  # Second session
    "2024-01-29"   # Third session
]

def get_base_dir():
    """Get the base directory for data files."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logger.debug(f"Base directory: {base_dir}")
    return base_dir

def get_data_dir():
    """Get the data directory path."""
    base_dir = get_base_dir()
    data_dir = os.path.join(base_dir, 'Swimming_times_statistics-main', DATA_DIR_NAME, DATA_DIR_NAME)
    logger.debug(f"Base directory: {base_dir}")
    logger.debug(f"Data directory: {data_dir}")
    logger.debug(f"Data directory exists: {os.path.exists(data_dir)}")
    if os.path.exists(data_dir):
        logger.debug(f"Files in data directory: {os.listdir(data_dir)}")
    return data_dir

# Date-related functions
def get_all_available_dates():
    """Get all available dates from the data files."""
    return SESSION_DATES

def get_swimmers_for_date(date):
    """Get all swimmers who have data for a specific date."""
    data_dir = get_data_dir()
    swimmers = set()
    
    logger.debug(f"Getting swimmers for date: {date}")
    logger.debug(f"Data directory: {data_dir}")
    
    if not os.path.exists(data_dir):
        logger.warning(f"Data directory does not exist: {data_dir}")
        return []
    
    try:
        files = os.listdir(data_dir)
        logger.debug(f"Found {len(files)} files in directory")
        logger.debug(f"Files: {files}")
        
        for filename in files:
            if filename.endswith('.txt') and not filename.startswith('.'):
                parts = filename.split('-')
                logger.debug(f"Processing file: {filename}, parts: {parts}")
                if len(parts) == 4:
                    swimmer = parts[0]
                    swimmers.add(swimmer)
                    logger.debug(f"Found swimmer: {swimmer} from file: {filename}")
        
        swimmers_list = sorted(list(swimmers))
        logger.debug(f"Returning swimmers: {swimmers_list}")
        return swimmers_list
    except Exception as e:
        logger.error(f"Error reading directory: {str(e)}", exc_info=True)
        return []

# Swimmer-related functions
def get_available_swimmers():
    """Get list of all available swimmers from the data files."""
    swimmers = set()
    data_dir = get_data_dir()
    
    if os.path.exists(data_dir):
        logger.debug(f"Directory exists, listing files...")
        for filename in os.listdir(data_dir):
            if filename.endswith('.txt') and not filename.startswith('.'):
                parts = filename.split('-')
                if len(parts) == 4:
                    swimmer = parts[0]
                    swimmers.add(swimmer)
                    logger.debug(f"Found swimmer: {swimmer} from file: {filename}")
    else:
        logger.warning(f"Directory does not exist: {data_dir}")
    
    return sorted(list(swimmers))

def get_swimmer_age(swimmer, distance, stroke):
    """Get a swimmer's age for a specific event."""
    data_dir = get_data_dir()
    
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt') and not filename.startswith('.'):
            parts = filename.split('-')
            if len(parts) == 4 and parts[0] == swimmer and parts[2] == f"{distance}m" and parts[3].startswith(stroke):
                return parts[1]
    return None

# Event-related functions
def get_events_for_swimmer_date(swimmer, date):
    """Get all events a swimmer participated in on a specific date."""
    data_dir = get_data_dir()
    events = set()
    
    try:
        for filename in os.listdir(data_dir):
            if filename.endswith('.txt') and not filename.startswith('.'):
                parts = filename.split('-')
                if len(parts) == 4 and parts[0] == swimmer:
                    distance = parts[2].replace('m', '')
                    stroke = parts[3].replace('.txt', '')
                    events.add(f"{distance}m {stroke}")
                    logger.debug(f"Found event: {distance}m {stroke} for {swimmer}")
        
        events_list = sorted(list(events))
        logger.debug(f"Returning events for {swimmer}: {events_list}")
        return events_list
    except Exception as e:
        logger.error(f"Error getting events: {str(e)}", exc_info=True)
        return []

def get_available_events():
    """Get list of all available events from the data files."""
    events = set()
    data_dir = get_data_dir()
    
    if os.path.exists(data_dir):
        logger.debug(f"Directory exists, listing files...")
        for filename in os.listdir(data_dir):
            if filename.endswith('.txt') and not filename.startswith('.'):
                parts = filename.split('-')
                if len(parts) == 4:
                    distance = parts[2]
                    stroke = parts[3].replace('.txt', '')
                    event = f"{distance} {stroke}"
                    events.add(event)
                    logger.debug(f"Found event: {event} from file: {filename}")
    else:
        logger.warning(f"Directory does not exist: {data_dir}")
    
    return sorted(list(events))

# Time-related functions
def get_swimmers_times(swimmer, age, distance, stroke, date):
    """Get a swimmer's times for a specific event on a specific date."""
    data_dir = get_data_dir()
    filename = f"{swimmer}-{age}-{distance}m-{stroke}.txt"
    filepath = os.path.join(data_dir, filename)
    
    if not os.path.exists(filepath):
        return []
        
    with open(filepath, 'r') as f:
        content = f.read().strip()
        if not content:
            return []
            
        times = [time.strip() for time in content.split(',')]
        return [(time, date) for time in times if time]

def get_available_dates(swimmer, age, distance, stroke):
    """Get list of available dates for a swimmer's event."""
    return SESSION_DATES 