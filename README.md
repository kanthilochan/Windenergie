Wind Energy Suitability Analysis in Germany

Overview

This project aims to analyze and visualize wind energy potential across Germany by integrating geospatial data and machine learning techniques. The project involves data collection, preprocessing, visualization, spatial analysis, training of a machine learning model, and deployment of a web-based suitability checker.

Objectives

Data Collection: Wind turbines, substations, land cover classification, and wind speed data.

Data Processing: Using PostgreSQL/PostGIS and GitHub for data storage and retrieval.

Visualization: Leveraging ArcGIS Pro for spatial analysis and ArcGIS Online for web visualization.

Machine Learning: Developing a site suitability model for wind turbine installation.

Web Deployment: Building a web-based user interface using Flask and deploying on AWS.

Technologies Used

Programming Languages: Python, HTML, CSS

GIS Tools: ArcGIS Pro, ArcGIS Online

Database Management: PostgreSQL/PostGIS

Automation: Jenkins for workflow automation

Version Control: GitHub

Machine Learning: Scikit-learn for predictive modeling

Deployment: AWS EC2 instance with Flask backend

Project Workflow

Data Acquisition:

Wind turbine data from Open Power System Data

Substation locations from Overpass Turbo

Land cover classification from Mundialis

Wind speed data from Global Wind Atlas

Data Preprocessing:

Importing raw data into PostgreSQL/PostGIS database using Python scripts.

Cleaning and preprocessing data.

Automation with Jenkins:

Automating data retrieval from GitHub and PostgreSQL/PostGIS.

Processing data and storing results back in the database.

Loading processed data into ArcGIS Pro for visualization.

Visualization in ArcGIS Pro:

XY Table to Point conversion for wind turbine data.

Distance calculations between turbines and substations.

Land cover and wind speed integration.

Symbolization and pop-up configurations.

Exporting final layers to ArcGIS Online.

Machine Learning Model:

Data preparation with feature engineering.

Model training and evaluation using Random Forest Classifier.

Suitability prediction based on distance to nearest substation, wind speed, and land cover type.

Web Deployment:

Flask-based web interface for user input and model prediction.

Hosted on AWS EC2 instance.

Users can see the visualizations of wind turbines and substations and also can input latitude and longitude to check site suitability for wind turbine installation.
