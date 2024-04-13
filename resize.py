import os
from PIL import Image

def redimensionner_et_combler_images(chemin_dossier_entree, chemin_dossier_sortie, nouvelle_largeur, nouvelle_hauteur):
    # Créer le répertoire de sortie s'il n'existe pas déjà
    if not os.path.exists(chemin_dossier_sortie):
        os.makedirs(chemin_dossier_sortie)
    
    # Liste tous les fichiers dans le dossier d'entrée
    fichiers = os.listdir(chemin_dossier_entree)
    
    # Parcourir chaque fichier
    for fichier in fichiers:
        chemin_fichier_entree = os.path.join(chemin_dossier_entree, fichier)
        
        # Vérifier si le fichier est une image
        if os.path.isfile(chemin_fichier_entree) and fichier.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            # Ouvrir l'image
            image_origine = Image.open(chemin_fichier_entree)
            
            # Obtenir les dimensions de l'image originale
            largeur_origine, hauteur_origine = image_origine.size
            
            # Calculer les dimensions pour redimensionner l'image tout en conservant ses proportions
            rapport_origine = largeur_origine / hauteur_origine
            nouvelle_hauteur_calculée = nouvelle_largeur / rapport_origine
            
            # Redimensionner l'image tout en conservant les proportions
            image_redimensionnee = image_origine.resize((nouvelle_largeur, int(nouvelle_hauteur_calculée)), Image.ANTIALIAS)
            
            # Créer une nouvelle image avec les dimensions finales et remplir le reste avec du noir
            nouvelle_image = Image.new("RGB", (nouvelle_largeur, nouvelle_hauteur), "black")
            x_position = (nouvelle_largeur - image_redimensionnee.width) // 2
            y_position = (nouvelle_hauteur - image_redimensionnee.height) // 2
            nouvelle_image.paste(image_redimensionnee, (x_position, y_position))
            
            # Enregistrer l'image avec le même nom dans le répertoire de sortie
            chemin_fichier_sortie = os.path.join(chemin_dossier_sortie, fichier)
            nouvelle_image.save(chemin_fichier_sortie)

# Exemple d'utilisation
chemin_dossier_entree = r"F:\downloads\bot_Clash_Royale-main\bot_Clash_Royale-main\Cards"  # Chemin du dossier contenant les images à redimensionner
chemin_dossier_sortie = r"C:\Users\wassi\Documents\3A\Ouverture\Bot-Clash-Royal-main\use_fonction\test"  # Chemin du dossier où enregistrer les images redimensionnées
redimensionner_et_combler_images(chemin_dossier_entree, chemin_dossier_sortie, 63, 80)  # Redimensionne et comble les images du dossier d'entrée pour correspondre à 800x600 pixels et les enregistre dans le dossier de sortie
