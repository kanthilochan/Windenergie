import os
import requests
import arcpy

# PostgreSQL-Verbindungsinformationen
pg_connection = r"C:\Users\User\Documents\ArcGIS\Projects\MyProject_neues\PostgreSQL-localhost-windenergie(postgres).sde\windenergie.public"
output_gdb = r"C:\Users\User\Documents\ArcGIS\Projects\MyProject_neues\MyProject_neues.gdb"

# Zielverzeichnisse für Dateien
tif_folder = r"C:\Users\User\Documents\ArcGIS\Projects\MyProject_neues\TIF_Files"
gpx_folder = r"C:\Users\User\Documents\ArcGIS\Projects\MyProject_neues\GPX_Files"

# Personal Access Token (PAT) für GitHub
GITHUB_TOKEN = "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"

def lade_daten_aus_pg(tabellen, gdb):
    """Lädt Tabellen aus PostgreSQL in eine Geodatabase."""
    for tabelle in tabellen:
        out_table = os.path.join(gdb, tabelle)
        # Prüfen, ob die Tabelle bereits existiert, und löschen, falls ja
        if arcpy.Exists(out_table):
            arcpy.management.Delete(out_table)
        arcpy.conversion.TableToTable(f"{pg_connection}.{tabelle}", gdb, tabelle)
        print(f"{tabelle} wurde abgerufen und gespeichert.")

def lade_dateien_von_github(repo_owner, repo_name, ordner, zielverzeichnisse, branch="main"):
    """Lädt Dateien aus einem angegebenen GitHub-Ordner herunter."""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{ordner}?ref={branch}"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Fehler beim Abrufen der GitHub-Dateien: {response.status_code}, {response.text}")
    
    files = response.json()
    if not isinstance(files, list):
        raise Exception("Unerwartete Antwortstruktur von GitHub. Überprüfen Sie den Ordnerpfad.")
    
    for file in files:
        if file['name'] == 'Windgeschwindigkeit_DE.tif':
            zielpfad = os.path.join(zielverzeichnisse['tif'], file['name'])
        elif file['name'] == 'umspannwerke.gpx':
            zielpfad = os.path.join(zielverzeichnisse['gpx'], file['name'])
        else:
            continue

        with open(zielpfad, 'wb') as f:
            f.write(requests.get(file['download_url'], headers=headers).content)
        print(f"{file['name']} wurde heruntergeladen.")

def main():
    os.makedirs(tif_folder, exist_ok=True)
    os.makedirs(gpx_folder, exist_ok=True)

    lade_daten_aus_pg(['windparks_vva', 'zeitreihe_vva'], output_gdb)
    lade_dateien_von_github(
        repo_owner="kanthilochan",
        repo_name="Windenergie",
        ordner="Daten",
        zielverzeichnisse={'tif': tif_folder, 'gpx': gpx_folder}
    )

if __name__ == "__main__":
    main()
