# src/core/transcriber.py

import json
import os
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
from PySide6.QtCore import QThread, Signal

MODEL_PATH = "models/vosk-model-small-en-us-0.15"


class WorkerThread(QThread):
    """
    Worker thread for performing audio transcription to prevent UI freezing.
    """
    # Define signals
    # Signal to emit the final transcribed text
    transcription_finished = Signal(str)
    # Signal to emit error messages
    error_occurred = Signal(str)
    # Signal to emit progress updates (e.g., status messages)
    progress_updated = Signal(str)

    def __init__(self, audio_file_path: str):
        super().__init__()
        self.audio_file_path = audio_file_path

    def run(self):
        """The main work of the thread."""
        try:
            # --- 1. Model Loading ---
            self.progress_updated.emit("Loading transcription model...")
            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError("Vosk model not found.")
            model = Model(MODEL_PATH)

            # --- 2. Audio Conversion ---
            self.progress_updated.emit("Preparing audio file...")
            sound = AudioSegment.from_file(self.audio_file_path)
            sound = sound.set_channels(1)
            sound = sound.set_frame_rate(16000)
            buffer = sound.raw_data

            # --- 3. Transcription ---
            self.progress_updated.emit("Transcribing... Please wait.")
            recognizer = KaldiRecognizer(model, 16000)
            if not recognizer.AcceptWaveform(buffer):
                pass

            result = recognizer.FinalResult()
            transcribed_text = json.loads(result)["text"]

            self.transcription_finished.emit(transcribed_text)

        except FileNotFoundError as e:
            self.error_occurred.emit(f"Error: {e}. Please ensure the model is in the 'models' directory.")
        except Exception as e:
            # General error handling
            self.error_occurred.emit(f"An unexpected error occurred: {e}")