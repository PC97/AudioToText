# src/core/transcriber.py

import json
import wave
import os
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

# Path to the Vosk model folder
MODEL_PATH = "models/vosk-model-small-en-us-0.15"

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribes an audio file using the local Vosk model.
    Handles MP3 and other formats by converting to WAV.

    Args:
        audio_file_path: The path to the audio file.

    Returns:
        The transcribed text.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Vosk model not found. Please download and place it in the 'models' directory.")

    # --- Convert audio to the required format (WAV, 16kHz, mono) ---
    # pydub handles various formats and uses ffmpeg under the hood.
    sound = AudioSegment.from_file(audio_file_path)
    sound = sound.set_channels(1)
    sound = sound.set_frame_rate(16000)

    # Vosk needs the raw audio data as bytes.
    # We use a temporary in-memory buffer to avoid writing a file to disk.
    buffer = sound.raw_data

    # --- Perform Transcription ---
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)

    if not recognizer.AcceptWaveform(buffer):
        # This handles shorter audio files that might be processed in one go.
        pass

    result = recognizer.FinalResult()
    # The result is a JSON string, we need to parse it to get the text.
    return json.loads(result)["text"]