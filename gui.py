import sys
from PyQt6.QtCore import Qt, QThread
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QProgressBar
from main import Main

class LoadingThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        main = Main()
        self.quit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Recognition")
        self.setGeometry(100, 100, 640, 480)

        # Create and show loading widget
        self.loading_widget = QWidget()
        self.loading_widget_layout = QVBoxLayout(self.loading_widget)
        self.loading_label = QLabel("Loading...", alignment=Qt.AlignmentFlag.AlignCenter)
        self.loading_widget_layout.addWidget(self.loading_label)
        self.progress_bar = QProgressBar()
        self.loading_widget_layout.addWidget(self.progress_bar)
        self.setCentralWidget(self.loading_widget)

        # Initialize and start loading thread
        self.loading_thread = LoadingThread()
        self.loading_thread.finished.connect(self.on_loading_finished)
        self.loading_thread.start()

    def on_loading_finished(self):
        # Remove loading widget and show main window
        self.setCentralWidget(QLabel("Face Recognition", alignment=Qt.AlignmentFlag.AlignCenter))
        self.show()

        # Run face recognition
        self.main = Main()
        self.main.run()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
