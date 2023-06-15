import logging
import queue
import json
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from websocket import WebSocket

logger = logging.getLogger(__name__)

# Variables de configuration pour l'API Deepgram
DEEPGRAM_API_ENDPOINT = "wss://api.deepgram.com/v1/listen"
DEEPGRAM_API_KEY = "Token 71bfbc4f056b672867a26d3099023f749a62de68"

# Fonction pour envoyer les données audio à l'API Deepgram
def send_audio_to_deepgram(audio_data):
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "application/octet-stream"
    }
    ws.send_binary(audio_data)

# Fonction pour extraire la transcription de la réponse de l'API Deepgram
def extract_transcription(api_response):
    response_data = json.loads(api_response)
    return response_data["results"]["transcripts"][0]["text"]

# Fonction pour envoyer une commande de fermeture à l'API Deepgram
def close_stream():
    ws.send(json.dumps({"type": "CloseStream"}))

# Configuration de la page Streamlit
st.title("Transcription audio en temps réel avec Deepgram")
transcription_placeholder = st.empty()

# Connexion à l'API Deepgram en mode sendonly
webrtc_ctx = webrtc_streamer(
    key="sendonly-audio",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=256,
    media_stream_constraints={"audio": True},
)

# Vérification de la connexion au flux audio
if webrtc_ctx.audio_receiver:
    # Connexion à l'API Deepgram
    ws = WebSocket()
    ws.connect(DEEPGRAM_API_ENDPOINT)

    while True:
        try:
            audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
        except queue.Empty:
            logger.warning("Queue is empty. Abort.")
            break

        for audio_frame in audio_frames:
            # Envoi des données audio à l'API Deepgram
            send_audio_to_deepgram(audio_frame.to_ndarray().tobytes())

        # Réception des réponses de transcription de l'API Deepgram
        result = ws.recv()
        # Traitement de la réponse de l'API Deepgram (extraction de la transcription, etc.)
        # Vous devrez adapter cette partie en fonction de la structure de réponse de l'API Deepgram
        
        # Affichage de la transcription sur la page Streamlit
        if result:
            transcription = extract_transcription(result)  # Fonction à adapter pour extraire la transcription de la réponse
            transcription_placeholder.text(transcription)

    # Envoi d'une commande de fermeture à l'API Deepgram
    close_stream()
    ws.close()
else:
    logger.warning("AudioReciver is not set. Abort.")
