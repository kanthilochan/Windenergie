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

GIS Tools: ArcGIS Pro, ArcGIS Online, QGIS

Database Management: PostgreSQL/PostGIS

Automation: Jenkins for workflow automation

Version Control: GitHub

Machine Learning: Scikit-learn for predictive modeling

Deployment: AWS EC2 instance with Flask backend

Project Workflow

1. Data Acquisition:

Wind turbine data from Open Power System Data

Substation locations from Overpass Turbo

Land cover classification from Mundialis

Wind speed data from Global Wind Atlas

2. Data Preprocessing:

Importing raw data into PostgreSQL/PostGIS database using Python scripts.

Cleaning and preprocessing data.

Generating additional features such as distance to substations.

3. Visualization in ArcGIS Pro:

XY Table to Point conversion for wind turbine data.

Distance calculations between turbines and substations.

Land cover and wind speed integration.

Symbolization and pop-up configurations.

Exporting final layers to ArcGIS Online.

4. Machine Learning Model:

Data preparation with feature engineering.

Model training and evaluation using Random Forest Classifier.

Suitability prediction based on distance, wind speed, and land cover type.

5. Web Deployment:

Flask-based web interface for user input and model prediction.

Hosted on AWS EC2 instance.

Users can input latitude and longitude to check site suitability.

How to Run Locally

# Clone the repository
git clone https://github.com/yourusername/wind-energy-analysis.git
cd wind-energy-analysis

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python vorhersagemodell.py

Repository Structure

├── data
│   ├── Windparks_final
│   ├── Windgeschwindigkeit_DE.tif
│   └── landbedeckung.tif
├── scripts
│   ├── zentraler_workflow.py
│   ├── pgadmin_zu_arcgis.py
│   ├── jenkins_workflow.groovy
├── web
│   ├── templates
│   │   ├── eignung_design.html
│   │   ├── haupt_design.html
│   ├── aws.py
├── README.md
├── requirements.txt
└── Vorhersagemodell.py

Contribution

Contributions are welcome! Feel free to fork the repository and submit pull requests.

Contact

For any inquiries, please contact: kanthilochanmuppalla@gmail.com

