import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Audio Transcriber")
    window.setGeometry(100, 100, 300, 100) # x, y, width, height

    layout = QVBoxLayout()
    label = QLabel("Hello, PySide6!")
    layout.addWidget(label)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()