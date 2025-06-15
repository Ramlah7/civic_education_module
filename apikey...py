import sys
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QListWidget, QTextBrowser, QLineEdit, QPushButton, QFrame, QLabel, QTextEdit, QScrollArea
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont

class CivicEducationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Civic Education System")
        self.resize(1000, 600)

        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            # Handle the case where API key is not found
            print("Error: GEMINI_API_KEY not found in your .env file.")
            # You might want to display a message box to the user here as well
            # QApplication.instance().quit() # Or exit the app gracefully
            sys.exit(1) # Exit if API key is critical for app function

        try:
            genai.configure(api_key=api_key)
            # Use a model that was found to be available and supports generateContent
            # Based on your output, 'models/gemini-2.0-flash' or 'models/gemini-1.5-flash'
            # are good choices for general chat.
            self.gemini_model = genai.GenerativeModel("models/gemini-2.0-flash")
            print(f"Successfully configured Gemini model: {self.gemini_model.model_name}")
        except Exception as e:
            print(f"Error configuring Gemini model: {e}")
            # Handle this error, e.g., display a message and disable chat features
            self.gemini_model = None # Ensure model is None if configuration fails

        self.topics = self.load_topics()
        self.init_ui()

    def load_topics(self):
        # Ensure 'topics.json' exists in the same directory as this script,
        # or provide a full path.
        try:
            with open("topics.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Error: topics.json not found. Please ensure it's in the correct directory.")
            return {"Welcome": "Welcome to the Civic Education System! No topics loaded due to missing file."}
        except json.JSONDecodeError:
            print("Error: Could not decode topics.json. Please check its format.")
            return {"Welcome": "Welcome to the Civic Education System! Topics file is corrupted."}


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
        self.topic_list.addItems(list(self.topics.keys()) + ["Ask Your Question 🤖"])
        self.topic_list.currentTextChanged.connect(self.display_topic)
        sidebar.addWidget(self.topic_list)

        layout.addLayout(sidebar, 2)

        # Main content card area
        self.content_stack = QVBoxLayout()
        layout.addLayout(self.content_stack, 5)

        # QTextBrowser for topics
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
                border: 1px solid #e0e0e0; /* Add a subtle border */
                box-shadow: 2px 2px 8px rgba(0,0,0,0.1); /* Add a subtle shadow */
            }
            a {
                color: #1976D2; /* Link color */
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        """)

        # Chat interface widgets
        self.chat_area = QVBoxLayout()
        self.chat_display = QTextBrowser()
        self.chat_display.setStyleSheet("""
            QTextBrowser {
                background-color: #F8F8F8; /* Light gray background for chat */
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                font-family: Segoe UI, sans-serif;
                border: 1px solid #e0e0e0;
            }
            b {
                color: #3F51B5; /* Blue for 'You' */
            }
            b:nth-of-type(odd) { /* Gemini's response */
                color: #4CAF50; /* Green for 'Gemini' */
            }
        """)
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Ask your civic question...")
        self.chat_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #BDBDBD;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }
        """)
        self.chat_send = QPushButton("Send")
        self.chat_send.clicked.connect(self.handle_chat)
        self.chat_send.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Green send button */
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #43A047; /* Darker green on hover */
            }
            QPushButton:pressed {
                background-color: #388E3C; /* Even darker on press */
            }
        """)
        self.chat_box = QWidget()
        chat_layout = QVBoxLayout(self.chat_box)
        chat_layout.addWidget(self.chat_display)
        chat_layout.addWidget(self.chat_input)
        chat_layout.addWidget(self.chat_send)
        self.chat_box.hide()

        self.content_stack.addWidget(self.content_card)
        self.content_stack.addWidget(self.chat_box)

        # Default selection
        self.topic_list.setCurrentRow(0)

    def filter_topics(self, text):
        self.topic_list.clear()
        filtered = [title for title in self.topics.keys() if text.lower() in title.lower()]
        self.topic_list.addItems(filtered + ["Ask Your Question 🤖"])

    def display_topic(self, topic):
        if topic == "Ask Your Question 🤖":
            self.content_card.hide()
            self.chat_box.show()
            self.chat_display.setText("Welcome! Ask your question about civic education below.")
        else:
            content = self.topics.get(topic, "No information available.")
            self.chat_box.hide()
            self.content_card.show()
            self.animate_topic(content)

    def animate_topic(self, new_text):
        # Create a temporary QTextBrowser to perform animation on
        temp_card = QTextBrowser()
        temp_card.setOpenExternalLinks(True)
        temp_card.setFrameShape(QFrame.StyledPanel)
        temp_card.setStyleSheet(self.content_card.styleSheet()) # Apply same style
        temp_card.setHtml(new_text)

        # Use an animation to fade out the old content and fade in the new
        # This requires more advanced handling if you want a true cross-fade.
        # For simplicity, this will just update the text after a brief delay/animation.
        # A more robust fade would involve stacking two QTextBrowsers and fading their opacities.

        # For a simple "clear and set" with a subtle animation, we clear first
        self.content_card.setText("")
        animation = QPropertyAnimation(self.content_card, b"windowOpacity")
        animation.setDuration(300) # Slightly longer duration for effect
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.finished.connect(lambda: self.content_card.setHtml(new_text)) # Set text when animation finishes fading in
        animation.start()


    def handle_chat(self):
        user_input = self.chat_input.text().strip()
        if not user_input:
            return

        self.chat_display.append(f"<b>You:</b> {user_input}")
        self.chat_input.clear()

        # Check if the model was successfully initialized
        if self.gemini_model is None:
            self.chat_display.append("<b>Gemini:</b> ⚠️ Error: AI chat functionality is not available. Model failed to load.")
            return

        try:
            # It's generally better to pass the entire history for context in a chat,
            # but for simplicity of this example, starting a new chat.
            # In a real chat app, you'd maintain self.chat_history and pass it.
            # For a more robust chat history:
            # history = []
            # for i in range(0, self.chat_display.document().blockCount()):
            #    block = self.chat_display.document().findBlockByNumber(i)
            #    text = block.text()
            #    if text.startswith("You:"):
            #        history.append({"role": "user", "parts": [text.replace("You:", "").strip()]})
            #    elif text.startswith("Gemini:"):
            #        history.append({"role": "model", "parts": [text.replace("Gemini:", "").strip()]})
            # chat = self.gemini_model.start_chat(history=history)

            chat = self.gemini_model.start_chat(history=[]) # Starting a fresh chat each time for simplicity
            response = chat.send_message(user_input)
            reply = response.text.strip()
        except Exception as e:
            reply = f"⚠️ Error: {str(e)}"
            print(f"Gemini API call failed: {e}") # Print full error to console for debugging

        self.chat_display.append(f"<b>Gemini:</b> {reply}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # A modern style for PyQt5 apps
    window = CivicEducationApp()
    window.show()
    sys.exit(app.exec_())