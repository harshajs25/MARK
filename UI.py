import sys
import numpy as np
import pyqtgraph as pg
import pyaudio
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QTimer

class VoiceRecorderUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle("Voice Recorder")
        self.setGeometry(0, 0, 1920, 1080)
        self.showFullScreen()

        # Central layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Button layout
        button_layout = QHBoxLayout()

        # Mic button
        mic_button = QPushButton()
        mic_icon = QIcon(QPixmap("mic_icon.png"))
        mic_button.setIcon(mic_icon)
        mic_button.setIconSize(mic_button.sizeHint())
        mic_button.clicked.connect(self.start_recording)
        button_layout.addWidget(mic_button)

        # Pause/Stop button
        self.pause_button = QPushButton("Pause/Stop")
        self.pause_button.clicked.connect(self.stop_recording)
        button_layout.addWidget(self.pause_button)

        main_layout.addLayout(button_layout)

        # Waveform plot
        self.waveform_plot = pg.PlotWidget()
        self.waveform_plot.setYRange(-1, 1)
        main_layout.addWidget(self.waveform_plot)
        self.waveform_curve = self.waveform_plot.plot()

        # Audio setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_waveform)
        self.is_recording = False
        self.stream = None
        self.CHUNK = 1024

    def start_recording(self):
        self.is_recording = True
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paFloat32,
                                      channels=1,
                                      rate=44100,
                                      input=True,
                                      frames_per_buffer=self.CHUNK)
        self.timer.start(20)

    def stop_recording(self):
        self.is_recording = False
        self.timer.stop()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio is not None:
            self.audio.terminate()

    def update_waveform(self):
        if self.is_recording:
            data = np.frombuffer(self.stream.read(self.CHUNK), dtype=np.float32)
            self.waveform_curve.setData(data)

    def closeEvent(self, event):
        self.stop_recording()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceRecorderUI()
    window.show()
    sys.exit(app.exec_())
