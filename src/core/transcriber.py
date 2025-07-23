# src/core/transcriber.py

import json
import os
from PySide6.QtCore import QThread, Signal
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

# Define the path to your downloaded Vosk model
MODEL_PATH = "models/vosk-model-small-en-us-0.15"


class WorkerThread(QThread):
    """
    Worker thread for performing audio transcription to prevent UI freezing.
    """
    # Signals to communicate with the main UI thread
    transcription_finished = Signal(str)
    error_occurred = Signal(str)
    progress_updated = Signal(str)

    def __init__(self, audio_file_path: str):
        super().__init__()
        self.audio_file_path = audio_file_path

    def run(self):
        """The main work of the thread is done here."""
        try:
            # --- 0. Pre-flight Checks ---
            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError("Vosk model not found. Ensure it's in the 'models' directory.")
            if not os.path.exists(self.audio_file_path):
                raise FileNotFoundError(f"Audio file not found: {self.audio_file_path}")

            # --- 1. Model Loading ---
            self.progress_updated.emit("Loading transcription model...")
            model = Model(MODEL_PATH)

            # --- 2. Audio Preparation ---
            self.progress_updated.emit("Preparing audio file...")
            sound = AudioSegment.from_file(self.audio_file_path)
            sound = sound.set_channels(1)
            sound = sound.set_frame_rate(16000)
            buffer = sound.raw_data

            # --- 3. Transcription ---
            self.progress_updated.emit("Transcribing... Please wait.")
            recognizer = KaldiRecognizer(model, 16000)
            recognizer.AcceptWaveform(buffer)

            result = recognizer.FinalResult()
            transcribed_text = json.loads(result)["text"]

            self.transcription_finished.emit(transcribed_text)

        except Exception as e:
            # Catch any exception and report it back to the UI
            self.error_occurred.emit(str(e))