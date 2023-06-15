import logging
import queue
import pydub
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer

logger = logging.getLogger(__name__)

# Variables de configuration pour l'API Deepgram
DEEPGRAM_API_ENDPOINT = "wss://api.deepgram.com/v1/listen"
DEEPGRAM_API_KEY = "Token 71bfbc4f056b672867a26d3099023f749a62de68"

# Fonction pour envoyer les données audio à l'API Deepgram
def send_audio_to_deepgram(audio_data):
    ws.send_binary(audio_data)

# Fonction pour extraire la transcription de la réponse de l'API Deepgram
def extract_transcription(api_response):
    response_data = json.loads(api_response)
    return response_data["results"]["transcripts"][0]["text"]

# Fonction pour envoyer une commande de fermeture à l'API Deepgram
def close_stream():
    ws.send(json.dumps({"type": "CloseStream"}))

# Obtenir la liste des périphériques audio disponibles
def get_audio_devices():
    # TODO: Implémenter la récupération de la liste des périphériques audio
    # Retourner une liste de chaînes représentant les noms des périphériques audio
    return ["Device 1", "Device 2"]

# Configuration de la page Streamlit
st.title("Transcription audio en temps réel avec Deepgram")
transcription_placeholder = st.empty()

# Sélection du périphérique audio
selected_audio_device = st.selectbox("Sélectionnez le périphérique audio", get_audio_devices())

# Connexion à l'API Deepgram en mode sendonly
webrtc_ctx = webrtc_streamer(
    key="sendonly-audio",
    mode=WebRtcMode.SENDONLY,
    audio_input_device=selected_audio_device,
    audio_receiver_size=256,
)

# Vérification de la connexion au flux audio
if webrtc_ctx.audio_receiver:
    # Connexion à l'API Deepgram
    ws = WebSocket()
    ws.connect(DEEPGRAM_API_ENDPOINT)

    sound_window_len = 5000  # 5s
    sound_window_buffer = None

    while True:
        try:
            audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
        except queue.Empty:
            logger.warning("Queue is empty. Abort.")
            break

        sound_chunk = pydub.AudioSegment.empty()
        for audio_frame in audio_frames:
            sound = pydub.AudioSegment(
                data=audio_frame.to_ndarray().tobytes(),
                sample_width=audio_frame.format.bytes,
                frame_rate=audio_frame.sample_rate,
                channels=len(audio_frame.layout.channels),
            )
            sound_chunk += sound

        if len(sound_chunk) > 0:
            if sound_window_buffer is None:
                sound_window_buffer = pydub.AudioSegment.silent(
                    duration=sound_window_len
                )

            sound_window_buffer += sound_chunk
            if len(sound_window_buffer) > sound_window_len:
                sound_window_buffer = sound_window_buffer[-sound_window_len:]

        if sound_window_buffer:
            send_audio_to_deepgram(sound_window_buffer.raw_data)

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
