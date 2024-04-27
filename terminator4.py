from moviepy.editor import VideoFileClip
import cv2
import numpy as np

def apply_red_filter_add_text_and_table(frame, frame_count, fps):
    # Convertir l'image en nuances de gris
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Créer une image rouge à partir des nuances de gris
    red_frame = cv2.merge([gray_frame, np.zeros_like(gray_frame), np.zeros_like(gray_frame)])

    # Définir la taille et la position du tableau
    height, width = frame.shape[:2]
    cell_width = width // 8
    cell_height = height // 8
    top_left_x = width // 4 - cell_width
    top_left_y = height // 4 - cell_height

    # Condition pour faire clignoter le tableau toutes les demi-secondes
    if frame_count[0] % (fps // 2) < (fps // 4):
        # Dessiner les cellules du tableau
        for i in range(2):
            for j in range(2):
                start_x = top_left_x + i * cell_width
                start_y = top_left_y + j * cell_height
                end_x = start_x + cell_width
                end_y = start_y + cell_height
                cv2.rectangle(red_frame, (start_x, start_y), (end_x, end_y), (255, 255, 255), 2)  # Blanc

    # Afficher le texte conditionnellement (clignotant)
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    if frame_count[0] % (fps // 2) < (fps // 4):
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        text_x = width - text_size[0] - 10
        text_y = height - 10
        cv2.putText(red_frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # Incrémenter le compteur de frame
    frame_count[0] += 1

    return red_frame

# Charger la vidéo
clip = VideoFileClip("test3.mp4")
frame_count = [0]  # Initialiser le compteur de frames comme une liste pour mutabilité
fps = clip.fps  # Récupérer le nombre d'images par seconde de la vidéo

# Appliquer le filtre rouge, ajouter du texte clignotant et un tableau sur chaque frame
video_with_table = clip.fl_image(lambda frame: apply_red_filter_add_text_and_table(frame, frame_count, fps))

# Sauvegarder et visualiser le résultat
video_with_table.write_videofile("red_video_with_table3.mp4", codec='libx264')
