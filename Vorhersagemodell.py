import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import geopandas as gpd
from shapely.geometry import Point
import rasterio
from pyproj import Transformer
import matplotlib.pyplot as plt
from flask import Flask, request, render_template

# Datensatz laden
data = pd.read_csv("/home/ec2-user/C/Users/User/Desktop/smart_energy_project/data/Windparks_final/windparks.csv")

data = data.dropna()  # Entfernen von fehlenden Werten
data = data[data['Landbedeck'] != 'Unknown']  # Entfernen von Zeilen mit unbekannter Landbedeckung
data = data.drop_duplicates(subset=['lon', 'lat', 'NEAR_DIST', 'Windgeschwindigkeit', 'Landbedeck'])  # Entfernen von Duplikaten
data['suitability'] = 'Geeignet'  # Alle vorhandenen Stichproben als geeignet markieren

# Begrenzungsrahmen für die Generierung neuer negativer Stichproben definieren
lon_min, lon_max = data['lon'].min() - 0.1, data['lon'].max() + 0.1
lat_min, lat_max = data['lat'].min() - 0.1, data['lat'].max() + 0.1

# Generierung neuer negativer Stichproben (gleiche Anzahl wie positive Stichproben)
num_new_negative_samples = len(data)
random_lons = np.random.uniform(lon_min, lon_max, num_new_negative_samples)
random_lats = np.random.uniform(lat_min, lat_max, num_new_negative_samples)

# Erstellung einer GeoDataFrame für neue negative Stichproben
new_negative_samples = pd.DataFrame({'lon': random_lons, 'lat': random_lats})
new_negative_samples['geometry'] = new_negative_samples.apply(lambda row: Point(row['lon'], row['lat']), axis=1)
new_negative_samples = gpd.GeoDataFrame(new_negative_samples, geometry='geometry')

# Simulation realistischer Windgeschwindigkeiten und Entfernungen
new_negative_samples['Windgeschwindigkeit'] = np.random.uniform(3.7, 6.5, size=len(new_negative_samples))
new_negative_samples['NEAR_DIST'] = np.random.uniform(10, 40, size=len(new_negative_samples))
new_negative_samples['Landbedeck'] = np.random.choice(['Agriculture', 'Built-Up', 'Bare Soil', 'Forest', 'Low Vegetation', 'Water'], 
                                                      size=len(new_negative_samples), p=[0.03, 0.6, 0.03, 0.3, 0.03, 0.01])
new_negative_samples['suitability'] = 'Nicht geeignet'

# Alle Stichproben kombinieren und mischen
combined_data = pd.concat([data, new_negative_samples], ignore_index=True)
combined_data = combined_data.sample(frac=1, random_state=42).reset_index(drop=True)

# Kodierung der Eignung und der Landbedeckung
suitability_encoder = LabelEncoder()
landbedeck_encoder = LabelEncoder()
combined_data['suitability_encoded'] = suitability_encoder.fit_transform(combined_data['suitability'])
combined_data['Landbedeck_encoded'] = landbedeck_encoder.fit_transform(combined_data['Landbedeck'])

# Definition der Merkmale und Zielvariable
features = ['NEAR_DIST', 'Windgeschwindigkeit', 'Landbedeck_encoded']
X = combined_data[features].copy()
y = combined_data['suitability_encoded']

# Standardisierung der Merkmale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Aufteilung in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42, stratify=y)

# Modelltraining mit RandomForestClassifier
model = RandomForestClassifier(random_state=42, max_features='sqrt', n_estimators=200)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Modellauswertung
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=suitability_encoder.classes_)
print("Genauigkeit:", accuracy)
print("\nKlassifikationsbericht:\n", report)

# Darstellung der Konfusionsmatrix
cm = confusion_matrix(y_test, y_pred)
print("\nKonfusionsmatrix:\n", cm)

# Anzeige der Feature-Importances
importances = model.feature_importances_
for feature, importance in zip(features, importances):
    print(f"Merkmal: {feature}, Wichtigkeit: {importance:.4f}")

# Flask-Anwendung initialisieren
app = Flask(__name__)

# Laden der TIF-Dateien
wind_speed_tif = rasterio.open("/home/ec2-user/C/Users/User/Desktop/smart_energy_project/Windgeschwindigkeit_DE.tif")
land_cover_tif = rasterio.open("/home/ec2-user/C/Users/User/Desktop/smart_energy_project/landbedeckung.tif")

# Laden der Umspannwerke
substations = gpd.read_file("/home/ec2-user/C/Users/User/Desktop/smart_energy_project/umspannwerke.gpx", layer='waypoints')

