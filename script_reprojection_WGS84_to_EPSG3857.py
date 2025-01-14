import os
import subprocess

# Fonction pour reprojeter une tuile à l'aide de gdalwarp
def reprojeter_tuile(input_path, output_path):
    # Commande gdalwarp pour reprojeter de EPSG:4326 vers EPSG:3857
    command = [
        "gdalwarp",
        "-s_srs", "EPSG:4326",  # Projection d'entrée (WGS 84)
        "-t_srs", "EPSG:3857",  # Projection cible (Web Mercator)
        input_path,  # Fichier d'entrée
        output_path  # Fichier de sortie
    ]
    
    # Exécuter la commande
    subprocess.run(command, check=True)
    print(f"Reprojection de {input_path} vers {output_path} réussie.")

# Fonction pour parcourir les dossiers et reprojeter toutes les tuiles
def reprojeter_tuiles_in_dossier(dossier_input, dossier_output):
    # Parcourir tous les niveaux de zoom dans le dossier
    for z in os.listdir(dossier_input):
        # Créer le dossier de sortie pour le niveau de zoom si nécessaire
        niveau_zoom_output = os.path.join(dossier_output, z)
        os.makedirs(niveau_zoom_output, exist_ok=True)
        
        niveau_zoom_input = os.path.join(dossier_input, z)
        
        # Vérifier si le dossier existe et est un répertoire
        if os.path.isdir(niveau_zoom_input):
            # Parcourir les sous-dossiers x
            for x in os.listdir(niveau_zoom_input):
                niveau_x_input = os.path.join(niveau_zoom_input, x)
                
                # Vérifier si c'est un répertoire
                if os.path.isdir(niveau_x_input):
                    niveau_x_output = os.path.join(niveau_zoom_output, x)
                    os.makedirs(niveau_x_output, exist_ok=True)
                    
                    # Parcourir toutes les tuiles y.png dans ce dossier
                    for y in os.listdir(niveau_x_input):
                        input_file = os.path.join(niveau_x_input, y)
                        output_file = os.path.join(niveau_x_output, y)
                        
                        # Vérifier si le fichier est bien une image PNG
                        if y.endswith(".png"):
                            reprojeter_tuile(input_file, output_file)

# Définir les chemins d'entrée et de sortie
dossier_input = "./tiles_output"  # Dossier contenant vos tuiles (en EPSG:4326)

dossier_output = "./tiles_reprojetees"  # Dossier de destination des tuiles reprojetées

# Reprojeter toutes les tuiles dans le dossier
reprojeter_tuiles_in_dossier(dossier_input, dossier_output)

