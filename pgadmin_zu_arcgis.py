import arcpy
import os

# PostgreSQL-Verbindungsinformationen
pg_connection = r"C:\Users\User\Documents\ArcGIS\Projects\MyProject_neues\PostgreSQL-localhost-windenergie(postgres).sde\windenergie.public"  # Pfad zur .sde-Verbindungsdatei
output_gdb = r"C:\Users\User\Desktop\smart_energy_project\MyProject\neues_projekt.gdb"  # Lokale Geodatabase in ArcGIS Pro

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

    # Hinzufügen der Tabellen als Layer in ArcGIS Pro
    for tabelle in tabellen:
        arcpy.management.MakeTableView(os.path.join(output_gdb, tabelle), tabelle)
        print(f"Tabelle {tabelle} wurde als Layer hinzugefügt.")

if __name__ == "__main__":
    main()
