from PIL import Image, ImageDraw

def decouper_et_afficher_contours(chemin_image, rois):
    # Ouvrir l'image
    image = Image.open(chemin_image)
    
    # Créer un objet ImageDraw pour dessiner sur l'image
    draw = ImageDraw.Draw(image)
    
    # Parcourir chaque ROI
    for roi in rois:
        x, y, largeur, hauteur = roi
        # Dessiner le contour du rectangle autour de la zone
        draw.rectangle([x, y, x + largeur, y + hauteur], outline='red', width=2)
    
    # Afficher l'image avec les contours des zones découpées
    image.show()

# Coordonnées des ROIs
ROIs = [
    [359, 673, 64, 81],
    [275, 674, 63, 80],
    [106, 675, 62, 78],
    [190, 674, 63, 80]
]

# # Exemple d'utilisation
# chemin_image = "chemin_vers_votre_image.jpg"  # Chemin de votre image
# decouper_et_afficher_contours(chemin_image, ROIs)


# # Exemple d'utilisation avec une autre image
# chemin_image_2 = r"C:\Users\wassi\Pictures\Capture d’écran 2024-03-19 104815.png"  # Chemin de votre deuxième image
# afficher_blocs_sur_image(chemin_image_2, chemin_json)

# Exemple d'utilisation
chemin_image_2 = r"C:\Users\wassi\Pictures\test.png"  # Chemin de votre deuxième image
decouper_et_afficher_contours(chemin_image_2, ROIs)
