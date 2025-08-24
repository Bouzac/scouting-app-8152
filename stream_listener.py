import json
import subprocess
import pytesseract
import yt_dlp
import cv2
import numpy as np
import constants as const
import os
import re

import database_manager as db_m
import time

STREAM_COORDS = const.STREAM_COORDS

def get_stream_url(url):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict['url']

def stream_video(url, target_pixel_pos=(367, 337), target_color=(255, 255, 255)):
    if const.STREAM_ON is False:
        return
    stream_url = get_stream_url(url)
    print(f"Streaming from: {stream_url}")

    width, height = get_video_info(stream_url)
    print(f"Video resolution: {width}x{height}")

    frame_size = width * height * 3

    cmd = [
        'ffmpeg',
        '-loglevel', 'quiet',
        '-i', stream_url,
        '-an',
        '-f', 'image2pipe',
        '-pix_fmt', 'bgr24',
        '-vcodec', 'rawvideo',
        '-'
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10**8)

    cooldown_until = 0

    try:
        while True:
            raw_frame = process.stdout.read(frame_size)
            if len(raw_frame) != frame_size:
                print('error: incomplete frame data')
                break

            frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((height, width, 3))

            # Ignore detection if on cooldown
            if time.time() < cooldown_until:
                continue

            pixel_color = frame[target_pixel_pos[1], target_pixel_pos[0]]
            if np.all(pixel_color == target_color):
                print(f"Pixel at {target_pixel_pos} matched target color {target_color}!")
                cv2.imwrite('temp/captured_frame.png', frame)
                match_data = process_match_data_frame('temp/captured_frame.png', debug=True)
                db_m.update_match(match_data)
                os.remove('temp/captured_frame.png')
                cooldown_until = time.time() + 10

    finally:
        print('finit')
        process.terminate()
        process.wait()


def get_video_info(url):
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,r_frame_rate',
        '-of', 'json',
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("ffprobe failed")

    data = json.loads(result.stdout)
    stream = data['streams'][0]

    width = stream['width']
    height = stream['height']

    return width, height

def extract_zone(img, zone_name):
    tl = STREAM_COORDS[zone_name]['top_left']
    br = STREAM_COORDS[zone_name]['bottom_right']
    return img[tl[1]:br[1], tl[0]:br[0]]

def preprocess_image(img, mode="auto"):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    if mode == "points":
        _, thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY_INV)
    elif mode == "teams":
        # Pour les numéros d'équipe, pas d'inversion, seuil plus bas
        _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
        # Agrandit l'image pour améliorer l'OCR
        thresh = cv2.resize(thresh, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)
    else:
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
            cv2.THRESH_BINARY_INV, 11, 4
        )
    return thresh

def ocr_image(img, whitelist=None):
    # Teste psm 6 (bloc de texte) pour les équipes
    config = r'--oem 3 --psm 6'
    if whitelist:
        config += f' -c tessedit_char_whitelist={whitelist}'
    text = pytesseract.image_to_string(img, config=config, lang='fra')
    # Nettoyage supplémentaire
    text = re.sub(r'[^\d\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_ocr(text, expect_team_numbers=False):
    text = text.replace('\n', ' ')
    print(f"OCR raw text: '{text}'")
    if expect_team_numbers:
        # Garde tous les groupes de 3 ou 4 chiffres (numéros FRC)
        teams = re.findall(r'\b\d{3,4}\b', text)
        print(f"OCR cleaned teams: '{teams}'")
        return teams
    else:
        # Pour les points, garde seulement le premier nombre
        points = re.findall(r'\d+', text)
        print(f"OCR cleaned points: '{points}'")
        return points[0] if points else ""

def process_match_data_frame(frame_path='temp/captured_frame.png', debug=True):
    img = cv2.imread(frame_path)
    results = {}

    if debug and not os.path.exists("debug_zones"):
        os.makedirs("debug_zones")

    for zone in STREAM_COORDS:
        # Choix du mode selon la zone
        if "teams" in zone:
            mode = "teams"
        elif "points" in zone:
            mode = "points"
        else:
            mode = "auto"
        zone_img = extract_zone(img, zone)
        preprocessed = preprocess_image(zone_img, mode=mode)

        if debug:
            debug_path = f"debug_zones/{zone}.png"
            cv2.imwrite(debug_path, preprocessed)

        if "teams" in zone:
            raw_text = ocr_image(preprocessed, whitelist="0123456789")
            results[zone] = clean_ocr(raw_text, expect_team_numbers=True)
        elif "points" in zone:
            raw_text = ocr_image(preprocessed, whitelist="0123456789")
            results[zone] = clean_ocr(raw_text)
        else:
            raw_text = ocr_image(preprocessed)
            results[zone] = raw_text.strip()

    return {
        "match_number": results.get("match_number", "").split(" ")[0],
        "blue_points": results.get("blue_points", ""),
        "red_points": results.get("red_points", ""),
        "blue_teams": results.get("blue_teams", []),
        "red_teams": results.get("red_teams", [])
    }