# Erstellung eines Transformationsobjekts von WGS84 (lat/lon) in das Koordinatensystem des Rasterbildes
transformer = Transformer.from_crs("epsg:4326", land_cover_tif.crs, always_xy=True)

# Funktionen zur Extraktion von Rasterwerten
def get_raster_value_wind(tif, lat, lon):
    coords = [(lon, lat)]
    values = [x[0] for x in tif.sample(coords)]
    return values[0]

def get_raster_value_landcover(tif, lat, lon):
    coords = [(transformer.transform(lon, lat))]
    values = [x[0] for x in tif.sample(coords)]
    return values[0]

# Funktion zur Berechnung der Entfernung zur nächstgelegenen Umspannstation
def get_nearest_distance(lat, lon):
    # Umwandlung des Benutzerstandorts in ein GeoDataFrame
    user_location = gpd.GeoDataFrame({'geometry': [Point(lon, lat)]}, crs="epsg:4326")
    
    # Reprojektion des Benutzerstandorts und der Umspannwerke in UTM (z. B. EPSG:32633)
    user_location = user_location.to_crs(epsg=32633)
    substations_projected = substations.to_crs(epsg=32633)
    
    # Berechnung der Entfernung zu jeder Umspannstation und Rückgabe der minimalen Entfernung
    distances = substations_projected.geometry.distance(user_location.loc[0, 'geometry'])
    return distances.min() / 1000  # Umrechnung von Metern in Kilometer

# Definition der Landbedeckungsklassen
land_cover_mapping = {
    10: 'Forest',
    20: 'Low Vegetation',
    30: 'Water',
    40: 'Built-Up',
    50: 'Bare Soil',
    60: 'Agriculture'
}

# Funktion zur Eignungsvorhersage
def predict_suitability(lat, lon):
    wind_speed = get_raster_value_wind(wind_speed_tif, lat, lon)
    land_cover_class = get_raster_value_landcover(land_cover_tif, lat, lon)
    nearest_distance = get_nearest_distance(lat, lon)
    land_cover_name = land_cover_mapping.get(land_cover_class, 'Unknown')

    if wind_speed >= 8 and land_cover_name in ['Agriculture', 'Low Vegetation', 'Bare Soil'] and nearest_distance <= 5:
        return "Sehr geeignet"
    elif land_cover_name == 'Water':
        return "Nicht geeignet"
    elif land_cover_name == 'Built-Up' and (wind_speed <7.5 or nearest_distance >2):
        return "Nicht geeignet"
    elif land_cover_name == 'Unknown':
        print(f"Unbekannte Landbedeckungsklasse: {land_cover_class}. Standardmäßig nicht geeignet.")
        return "Nicht geeignet"
    else:
        land_cover_encoded = landbedeck_encoder.transform([land_cover_name])[0]
        input_data = pd.DataFrame([[nearest_distance, wind_speed, land_cover_encoded]], columns=['NEAR_DIST', 'Windgeschwindigkeit', 'Landbedeck_encoded'])
        input_scaled = scaler.transform(input_data)
        predicted_class = model.predict(input_scaled)
        return suitability_encoder.inverse_transform(predicted_class)[0]

# Übersetzung der Landbedeckungsklassen und Eignungsbezeichnungen
translations = {
    'Agriculture': 'Landwirtschaft',
    'Built-Up': 'Bebaut',
    'Bare Soil': 'Nackter Boden',
    'Forest': 'Wald',
    'Low Vegetation': 'Niedrige Vegetation',
    'Water': 'Wasser'
}     

# Flask-Route zur Verarbeitung von Benutzereingaben und Anzeige der Ergebnisse
@app.route('/', methods=['GET', 'POST'])
def index():
    suitability_label = None
    wind_speed = None
    land_cover_name = None
    nearest_distance = None

    if request.method == 'POST':
        lat = float(request.form['latitude'])
        lon = float(request.form['longitude'])

        suitability_label = predict_suitability(lat, lon)
        wind_speed = round(get_raster_value_wind(wind_speed_tif, lat, lon), 4)
        land_cover_class = get_raster_value_landcover(land_cover_tif, lat, lon)
        land_cover_name = land_cover_mapping.get(land_cover_class, 'Unknown')
        nearest_distance = round(get_nearest_distance(lat, lon), 4)

        # Übersetzung der Ausgabewerte ins Deutsche
        land_cover_name = translations.get(land_cover_name, land_cover_name)

    return render_template('index.html', 
                           suitability_label=suitability_label, 
                           wind_speed=wind_speed, 
                           land_cover_name=land_cover_name, 
                           nearest_distance=nearest_distance)

# Starten der Flask-Anwendung
if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except SystemExit:
        pass
