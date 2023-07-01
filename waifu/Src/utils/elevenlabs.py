import os, json, io
import utils.audio
import utils.vtube_studio
from elevenlabslib import *

ELEVENLABS_CLIENT = ElevenLabsUser(os.environ.get("ELEVENLABS_KEY"))

ELEVENLABS_VOICE = None

env_voice = os.environ.get("ELEVENLABS_VOICE")

voices = ELEVENLABS_CLIENT.get_voices_by_name(env_voice)
if len(voices) > 0:
    ELEVENLABS_VOICE = voices[0]
else:
    print("No voices found.")



def speak(message):
    try:
        global ELEVENLABS_CLIENT, ELEVENLABS_VOICE

        stability, similarity = 0.75, 0.75
        env_stability, env_similarity = os.environ.get("ELEVENLABS_STABILITY"), os.environ.get("ELEVENLABS_SIMILARITY")

        if env_stability and env_stability.strip():
            stability = float(env_stability)

        if env_similarity and env_similarity.strip():
            stability = float(env_similarity)

        mp3_bytes = ELEVENLABS_VOICE.generate_audio_bytes(message, stability, similarity)

        with io.BytesIO(mp3_bytes) as memfile:
            utils.audio.play_mp3(memfile, utils.vtube_studio.set_audio_level)

    except Exception as e:
        print(e)
    