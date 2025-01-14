import os
import subprocess

def reprojeter_tuile(input_file, output_file):
    """
    Reprojette une seule tuile de WGS84 (EPSG:4326) vers Web Mercator (EPSG:3857).
    """
    print(f"Traitement de la tuile: {input_file} -> {output_file}")
    
    # Commande gdalwarp pour reprojeter la tuile
    command = [
        'gdalwarp',
        '-s_srs', 'EPSG:4326',  # Système de coordonnées source (WGS84)
        '-t_srs', 'EPSG:3857',   # Système de coordonnées cible (Web Mercator)
        '-srcnodata', '255',     # Option pour gérer les pixels sans données (si nécessaire)
        '-dstnodata', '255',     # Option pour gérer les pixels sans données (si nécessaire)
        '-of', 'PNG',            # Format de sortie
        '-co', 'TILED=YES',      # Options de compression pour les tuiles (si nécessaire)
        '-co', 'SRC_METHOD=NO_GEOTRANSFORM',  # Force la non-transformation géographique
        input_file,              # Fichier d'entrée
        output_file              # Fichier de sortie
    ]

    try:
        # Exécution de la commande et capture des erreurs
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Reprojection réussie : {input_file} -> {output_file}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur de reprojection pour {input_file}: {e}")
        print(f"STDERR: {e.stderr}")
        print(f"STDOUT: {e.stdout}")

def reprojeter_tuiles_in_dossier(dossier_input, dossier_output):
    """
    Reprojette toutes les tuiles dans un dossier.
    """
    for root, dirs, files in os.walk(dossier_input):
        for file in files:
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

