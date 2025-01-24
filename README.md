# Wind Energy Suitability Analysis in Germany

## Overview

This project aims to analyze and visualize wind energy potential across Germany by integrating geospatial data and machine learning techniques. The project involves data collection, preprocessing, visualization, spatial analysis, training of a machine learning model, and deployment of a web-based suitability checker.

## Objectives

- **Data Collection:** Wind turbines, substations, land cover classification, and wind speed data.
- **Data Processing:** Using PostgreSQL/PostGIS and GitHub for data storage and retrieval.
- **Visualization:** Leveraging ArcGIS Pro for spatial analysis and ArcGIS Online for web visualization.
- **Machine Learning:** Developing a site suitability model for wind turbine installation.
- **Web Deployment:** Building a web-based user interface using Flask and deploying on AWS.

## Technologies Used

- **Programming Languages:** Python, HTML, CSS
- **GIS Tools:** ArcGIS Pro, ArcGIS Online, QGIS
- **Database Management:** PostgreSQL/PostGIS
- **Automation:** Jenkins for workflow automation
- **Version Control:** GitHub
- **Machine Learning:** Scikit-learn for predictive modeling
- **Deployment:** AWS EC2 instance with Flask backend

## Project Workflow

### 1. Data Acquisition

- Wind turbine data from [Open Power System Data](https://data.open-power-system-data.org/renewable_power_plants/)
- Substation locations from Overpass Turbo
- Land cover classification from [Mundialis](https://www.mundialis.de/en/germany-2020-land-cover-based-on-sentinel-2-data/)
- Wind speed data from [Global Wind Atlas](https://globalwindatlas.info/en/area/Germany)

### 2. Data Preprocessing

- Importing raw data into PostgreSQL/PostGIS database using Python scripts.
- Cleaning and preprocessing data.
- Generating additional features such as distance to substations.

### 3. Visualization in ArcGIS Pro

- Converting tabular data to spatial data using `XY Table to Point` and `GPX to Features`.
- Performing spatial analysis such as nearest substation distance.
- Configuring pop-ups and symbology for better insights.
- Exporting final layers to ArcGIS Online for public sharing.

### 4. Machine Learning Model

- Preparing data with feature engineering.
- Training and evaluating a Random Forest Classifier model.
- Predicting site suitability based on wind speed, land cover, and distance.

### 5. Web Deployment

- Developing a web-based interface using Flask.
- Integrating model predictions with user input.
- Hosting the web application on AWS EC2.

## How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/wind-energy-analysis.git
   cd wind-energy-analysis
