# Site Analysis for Wind Energy in Germany

## Overview

This project aims to analyze and visualize wind energy potential in Germany by integrating geospatial data and machine learning techniques. The project includes data collection, preprocessing, visualization, spatial analysis, training of a machine learning model, and deployment of a web-based suitability checker.

## Objectives

- **Data Collection:** Wind farms, substations, land cover, and wind speed data.
- **Data Processing:** Using PostgreSQL/PostGIS and GitHub for data storage and retrieval.
- **Visualization:** Utilizing ArcGIS Pro for spatial analysis and ArcGIS Online for web visualization.
- **Machine Learning:** Developing a model to assess site suitability for wind farms.
- **Web Deployment:** Building a web-based user interface using Flask and deploying it on AWS.

## Technologies Used

- **Programming Languages:** Python, HTML, CSS
- **GIS Tools:** ArcGIS Pro, ArcGIS Online
- **Database Management:** PostgreSQL/PostGIS
- **Automation:** Jenkins for workflow automation
- **Version Control:** GitHub
- **Machine Learning:** Scikit-learn for predictive modeling
- **Deployment:** AWS EC2 instance with Flask backend

## Project Workflow

### 1. Data Collection

- Wind farm data from [Open Power System Data](https://data.open-power-system-data.org/renewable_power_plants/)
- Substation locations from [Overpass Turbo](https://overpass-turbo.eu/)
- Land cover classification from [Mundialis](https://www.mundialis.de/en/germany-2020-land-cover-based-on-sentinel-2-data/)
- Wind speed data from [Global Wind Atlas](https://globalwindatlas.info/en/area/Germany)

### 2. Data Processing

- Importing raw data into PostgreSQL/PostGIS using Python scripts.
- Cleaning and preprocessing the data.

### 3. Processing, Analyzing, and Visualizing Spatial Data in ArcGIS Pro

- Processing, analyzing, and visualizing geospatial data in ArcGIS Pro using tools such as "Define Projection," "Clip," "Union," "Spatial Join," "Near," "Extract Multi Values to Points," "XY Table to Point," "GPX to Features," "Intersect," "Calculate," "Symbology," and "Configure Pop-ups."
- Configuring pop-ups and symbology for better insights.
- Exporting final layers to ArcGIS Online for public access.

### 4. Machine Learning Model

- Data preparation with feature engineering.
- Training and evaluating a Random Forest classifier.
- Predicting site suitability based on wind speed, land cover, and distance.

### 5. Web Deployment

- Developing a web-based user interface using Flask.
- Integrating model predictions with user input.
- Hosting the web application on an AWS EC2 instance.

---

## Code Explanation

### 1. `central_workflow.py`
This script automates the data retrieval from the PostgreSQL/PostGIS database, processes wind power and time-series data, and stores the processed results back in the database.

### 2. `data_retrieval_in_arcgis.py`
This script loads preprocessed data from PostgreSQL/PostGIS and GitHub into ArcGIS Pro for visualizations and further spatial analysis.

### 3. `jenkins_workflow`
A Jenkins pipeline script automating the workflow implemented in `central_workflow.py` and `data_retrieval_in_arcgis.py`.

### 4. `prediction_model.py`
This script trains a machine learning model using Random Forest to predict the suitability of locations for wind farms based on wind speed, land cover, and distance to substations and sets up the Flask web application.

### 5. `aws.py`
This script deploys the Flask web application on an AWS EC2 instance, making the suitability checker and visualizations accessible online.

### 6. `suitability_design.html`
The HTML file used to create the user interface where users can enter latitude and longitude to check site suitability.

### 7. `main_design.html`
The main webpage providing links to ArcGIS visualizations and the suitability checker.

---

## Live Web Application

Click [here](http://18.199.174.181:5001/) to access **visualizations of wind farms and substations in Germany with additional details** and the **Wind Energy Suitability Checker**, where you can enter latitude and longitude to evaluate the feasibility of installing wind turbines at a specific location.

**Use Cases of the Web Application:**
- Evaluating site suitability based on wind speed, land cover, and distance to substations.
- Accessing interactive visualizations of wind farms and substations in Germany.
- Gaining insights into renewable energy potential for decision-making.

---

## Future Research and Improvements

- **Considering Additional Factors:** Integrating environmental factors such as air quality, soil conditions, and grid connection feasibility to enhance site analysis.
- **Expanding Training Data:** Incorporating manual labeling strategies and additional datasets to improve model accuracy and robustness.
- **Exploring Deep Learning Models:** Investigating deep learning approaches like Convolutional Neural Networks (CNNs) for more precise classification and site assessment.
- **Improving Visualizations:** Developing more interactive and user-friendly web maps with enhanced filtering and analysis functionalities.
- **Optimizing Data Processing Pipeline:** Implementing more efficient ETL processes for improved data processing and delivery.
- **Scalability and Performance:** Evaluating cloud-based solutions for more efficient scaling and processing of large datasets.
- **Integrating New Data Sources:** Incorporating real-time weather data for dynamic site assessment and decision support.
- **Expanding the Web Platform:** Adding new features to enhance user experience, such as integrating user feedback mechanisms or export functions.
