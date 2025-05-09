# Swimming Times Statistics

A web application for tracking and analyzing swimming times and performance statistics.

## Features

- Track swimming times for different events and distances
- View performance statistics and trends
- Generate visual charts and comparisons
- Support for multiple swimmers and events
- Modern, responsive web interface

## Project Structure

```
swimming_times_statistics/
├── webapp/                    # Main application directory
│   ├── static/               # Static files (CSS, images)
│   │   └── background.webp   # Background image
│   ├── templates/            # HTML templates
│   │   ├── base.html        # Base template
│   │   ├── index.html       # Main page
│   │   └── chart.html       # Chart display page
│   ├── app.py               # Main Flask application
│   ├── data_utils.py        # Data processing utilities
│   └── convert_utils.py     # Time conversion utilities
├── tests/                    # Test files
├── requirements.txt          # Python dependencies
└── README.md                # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd swimming_times_statistics
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure you're in the project directory and your virtual environment is activated.

2. Start the Flask application:
```bash
cd webapp
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5001
```

## Dependencies

- Flask 3.0.0
- SQLAlchemy 2.0.23
- NumPy 1.26.0
- Matplotlib 3.8.2
- Python-dateutil 2.8.2
- MySQL-connector-python 8.2.0

## Usage

1. Select a date from the dropdown menu
2. Choose a swimmer
3. Select an event
4. View the performance statistics and charts

## Development

The application is built using:
- Backend: Python/Flask
- Frontend: HTML, CSS, JavaScript
- Database: MySQL
- Data Visualization: Matplotlib

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 