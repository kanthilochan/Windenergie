## (Please scroll down for English version)
# Standortanalyse für Windenergie in Deutschland

## Überblick

Dieses Projekt zielt darauf ab, das Windenergiepotenzial in Deutschland durch die Integration von Geodaten und maschinellen Lerntechniken zu analysieren und zu visualisieren. Das Projekt umfasst die Datenerfassung, Vorverarbeitung, Visualisierung, räumliche Analyse, das Training eines Machine-Learning-Modells und die Bereitstellung eines webbasierten Eignungsprüfers.

## Ziele

- **Datenerfassung:** Windkraftanlagen, Umspannwerke, Landbedeckung und Windgeschwindigkeitsdaten.
- **Datenverarbeitung:** Verwendung von PostgreSQL/PostGIS und GitHub zur Speicherung und Abruf von Daten.
- **Visualisierung:** Nutzung von ArcGIS Pro für räumliche Analysen und ArcGIS Online für Web-Visualisierung.
- **Maschinelles Lernen:** Entwicklung eines Modells zur Bewertung der Standorttauglichkeit für Windkraftanlagen.
- **Webbereitstellung:** Entwicklung einer webbasierten Benutzeroberfläche mit Flask und Bereitstellung auf AWS.

## Verwendete Technologien

- **Programmiersprachen:** Python, HTML, CSS
- **GIS-Tools:** ArcGIS Pro, ArcGIS Online
- **Datenbankverwaltung:** PostgreSQL/PostGIS
- **Automatisierung:** Jenkins für die Workflow-Automatisierung
- **Versionskontrolle:** GitHub
- **Maschinelles Lernen:** Scikit-learn für prädiktive Modellierung
- **Bereitstellung:** AWS EC2-Instanz mit Flask-Backend

## Projektablauf

### 1. Datenerfassung

