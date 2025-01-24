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

### 3. Visualisierung in ArcGIS Pro

- Konvertierung tabellarischer Daten in räumliche Daten mit `XY Table to Point` und `GPX to Features`.
- Durchführung räumlicher Analysen, z. B. Berechnung der Entfernung zur nächstgelegenen Umspannstation.
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

