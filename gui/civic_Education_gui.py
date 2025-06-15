import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListView, QPushButton, QRadioButton, \
    QButtonGroup, QTextEdit, QHBoxLayout, QSpacerItem, QSizePolicy, QListWidget
from PyQt5.QtCore import Qt
import requests


class CivicEducationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Civic Education System")
        self.setGeometry(100, 100, 900, 600)

        # Main layout for the window
        layout = QVBoxLayout()

        # Title label with a customized style
        title_label = QLabel("Civic Education System")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2F4F4F; padding: 10px;")
        layout.addWidget(title_label)

        # Civics Topics Section
        self.topic_list = QListView()
        self.topic_list.setSelectionMode(QListView.SingleSelection)
        self.topic_list.setStyleSheet("background-color: #f0f0f0; padding: 10px;")
        self.topic_list.clicked.connect(self.display_topic_details)

        layout.addWidget(self.topic_list)

        # Topic Details Section
        self.topic_details = QTextEdit()
        self.topic_details.setReadOnly(True)
        self.topic_details.setStyleSheet("background-color: #f9f9f9; border: 1px solid #2F4F4F; padding: 10px;")
        layout.addWidget(self.topic_details)

        # Spacer to separate sections
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        # Interactive Quizzes Section
        self.quiz_label = QLabel("Question will appear here")
        self.quiz_label.setAlignment(Qt.AlignCenter)
        self.quiz_label.setStyleSheet("font-size: 18px; color: #2F4F4F; padding: 10px;")
        layout.addWidget(self.quiz_label)

        self.quiz_question = QLabel("What is the Constitution?")
        self.quiz_question.setAlignment(Qt.AlignCenter)
        self.quiz_question.setStyleSheet("font-size: 18px; color: #333333; padding: 10px;")
        layout.addWidget(self.quiz_question)

        # MCQ Options
        self.option1 = QRadioButton("Option 1: Constitution definition")
        self.option1.setStyleSheet("font-size: 16px; padding: 8px;")
        self.option2 = QRadioButton("Option 2: Voting rights")
        self.option2.setStyleSheet("font-size: 16px; padding: 8px;")
        self.option3 = QRadioButton("Option 3: Government structure")
        self.option3.setStyleSheet("font-size: 16px; padding: 8px;")

        self.option_group = QButtonGroup(self)
        self.option_group.addButton(self.option1)
        self.option_group.addButton(self.option2)
        self.option_group.addButton(self.option3)

        # Add the options to the layout
        layout.addWidget(self.option1)
        layout.addWidget(self.option2)
        layout.addWidget(self.option3)

        # Submit Button
        self.submit_button = QPushButton("Submit Answer")
        self.submit_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 18px; padding: 10px;")
        self.submit_button.clicked.connect(self.check_answer)
        layout.addWidget(self.submit_button)

        # News Section
        self.news_list = QListWidget()
        self.news_list.setStyleSheet("background-color: #f0f0f0; padding: 10px;")
        self.refresh_news()
        layout.addWidget(self.news_list)

        # Refresh Button
        self.refresh_button = QPushButton("Refresh News")
        self.refresh_button.setStyleSheet("background-color: #2196F3; color: white; font-size: 18px; padding: 10px;")
        self.refresh_button.clicked.connect(self.refresh_news)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)

    def display_topic_details(self):
        # Show details of the selected topic
        topic_index = self.topic_list.selectedIndexes()[0].row()
        topic_name = self.topics[topic_index]
        self.topic_details.setText(f"Details about {topic_name}: This is the explanation of the topic.")

    def check_answer(self):
        # Check selected answer
        if self.option1.isChecked():
            result = "Correct!"
            self.quiz_label.setStyleSheet("font-size: 18px; color: green; padding: 10px;")
        else:
            result = "Incorrect, try again."
            self.quiz_label.setStyleSheet("font-size: 18px; color: red; padding: 10px;")
        self.quiz_label.setText(result)

    def refresh_news(self):
        # Fetch live news from Google Custom Search API (or any other source)
        api_key = "your_google_api_key"
        search_engine_id = "your_search_engine_id"
        query = "civic education"
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={search_engine_id}"

        response = requests.get(url)
        news_data = response.json()

        self.news_list.clear()
        for item in news_data['items'][:5]:
            self.news_list.addItem(item['title'])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CivicEducationApp()
    window.show()
    sys.exit(app.exec_())
