import pandas as pd
from sqlalchemy import create_engine

# Datenbankverbindung einrichten
engine = create_engine('postgresql://postgres:XXXXXXXXX@localhost:5432/windenergie')

def lade_daten():
    """
    Diese Funktion lädt die Daten aus zwei vorhandenen Tabellen (z.B. 'raw_data_1' und 'raw_data_2') in PostgreSQL.
    """
    # Lade die Daten aus der ersten Tabelle
    windparks_raw = pd.read_sql("SELECT * FROM windparks_roh", engine)
    # Lade die Daten aus der zweiten Tabelle
    timeseries_raw = pd.read_sql("SELECT * FROM zeitreihe_roh", engine)
    return windparks_raw, timeseries_raw

def daten_vorverarbeiten(windparks_raw, timeseries_raw):
    """
    Diese Funktion verarbeitet die Daten aus beiden Tabellen separat.
    """
    # Behandle fehlende Werte in den Zeitreihendaten
    timeseries_raw.fillna(method='ffill', inplace=True)
    # Behandle fehlende Werte in den Windkraftanlagedaten
    windparks_proc = windparks_raw.dropna(subset=['electrical_capacity', 'lon', 'lat'])
    timeseries_proc = timeseries_raw.drop(timeseries_raw.index[:5])

    return windparks_proc, timeseries_proc

def daten_speichern(windparks_proc, timeseries_proc):
    """
    Speichert die verarbeiteten Daten in separaten Tabellen in PostgreSQL.
    """
    # Speichert die verarbeiteten Daten aus der ersten Tabelle
    windparks_proc.to_sql('windparks_vva', engine, if_exists='replace', index=False)
    
    # Speichert die verarbeiteten Daten aus der zweiten Tabelle
    timeseries_proc.to_sql('zeitreihe_vva', engine, if_exists='replace', index=False)

def main():
    # Lade Daten aus beiden Tabellen
    windparks_raw, timeseries_raw = lade_daten()
    
    # Daten vorverarbeiten
    windparks_proc, timeseries_proc = daten_vorverarbeiten(windparks_raw, timeseries_raw)
    print("Datenvorverarbeitung abgeschlossen.")
    
    # Verarbeitete Daten getrennt speichern
    daten_speichern(windparks_proc, timeseries_proc)
    print("Verarbeitete Daten wurden erfolgreich in separaten Tabellen gespeichert.")

if __name__ == "__main__":
    main()
