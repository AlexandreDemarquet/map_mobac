import sqlite3
import os

# Chemin vers le fichier MBTiles
mbtiles_path = './map_med.mbtiles'

# Créer un dossier pour les tuiles extraites
output_dir = 'tiles_output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Connexion à la base de données MBTiles
conn = sqlite3.connect(mbtiles_path)
cursor = conn.cursor()

# Récupérer toutes les tuiles du fichier MBTiles
cursor.execute("SELECT zoom_level, tile_column, tile_row, tile_data FROM tiles")

# Extraire les tuiles et les enregistrer dans un répertoire
for zoom, col, row, tile in cursor.fetchall():
    # Créer un dossier pour chaque niveau de zoom et chaque colonne de tuile
    tile_dir = os.path.join(output_dir, str(zoom), str(col))
    if not os.path.exists(tile_dir):
        os.makedirs(tile_dir)

    # Chemin de la tuile
    tile_filename = os.path.join(tile_dir, f"{row}.png")
    
    # Enregistrer la tuile sur le disque
    with open(tile_filename, 'wb') as f:
        f.write(tile)

# Fermer la connexion à la base de données
conn.close()

