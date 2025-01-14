import os
import subprocess

def reprojeter_tuile(input_file, output_file):
    """
    Reprojette une seule tuile de WGS84 (EPSG:4326) vers Web Mercator (EPSG:3857).
    """
    # Commande gdalwarp pour reprojeter la tuile
    command = [
        'gdalwarp',
        '-s_srs', 'EPSG:4326',  # Système de coordonnées source (WGS84)
        '-t_srs', 'EPSG:3857',   # Système de coordonnées cible (Web Mercator)
        '-srcnodata', '255',     # Option pour gérer les pixels sans données (si nécessaire)
        '-dstnodata', '255',     # Option pour gérer les pixels sans données (si nécessaire)
        '-of', 'PNG',            # Format de sortie
        '-co', 'TILED=YES',      # Options de compression pour les tuiles (si nécessaire)
        '-src_method', 'NO_GEOTRANSFORM',  # Ajout de l'option pour contourner les erreurs de transformation
        input_file,              # Fichier d'entrée
        output_file              # Fichier de sortie
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Reprojection réussie : {input_file} -> {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur de reprojection pour {input_file}: {e}")

def reprojeter_tuiles_in_dossier(dossier_input, dossier_output):
    """
    Reprojette toutes les tuiles dans un dossier.
    """
    for root, dirs, files in os.walk(dossier_input):
        for file in files:
            # Vérifier que le fichier est une image PNG
            if file.endswith(".png"):
                input_file = os.path.join(root, file)
                relative_path = os.path.relpath(input_file, dossier_input)
                output_file = os.path.join(dossier_output, relative_path)
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                reprojeter_tuile(input_file, output_file)

# Exemple d'utilisation :
dossier_input = './tiles_output'  # Remplacez par le chemin du dossier d'entrée
dossier_output = './tiles_reprojetees'  # Remplacez par le chemin du dossier de sortie
reprojeter_tuiles_in_dossier(dossier_input, dossier_output)

