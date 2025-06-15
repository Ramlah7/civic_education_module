import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QListWidget, QTextBrowser, QLineEdit, QPushButton, QFrame, QLabel
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont

class CivicEducationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Civic Education System")
        self.resize(1000, 600)

        self.topics = self.load_topics()
        self.init_ui()

    def load_topics(self):
        with open("topics.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def init_ui(self):
        container = QWidget()
        self.setCentralWidget(container)

        outer_layout = QVBoxLayout(container)

        # Title Header
        self.title = QLabel("📘 Civic Education System")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                padding: 14px;
                color: #1F4E79;
                background-color: #E3F2FD;
                border-bottom: 2px solid #90CAF9;
            }
        """)
        outer_layout.addWidget(self.title)

        layout = QHBoxLayout()
        outer_layout.addLayout(layout)

        # Sidebar
        sidebar = QVBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search topics...")
        self.search_bar.textChanged.connect(self.filter_topics)
        sidebar.addWidget(self.search_bar)

        self.topic_list = QListWidget()
        self.topic_list.addItems(self.topics.keys())
        self.topic_list.currentTextChanged.connect(self.display_topic)
        sidebar.addWidget(self.topic_list)

        layout.addLayout(sidebar, 2)

        # Main content area
        self.content_card = QTextBrowser()
        self.content_card.setOpenExternalLinks(True)
        self.content_card.setFrameShape(QFrame.StyledPanel)
        self.content_card.setStyleSheet("""
            QTextBrowser {
                background-color: #ffffff;
                border-radius: 15px;
                padding: 15px;
                font-size: 14px;
                font-family: Segoe UI, sans-serif;
            }
        """)

        layout.addWidget(self.content_card, 5)

        # Default selection
        self.topic_list.setCurrentRow(0)

    def filter_topics(self, text):
        self.topic_list.clear()
        filtered = [title for title in self.topics.keys() if text.lower() in title.lower()]
        self.topic_list.addItems(filtered)

    def display_topic(self, topic):
        content = self.topics.get(topic, "No information available.")
        self.animate_topic(content)

    def animate_topic(self, new_text):
        self.content_card.setText("")  # Clear for fade
        animation = QPropertyAnimation(self.content_card, b"windowOpacity")
        animation.setDuration(200)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()
        self.content_card.setHtml(new_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = CivicEducationApp()
    window.show()
    sys.exit(app.exec_())