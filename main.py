import sys
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QListWidget, QTextBrowser, QLineEdit, QPushButton, QFrame, QLabel
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QPalette

class CivicEducationApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Civic Education System")
        self.resize(1000, 600)

        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            print("Error: GEMINI_API_KEY not found in your .env file.")
            sys.exit(1)

        try:
            genai.configure(api_key=api_key)
            self.gemini_model = genai.GenerativeModel("models/gemini-2.0-flash")
            print(f"Successfully configured Gemini model: {self.gemini_model.model_name}")
        except Exception as e:
            print(f"Error configuring Gemini model: {e}")
            self.gemini_model = None

        self.topics = self.load_topics()
        self.init_ui()

    def load_topics(self):
        try:
            with open("topics.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Error: topics.json not found.")
            return {"Welcome": "Welcome to the Civic Education System!"}
        except json.JSONDecodeError:
            print("Error: topics.json format issue.")
            return {"Welcome": "Welcome! Topics file is corrupted."}

    def init_ui(self):
        primary = "#0D1B2A"
        secondary = "#1B263B"
        accent = "#415A77"
        bg = "#E0E1DD"
        surface = "#C0C9EE"
        text_primary = "#0D1B2A"

        container = QWidget()
        self.setCentralWidget(container)

        outer_layout = QVBoxLayout(container)

        self.title = QLabel("\U0001F4D8 Civic Education System")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet(f"""
            QLabel {{
                font-size: 32px;
                font-weight: bold;
                color: {bg};
                background-color: {primary};
                padding: 16px;
                border-bottom: 2px solid {accent};
            }}
        """)
        outer_layout.addWidget(self.title)

        layout = QHBoxLayout()
        outer_layout.addLayout(layout)

        sidebar = QVBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search topics...")
        self.search_bar.textChanged.connect(self.filter_topics)
        self.search_bar.setStyleSheet(f"""
            QLineEdit {{
                padding: 12px;
                border-radius: 12px;
                border: 1px solid {accent};
                font-size: 16px;
                color: {text_primary};
                background-color: {surface};
            }}
        """)
        sidebar.addWidget(self.search_bar)

        self.topic_list = QListWidget()
        self.topic_list.addItems(sorted(set(self.topics.keys()) | {"Ask Your Question 🧠"}))
        self.topic_list.currentTextChanged.connect(self.display_topic)
        self.topic_list.setStyleSheet(f"""
            QListWidget {{
                border: none;
                font-size: 16px;
                background-color: {bg};
                padding: 10px;
                color: {text_primary};
            }}
            QListWidget::item:selected {{
                background-color: {accent};
                color: {bg};
            }}
        """)
        sidebar.addWidget(self.topic_list)

        layout.addLayout(sidebar, 2)

        self.content_stack = QVBoxLayout()
        layout.addLayout(self.content_stack, 5)

        self.content_card = QTextBrowser()
        self.content_card.setOpenExternalLinks(True)
        self.content_card.setFrameShape(QFrame.StyledPanel)
        self.content_card.setStyleSheet(f"""
            QTextBrowser {{
                background-color: {bg};
                border-radius: 18px;
                padding: 24px;
                font-size: 16px;
                font-family: 'Segoe UI';
                border: 1px solid {surface};
                color: {text_primary};
            }}
        """)

        self.chat_box = QWidget()
        chat_layout = QVBoxLayout(self.chat_box)

        self.chat_display = QTextBrowser()
        self.chat_display.setStyleSheet(f"""
            QTextBrowser {{
                background-color: {surface};
                border-radius: 12px;
                padding: 20px;
                font-size: 15px;
                font-family: 'Segoe UI';
                border: 1px solid {surface};
                color: "030303";
            }}
        """)

        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Ask your civic question...")
        self.chat_input.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {accent};
                border-radius: 10px;
                padding: 12px;
                font-size: 15px;
                color: {text_primary};
                background-color: white;
            }}
        """)

        self.chat_send = QPushButton("Send")
        self.chat_send.clicked.connect(self.handle_chat)
        self.chat_send.setStyleSheet(f"""
            QPushButton {{
                background-color: {accent};
                color: white;
                border-radius: 12px;
                padding: 12px 24px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {secondary};
            }}
        """)

        chat_layout.addWidget(self.chat_display)
        chat_layout.addWidget(self.chat_input)
        chat_layout.addWidget(self.chat_send)

        self.chat_box.hide()

        self.content_stack.addWidget(self.content_card)
        self.content_stack.addWidget(self.chat_box)

        self.topic_list.setCurrentRow(0)

    def filter_topics(self, text):
        self.topic_list.clear()
        filtered = [t for t in self.topics if text.lower() in t.lower()]
        self.topic_list.addItems(sorted(filtered + ["Ask Your Question 🧠"]))

    def display_topic(self, topic):
        if topic == "Ask Your Question 🧠":
            self.content_card.hide()
            self.chat_box.show()
            self.chat_display.setText("\u2728 Welcome! Ask your civic education question below.")
        else:
            content = self.topics.get(topic, "No content found for this topic.")
            self.chat_box.hide()
            self.content_card.show()
            self.animate_topic(content)

    def animate_topic(self, new_text):
        self.content_card.hide()
        self.content_card.setHtml(new_text)
        self.content_card.show()

        animation = QPropertyAnimation(self.content_card, b"windowOpacity")
        animation.setDuration(500)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()

    def handle_chat(self):
        user_input = self.chat_input.text().strip()
        if not user_input:
            return

        self.chat_display.append(f"<b>You:</b> {user_input}")
        self.chat_input.clear()

        if self.gemini_model is None:
            self.chat_display.append("<b>Gemini:</b> ⚠️ Chat feature not available.")
            return

        try:
            chat = self.gemini_model.start_chat(history=[])
            response = chat.send_message(user_input)
            reply = response.text.strip()
        except Exception as e:
            reply = f"⚠️ Error: {str(e)}"
            print(f"Gemini error: {e}")

        self.chat_display.append(f"<b>Gemini:</b> {reply}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = CivicEducationApp()
    window.show()
    sys.exit(app.exec_())
