# ==========================================
# FILE: app.py
# FINAL STABLE VERSION
# Hidden Start + Hey Neuro Wake Word
# Same UI + No Blank Screen + No Attribute Error
# ==========================================

import sys
import threading
import time

from Modules.wake_word import listen_for_wake_word

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout
)

from PyQt6.QtCore import Qt, QTimer

from Modules.voice_assistant import (
    listen,
    process_command,
    speak
)


# ==========================================
# MAIN WINDOW
# ==========================================
class NeuroDeskUI(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("NeuroDesk AI")
        self.setGeometry(200, 100, 950, 650)

        self.mic_running = False

        self.setup_ui()

    # ======================================
    # UI
    # ======================================
    def setup_ui(self):

        root = QWidget()
        self.setCentralWidget(root)

        layout = QHBoxLayout(root)

        # Left Panel
        left = QVBoxLayout()

        self.status = QLabel("Sleeping...")
        self.status.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.status.setStyleSheet("""
            font-size:22px;
            color:#00e5ff;
        """)

        self.enable_btn = QPushButton("🎤 Enable Mic")
        self.stop_btn = QPushButton("🛑 Stop Mic")

        self.enable_btn.clicked.connect(
            self.start_mic
        )

        self.stop_btn.clicked.connect(
            self.stop_mic
        )

        self.enable_btn.setMinimumHeight(50)
        self.stop_btn.setMinimumHeight(50)

        left.addWidget(self.status)
        left.addSpacing(20)
        left.addWidget(self.enable_btn)
        left.addWidget(self.stop_btn)
        left.addStretch()

        # Right Panel Logs
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)

        self.logs.setStyleSheet("""
            font-size:15px;
            background:#111;
            color:white;
        """)

        layout.addLayout(left, 1)
        layout.addWidget(self.logs, 2)

    # ======================================
    # SAFE LOG
    # ======================================
    def add_log(self, text):
        try:
            self.logs.append(text)
        except:
            pass

    # ======================================
    # SAFE STATUS
    # ======================================
    def set_status(self, text):
        try:
            self.status.setText(text)
        except:
            pass

    # ======================================
    # START MIC
    # ======================================
    def start_mic(self):

        if self.mic_running:
            return

        self.mic_running = True

        self.add_log("Mic Enabled")

        threading.Thread(
            target=self.mic_loop,
            daemon=True
        ).start()

    # ======================================
    # STOP MIC
    # ======================================
    def stop_mic(self):

        self.mic_running = False
        self.set_status("Stopped")
        self.add_log("Mic Disabled")

    # ======================================
    # MIC LOOP
    # ======================================
    def mic_loop(self):

        while self.mic_running:

            try:
                self.set_status("Listening...")

                command = listen()

                if command == "":
                    continue

                self.add_log("You: " + command)

                self.set_status("Processing...")

                result = process_command(command)

                if result is False:
                    self.mic_running = False
                    break

                time.sleep(0.2)

            except Exception as e:

                self.add_log(
                    "Error: " + str(e)
                )

                time.sleep(0.5)

        self.set_status("Idle")

    # ======================================
    # WAKE WORD MODE
    # ======================================
    def wake_mode(self):

        self.add_log("Waiting for wake word...")

        while True:

            heard = listen_for_wake_word()

            if heard:

                # UI safely main thread me open hoga
                QTimer.singleShot(0, self.showNormal)
                QTimer.singleShot(0, self.raise_)
                QTimer.singleShot(0, self.activateWindow)

                QTimer.singleShot(
                    0,
                    lambda: self.set_status("Awakened")
                )

                speak("Yes sir")

                QTimer.singleShot(
                    0,
                    self.start_mic
                )

                break

    # ======================================
    # CLOSE EVENT
    # ======================================
    def closeEvent(self, event):

        self.mic_running = False
        event.accept()


# ==========================================
# RUN APP
# ==========================================
if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = NeuroDeskUI()

    # First load UI properly, then hide
    win.show()
    win.hide()

    # Wake word background listener
    threading.Thread(
        target=win.wake_mode,
        daemon=True
    ).start()

    sys.exit(app.exec())