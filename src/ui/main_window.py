# src/ui/main_window.py (Updated)
# ... (imports remain the same, add the new one)
import os

from PySide6.QtWidgets import QMainWindow

from src.core.transcriber import WorkerThread # Import the worker

class MainWindow(QMainWindow):
    def __init__(self):
        # ... (the __init__ method is the same up to the button connections)

        # Connect transcribe button
        self.transcribe_button.clicked.connect(self.start_transcription)
        # ... (rest of __init__ is the same)

    # ... (browse_file, save_text, clear_all methods are the same)

    def start_transcription(self):
        """Initiates the transcription process in a background thread."""
        audio_path = self.file_path_label.text()

        # --- Input Validation ---
        if not os.path.exists(audio_path):
            self.status_label.setText("Error: Please select a valid audio file first.")
            return

        # Disable button to prevent multiple clicks
        self.transcribe_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0) # Indeterminate progress

        # Create and start the worker thread
        self.worker = WorkerThread(audio_path)
        self.worker.transcription_finished.connect(self.on_transcription_complete)
        self.worker.error_occurred.connect(self.on_transcription_error)
        self.worker.progress_updated.connect(self.update_status)
        self.worker.start()

    def update_status(self, message: str):
        """Updates the status label."""
        self.status_label.setText(message)

    def on_transcription_complete(self, text: str):
        """Handles the successful completion of transcription."""
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 1) # Reset progress bar
        self.text_display.setText(text)
        self.status_label.setText("Transcription complete! ✨")
        self.transcribe_button.setEnabled(True)

    def on_transcription_error(self, error_message: str):
        """Handles errors reported by the worker thread."""
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Error: {error_message}")
        # Optionally, log the error to a file
        # import logging
        # logging.basicConfig(filename='app_errors.log', level=logging.ERROR)
        # logging.error(error_message)
        self.transcribe_button.setEnabled(True)