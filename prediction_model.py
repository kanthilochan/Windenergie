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
data = pd.read_csv(r"C:\Users\User\Desktop\smart_energy_project\data\Windparks_final\windparks.csv")

# Entfernen von Zeilen mit fehlenden Werten
data = data.dropna()

# Filtern der Daten, um unbekannte Landbedeckung auszuschließen
data = data[data['Landbedeck'] != 'Unknown']

# Entfernen von Duplikaten anhand von Koordinaten- und Merkmalsdaten
data = data.drop_duplicates(subset=['lon', 'lat', 'NEAR_DIST', 'Windgeschwindigkeit', 'Landbedeck'])

# Alle vorhandenen Datensätze als "Geeignet" markieren
data['suitability'] = 'Geeignet'

# Definieren eines Begrenzungsrahmens für das Erzeugen neuer negativer Stichproben
lon_min, lon_max = data['lon'].min() - 0.1, data['lon'].max() + 0.1
lat_min, lat_max = data['lat'].min() - 0.1, data['lat'].max() + 0.1

# Generierung neuer negativer Stichproben mit zufälligen Koordinaten innerhalb des definierten Bereichs
num_new_negative_samples = len(data)
random_lons = np.random.uniform(lon_min, lon_max, num_new_negative_samples)
random_lats = np.random.uniform(lat_min, lat_max, num_new_negative_samples)

# Erstellen eines GeoDataFrame für die negativen Stichproben
new_negative_samples = pd.DataFrame({'lon': random_lons, 'lat': random_lats})
new_negative_samples['geometry'] = new_negative_samples.apply(lambda row: Point(row['lon'], row['lat']), axis=1)
new_negative_samples = gpd.GeoDataFrame(new_negative_samples, geometry='geometry')

# Generierung von Windgeschwindigkeitswerten mit mehr Werten in einem bestimmten Bereich
new_negative_samples['Windgeschwindigkeit'] = np.random.uniform(3.7, 6.5, size=len(new_negative_samples))

# Generierung von Entfernungswerten mit einer Gewichtung auf niedrigere Werte
new_negative_samples['NEAR_DIST'] = np.random.uniform(10, 40, size=len(new_negative_samples))

# Zufällige Zuweisung von Landbedeckungstypen unter Berücksichtigung der Wahrscheinlichkeiten
new_negative_samples['Landbedeck'] = np.random.choice(
    ['Agriculture', 'Built-Up', 'Bare Soil', 'Forest', 'Low Vegetation', 'Water'], 
    size=len(new_negative_samples), p=[0.03, 0.6, 0.03, 0.3, 0.03, 0.01]
)
new_negative_samples['suitability'] = 'Nicht geeignet'

# Zusammenführen der positiven und negativen Stichproben und zufälliges Mischen
combined_data = pd.concat([data, new_negative_samples], ignore_index=True)
combined_data = combined_data.sample(frac=1, random_state=42).reset_index(drop=True)

# Kodierung von Eignung und Landbedeckung in numerische Werte
suitability_encoder = LabelEncoder()
landbedeck_encoder = LabelEncoder()

combined_data['suitability_encoded'] = suitability_encoder.fit_transform(combined_data['suitability'])
combined_data['Landbedeck_encoded'] = landbedeck_encoder.fit_transform(combined_data['Landbedeck'])

# Definition der Merkmale und Zielvariable für das Modell
features = ['NEAR_DIST', 'Windgeschwindigkeit', 'Landbedeck_encoded']
X = combined_data[features].copy()  # Erstellen einer sicheren Kopie der Daten
y = combined_data['suitability_encoded']

# Normalisierung der Merkmale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Aufteilung der Daten in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42, stratify=y)

# Training des Random-Forest-Klassifikators mit optimierten Parametern
model = RandomForestClassifier(random_state=42, max_features='sqrt', n_estimators=200)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Modellbewertung durch Genauigkeit, Berichts- und Verwirrungsmatrix
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=suitability_encoder.classes_)

print("Genauigkeit:", accuracy)
print("\nKlassifikationsbericht:\n", report)

# Ausgabe der Feature-Importance-Werte
importances = model.feature_importances_
for feature, importance in zip(features, importances):
    print(f"Feature: {feature}, Wichtigkeit: {importance:.4f}")

# Flask-App zur Bereitstellung der Vorhersagefunktionalität
app = Flask(__name__)

# Laden von TIF-Dateien für Windgeschwindigkeit und Landbedeckung
wind_speed_tif = rasterio.open(r"C:\Users\User\Desktop\smart_energy_project\Windgeschwindigkeit_DE.tif")
land_cover_tif = rasterio.open(r"C:\Users\User\Desktop\smart_energy_project\landbedeckung.tif")

# Laden der Umspannwerksdaten
substations = gpd.read_file(r"C:\Users\User\Desktop\smart_energy_project\umspannwerke.gpx", layer='waypoints')

# Koordinatentransformation von WGS84 in das Raster-Koordinatensystem
transformer = Transformer.from_crs("epsg:4326", land_cover_tif.crs, always_xy=True)

# Funktion zum Abrufen von Windgeschwindigkeitswerten
def get_raster_value_wind(tif, lat, lon):
    coords = [(lon, lat)]
    values = [x[0] for x in tif.sample(coords)]
    return values[0]

# Funktion zum Abrufen von Landbedeckungswerten
def get_raster_value_landcover(tif, lat, lon):
    coords = [(transformer.transform(lon, lat))]
    values = [x[0] for x in tif.sample(coords)]
    return values[0]

# Berechnung der Entfernung zur nächstgelegenen Umspannstation
def get_nearest_distance(lat, lon):
    user_location = gpd.GeoDataFrame({'geometry': [Point(lon, lat)]}, crs="epsg:4326")
    user_location = user_location.to_crs(epsg=32633)
    substations_projected = substations.to_crs(epsg=32633)
    distances = substations_projected.geometry.distance(user_location.loc[0, 'geometry'])
    return distances.min() / 1000  # Umwandlung in Kilometer

# Flask-Route für die Verarbeitung von Benutzereingaben und Anzeige der Ergebnisse
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        lat = float(request.form['latitude'])
        lon = float(request.form['longitude'])
        suitability_label = predict_suitability(lat, lon)
        return render_template('index.html', suitability_label=suitability_label)
    return render_template('index.html')

# Flask-App starten
if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except SystemExit:
        pass
