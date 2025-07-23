# src/ui/main_window.py

import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QLineEdit, QTextEdit, QProgressBar, QLabel
)
from PySide6.QtCore import Qt
from src.core.transcriber import WorkerThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Offline Audio Transcriber")
        self.setGeometry(100, 100, 800, 600)

        # --- 1. DEFINE WIDGETS ---
        # All widgets are created here first.
        self.file_path_label = QLineEdit("No file selected...")
        self.file_path_label.setReadOnly(True)
        self.browse_button = QPushButton("Browse Audio File")

        self.status_label = QLabel("Ready. Select an audio file to begin.")
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        self.text_display = QTextEdit()
        self.text_display.setPlaceholderText("Transcribed text will appear here...")
        self.text_display.setReadOnly(True)

        self.transcribe_button = QPushButton("Transcribe")
        self.save_button = QPushButton("Save Text")
        self.clear_button = QPushButton("Clear All")

        # --- 2. CONNECT SIGNALS TO SLOTS ---
        # Now that widgets exist, we can connect their signals.
        self.browse_button.clicked.connect(self.browse_file)
        self.transcribe_button.clicked.connect(self.start_transcription)
        self.save_button.clicked.connect(self.save_text)
        self.clear_button.clicked.connect(self.clear_all)

        # --- 3. SET UP LAYOUT ---
        # A structured layout for a clean UI.
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(self.browse_button)

        action_layout = QHBoxLayout()
        action_layout.addWidget(self.transcribe_button)
        action_layout.addWidget(self.save_button)
        action_layout.addWidget(self.clear_button)

        main_layout.addLayout(file_layout)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.text_display, 1)  # Make text area expand
        main_layout.addLayout(action_layout)

    def browse_file(self):
        """Opens a file dialog to select an audio file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select an Audio File", "", "Audio Files (*.mp3 *.wav *.m4a)"
        )
        if file_path:
            self.file_path_label.setText(file_path)
            self.status_label.setText(f"Loaded: {os.path.basename(file_path)}")

    def start_transcription(self):
        """Initiates the transcription process in a background thread."""
        audio_path = self.file_path_label.text()

        if not os.path.exists(audio_path):
            self.status_label.setText("Error: Please select a valid audio file first.")
            return

        self.transcribe_button.setEnabled(False)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.setVisible(True)

        self.worker = WorkerThread(audio_path)
        self.worker.transcription_finished.connect(self.on_transcription_complete)
        self.worker.error_occurred.connect(self.on_transcription_error)
        self.worker.progress_updated.connect(self.update_status)
        self.worker.start()

    def update_status(self, message: str):
        self.status_label.setText(message)

    def on_transcription_complete(self, text: str):
        """Handles successful completion of transcription."""
        self.progress_bar.setVisible(False)
        self.text_display.setText(text)
        self.status_label.setText("Transcription complete! ✨")
        self.transcribe_button.setEnabled(True)

    def on_transcription_error(self, error_message: str):
        """Handles errors reported by the worker thread."""
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Error: {error_message}")
        self.transcribe_button.setEnabled(True)

    def save_text(self):
        """Saves the content of the text display to a .txt file."""
        if not self.text_display.toPlainText():
            self.status_label.setText("Nothing to save.")
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Transcription", "", "Text Files (*.txt)"
        )
        if save_path:
            try:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(self.text_display.toPlainText())
                self.status_label.setText(f"Saved to {save_path}")
            except Exception as e:
                self.status_label.setText(f"Error saving file: {e}")

    def clear_all(self):
        """Resets the application state."""
        self.file_path_label.setText("No file selected...")
        self.text_display.clear()
        self.status_label.setText("Ready")
        self.progress_bar.setVisible(False)
        self.transcribe_button.setEnabled(True)