# Blue Crab GIS

A Geographic Information System for Blue Crab population monitoring using PyQt5, OpenStreetMap, and Leaflet.js.

## Overview

Blue Crab GIS is a desktop application designed for monitoring and analyzing blue crab populations in the Negros Island region. It provides an intuitive interface for data visualization, analysis, and management.

## Key Features

### Interactive GIS Map
- Dark mode interface with customizable map layers
- Real-time population density visualization
- Location search functionality
- Interactive markers with detailed information
- Customizable map controls and filters

### Data Management
- CSV file import with drag-and-drop support
- Manual data entry form
- SQLite database for reliable data storage
- Data validation and error handling
- Export functionality for reports

### Analytics Dashboard
- Population distribution charts
- Density heatmaps
- Year-over-year comparisons
- Sex ratio analysis
- Regional statistics

### User Interface
- Modern glass-effect design
- Responsive layout
- Customizable settings
- Dark theme for reduced eye strain
- Intuitive navigation

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Blue-Crab-GIS.git
   cd Blue-Crab-GIS
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Project Structure

```
Blue Crab GIS/
├── LICENSE                     # MIT License file
├── main.py                    # Main application entry point
├── run_erd.py                 # ERD (Entity Relationship Diagram) runner
├── requirements.txt           # Python package dependencies
├── readme                     # Project documentation

├── assets/                    # Static assets directory
│   └── map/                   # Map-related assets
│       └── gis_map.html       # Generated map HTML file

├── data/                      # Data storage directory
│   └── ...                    # Database and data files

├── GeoJson/                   # Geographic data files
│   └── map.geojson           # Map GeoJSON data

└── src/                       # Source code directory
    ├── __init__.py           # Python package marker
    ├── gis_map.py            # GIS map implementation
    ├── main_window.py        # Main application window
    ├── sidebar.py            # Sidebar navigation
    ├── about.py              # About page
    ├── settings.py           # Application settings
    ├── dashboard.py          # Dashboard implementation
    ├── analytics.py          # Analytics implementation
    ├── datasets.py           # Dataset management
    ├── upload_data.py        # Data upload functionality
    └── utils/                # Utility modules
        ├── __init__.py       # Package marker
        ├── database.py       # Database management
        ├── map_controls.py   # Map control widgets
        └── glass_controls.py # Glass-effect UI controls
```

## Performance Optimization

The application implements several optimizations for low-spec laptops:

1. Hardware acceleration for QWebEngineView
2. Local tile caching for Negros Island region
3. Loading map from file instead of injecting HTML
4. Reduced Leaflet map load with frontend optimizations
5. Vector tiles option for better performance
6. Developer tools disabled in production

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenStreetMap for map data
- Leaflet.js for interactive maps
- PyQt5 for the desktop interface
- SQLite for database management
