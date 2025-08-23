import cv2
import time
import constants

video_path = constants.STREAM_PATH
pixel_coord = (100,200)
target_color = (255, 255, 255)
tolerance = 10
pause = 1/30

def color_close(c1, c2, tol):
    return all(abs(a - b) <= tol for a, b in zip(c1,c2))

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print('Vidéo pas ouverte')
    exit()

found = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print('Fin de la vidéo ou erreur')
        break

    x, y = pixel_coord
    if y >= frame.shape[0] or x >= frame.shape[1]:
        print("Erreur : coordonnées hors de la vidéo.")
        break

    pixel_color = frame[y, x]

    if color_close(pixel_color, target_color, tolerance):
        print(f"Pixel trouvé à la couleur {target_color} !")
        found = True
        break

    time.sleep(pause)

cap.release()

if not found:
    print("La couleur n'a pas été détectée.")