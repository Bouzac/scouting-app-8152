from flask import Flask
from threading import Thread
import time
import webserver
import constants as const

from stream_listener import stream_video

STREAM_URL = const.STREAM_URL

# Thread qui exécute le stream
def start_stream():
    stream_video(
        url=STREAM_URL,
        target_pixel_pos=(757, 700),  
        target_color=(255, 255, 255)
    )

if __name__ == "__main__":
    # Démarre le thread avant Flask
    stream_thread = Thread(target=start_stream, daemon=True)
    stream_thread.start()

    # Lance Flask (backend)
    webserver.app.run(debug=True, port=5000) #à exécuter en dernier
