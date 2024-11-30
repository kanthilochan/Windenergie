import arcpy
import os

# PostgreSQL-Verbindungsinformationen
pg_connection = r"C:\Users\User\Documents\ArcGIS\Projects\MyProject_neues\PostgreSQL-localhost-windenergie(postgres).sde\windenergie.public"  # Pfad zur .sde-Verbindungsdatei
output_gdb = r"C:\Users\User\Documents\ArcGIS\Projects\MyProject_neues\MyProject_neues.gdb"  # Lokale Geodatabase in ArcGIS Pro

def lade_daten_aus_pg(tabellen, gdb):
    """
    Lädt Tabellen aus PostgreSQL in eine Geodatabase.
    """
    for tabelle in tabellen:
        in_table = f"{pg_connection}.{tabelle}"  # Datenbanktabelle
        out_table = os.path.join(gdb, tabelle)  # Ziel-GDB-Tabelle

        # Prüfen, ob die Ausgabe bereits existiert
        if arcpy.Exists(out_table):
            print(f"{out_table} existiert bereits. Es wird gelöscht...")
            arcpy.management.Delete(out_table)

        print(f"Lade {tabelle} in {out_table}...")
        arcpy.conversion.TableToTable(in_table, gdb, tabelle)
    print("Tabellen wurden erfolgreich in die Geodatabase geladen.")

def main():
    # Tabellen, die geladen werden sollen
    tabellen = ['windparks_vva', 'zeitreihe_vva']

    # Daten in die Geodatabase laden
    lade_daten_aus_pg(tabellen, output_gdb)

    # ArcGIS Pro-Projektpfad (aktuelle .aprx-Datei)
    project_path = r"C:\Users\User\Documents\ArcGIS\Projects\MyProject_neues\MyProject_neues.aprx"

    # Projekt öffnen
    aprx = arcpy.mp.ArcGISProject(project_path)

    # **Debugging: Alle Karten im Projekt auflisten**
    print(f"Karten im Projekt: {[m.name for m in aprx.listMaps()]}")

    # Erste Karte auswählen
    map_view = aprx.listMaps()[0]
    print(f"Ausgewählte Karte: {map_view.name}")

    # Hinzufügen der Tabellen als Layer in die Karte
    for tabelle in tabellen:
        layer_path = os.path.join(output_gdb, tabelle)
        print(f"Versuche, Tabelle {tabelle} als Layer hinzuzufügen. Pfad: {layer_path}")

        # Layer hinzufügen
        map_view.addDataFromPath(layer_path)
        print(f"Tabelle {tabelle} wurde als Layer in die Karte hinzugefügt.")

        # **Debugging: Layer nach Hinzufügen auflisten**
        print(f"Layer in der Karte nach Hinzufügen: {[layer.name for layer in map_view.listLayers()]}")

        # Layer sichtbar machen
        try:
            layer = next(layer for layer in map_view.listLayers() if tabelle in layer.name)
            layer.visible = True
            print(f"Layer {layer.name} wurde sichtbar gemacht.")
        except StopIteration:
            print(f"Fehler: Layer für Tabelle {tabelle} wurde nicht gefunden.")

    # Projekt speichern
    try:
        aprx.save()
        print("Projekt wurde erfolgreich gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern des Projekts: {e}")

if __name__ == "__main__":
    main()
