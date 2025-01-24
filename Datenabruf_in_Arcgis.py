import os
import requests
import arcpy

# Verbindungsinformationen
pg_connection = r"C:\Users\User\Documents\ArcGIS\Projects\MyProject_neues\PostgreSQL-localhost-windenergie(postgres).sde\windenergie.public"
output_gdb = r"C:\Users\User\Documents\ArcGIS\Projects\MyProject_neues\MyProject_neues.gdb"
tif_folder = r"C:\Users\User\Documents\ArcGIS\Projects\MyProject_neues\TIF_Files"
gpx_folder = r"C:\Users\User\Documents\ArcGIS\Projects\MyProject_neues\GPX_Files"
GITHUB_TOKEN = "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"

def lade_daten_aus_pg(tabellen, gdb):
    for tabelle in tabellen:
        out_table = os.path.join(gdb, tabelle)
        if arcpy.Exists(out_table):
            arcpy.management.Delete(out_table)
        arcpy.conversion.TableToTable(f"{pg_connection}.{tabelle}", gdb, tabelle)

def lade_dateien_von_github(repo_owner, repo_name, ordner, zielverzeichnisse, branch="main"):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{ordner}?ref={branch}"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    files = requests.get(url, headers=headers).json()
    for file in files:
        if file['name'] == 'Windgeschwindigkeit_DE.tif':
            pfad = os.path.join(zielverzeichnisse['tif'], file['name'])
        elif file['name'] == 'umspannwerke.gpx':
            pfad = os.path.join(zielverzeichnisse['gpx'], file['name'])
        else:
            continue
        with open(pfad, 'wb') as f:
            f.write(requests.get(file['download_url'], headers=headers).content)

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