- Windkraftanlagendaten von [Open Power System Data](https://data.open-power-system-data.org/renewable_power_plants/)
- Umspannwerk-Standorte von [Overpass Turbo](https://overpass-turbo.eu/)
- Landbedeckungsklassifikation von [Mundialis](https://www.mundialis.de/en/germany-2020-land-cover-based-on-sentinel-2-data/)
- Windgeschwindigkeitsdaten vom [Global Wind Atlas](https://globalwindatlas.info/en/area/Germany)

### 2. Datenverarbeitung

- Importieren der Rohdaten in die PostgreSQL/PostGIS-Datenbank mit Python-Skripten.
- Bereinigung und Vorverarbeitung der Daten.

### 3. Verarbeitung, Analyse und Visualisierung räumlicher Daten in Arcgis Pro

- Verarbeitung, Analyse und Visualisierung von Geodaten in ArcGIS Pro unter Verwendung von Werkzeugen wie „Projektion definieren“ (Define Projection), „Zuschnitt“ (Clip), 
  „Vereinigung“ (Union), „Räumliches Verbinden“ (Spatial Join), „Nähe“ (Near), „Mehrfachwerte zu Punkten extrahieren“ (Extract Multi Values to Points), „XY-Tabelle in Punkt 
  konvertieren“ (XY Table to Point), „GPX zu Features“ (GPX to Features), „Überschneidung“ (Intersect), „Berechnung“ (Calculate), „Symbolisierung“ (Symbology) und „Pop-ups 
  konfigurieren“ (Configure Pop-ups).
- Konfiguration von Pop-ups und Symbolisierung für bessere Einblicke.
- Export der endgültigen Layer nach ArcGIS Online zur öffentlichen Freigabe.

### 4. Maschinelles Lernmodell

- Datenaufbereitung mit Feature Engineering.
- Training und Evaluierung eines Random-Forest-Klassifikators.
- Vorhersage der Standorttauglichkeit basierend auf Windgeschwindigkeit, Landbedeckung und Entfernung.

### 5. Webbereitstellung

- Entwicklung einer webbasierten Benutzeroberfläche mit Flask.
- Integration von Modellvorhersagen mit Benutzereingaben.
- Hosting der Webanwendung auf einer AWS EC2-Instanz.

---

## Code-Erklärung

### 1. `zentraler_workflow.py`
Dieses Skript automatisiert die Datenabfrage aus der PostgreSQL/PostGIS-Datenbank, verarbeitet die Windkraft- und Zeitreihendaten und speichert die verarbeiteten Ergebnisse zurück in die Datenbank.

### 2. `Datenabruf_in_Arcgis.py` 
Dieses Skript lädt vorverarbeitete Daten aus PostgreSQL/PostGIS und GitHub in ArcGIS Pro, um Visualisierungen und weitere räumliche Analysen zu ermöglichen.

### 3. `Jenkins_workflow`
Ein Jenkins-Pipeline-Skript, das den gesamten Workflow automatisiert, der durch die Dateien `zentraler_workflow.py` und `Datenabruf_in_Arcgis.py` implementiert wurde.

### 4. `vorhersagemodell.py`
Dieses Skript trainiert ein Machine-Learning-Modell mit Random Forest, um die Eignung von Standorten für Windkraftanlagen basierend auf Windgeschwindigkeit, Landbedeckung und Entfernung zu Umspannwerken vorherzusagen und richtet die Flask-Webanwendung ein.

### 5. `aws.py`
Dieses Skript stellt die Flask-Webanwendung auf einer AWS EC2-Instanz bereit, um den Eignungsprüfer und Visualisierungen online für die Öffentlichkeit zugänglich zu machen.

### 6. `eignung_design.html`
Die HTML-Datei, die für die Erstellung der Benutzeroberfläche verwendet wird, in der Benutzer Breitengrad und Längengrad eingeben können, um die Standorttauglichkeit zu prüfen.

### 7. `haupt_design.html`
Die Hauptwebseite, die Links zu den ArcGIS-Visualisierungen und dem Eignungsprüfer bereitstellt.

---

## Live-Webanwendung

Klicken Sie [hier](http://18.199.174.181:5001/), um auf die **Visualisierungen von Windkraftanlagen und Umspannwerken in Deutschland mit weiteren Details** und den **Windenergie-Eignungsprüfer** zuzugreifen, wo Sie Breitengrad und Längengrad eingeben können, um die Machbarkeit der Installation von Windkraftanlagen an einem bestimmten Standort zu bewerten.

**Verwendungszwecke der Webanwendung:**
- Bewertung der Standorttauglichkeit basierend auf Windgeschwindigkeit, Landbedeckung und Entfernung zu Umspannwerken.
- Zugriff auf interaktive Visualisierungen von Windkraftanlagen und Umspannwerken in Deutschland.
- Gewinnung von Erkenntnissen über das Potenzial erneuerbarer Energien für Entscheidungsfindungen.

---

## Zukünftige Forschung und Verbesserungsmöglichkeiten

- **Berücksichtigung zusätzlicher Faktoren:** Integration weiterer Umweltfaktoren wie Luftqualität, Bodenbeschaffenheit und Netzanschlussmöglichkeiten zur Verbesserung der Standortanalyse.
- **Erweiterung der Trainingsdaten:** Manuelle Labeling-Strategien und Nutzung zusätzlicher Datensätze zur Verbesserung der Modellgenauigkeit und -robustheit.
- **Erkundung tieferer Lernmodelle:** Untersuchung von Deep-Learning-Ansätzen wie Convolutional Neural Networks (CNNs) zur präziseren Klassifizierung und Standortbewertung.
- **Verbesserung der Visualisierungen:** Entwicklung interaktiverer und benutzerfreundlicherer Webkarten mit erweiterten Filter- und Analysefunktionen.
- **Optimierung der Datenverarbeitungspipeline:** Einführung effizienterer ETL-Prozesse für eine verbesserte Datenverarbeitung und -bereitstellung.
- **Skalierbarkeit und Leistung:** Evaluierung von Cloud-Lösungen für eine effizientere Skalierung und Verarbeitung großer Datenmengen.
- **Integration neuer Datenquellen:** Einbindung von Echtzeit-Wetterdaten zur dynamischen Standortbewertung und Entscheidungsunterstützung.
- **Erweiterung der Webplattform:** Hinzufügen neuer Features zur besseren Nutzererfahrung, z. B. Integration von Benutzerfeedback-Mechanismen oder Exportfunktionen.



----------



## (English version starts from here)
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


