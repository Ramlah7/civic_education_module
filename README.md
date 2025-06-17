
# 📘 Civic Education System

A modern, Gemini-powered desktop application built with **Python** and **PyQt5** that helps users learn about civic responsibilities, rights, and societal functions.

---

## 🚀 Features

- 📚 Browse curated civic education topics in a sidebar.
- 🔍 Real-time search through topics.
- 🤖 Chat with Google Gemini API to ask civic-related questions.
- 🧠 Switch seamlessly between static content and interactive chat.
- 🎨 Green-themed, clean, user-friendly interface.

---

## 🛠️ Technologies

- **Frontend**: PyQt5
- **Backend**: Python 3
- **AI Assistant**: Google Gemini API (`models/gemini-2.0-flash`)
- **Environment Config**: dotenv (`.env` file)
- **Data Source**: JSON (`topics.json`)

---

## 📂 File Structure

```
.
├── main.py               # Main PyQt5 application
├── topics.json           # JSON file with civic topics and HTML content
├── .env                  # Environment file with Gemini API key
├── requirements.txt      # Python package requirements
└── README.md             # Project documentation
```

---

## ✅ Requirements

Create a `.env` file containing:

```
GEMINI_API_KEY=your_google_gemini_api_key
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### requirements.txt

```
PyQt5>=5.15.0
python-dotenv>=1.0.0
google-generativeai>=0.3.0
```

---

## ▶️ Running the App

```bash
python main.py
```

---

## 🧠 How it Works

- Select a topic to view its structured explanation.
- Click **“Ask Your Question 🧠”** to switch to Gemini chatbot mode.
- Ask any civic-related question and get an instant AI-generated reply.
- Uses `QPropertyAnimation` for smooth transitions.

---


## 🙋‍♀️ Contributions

Pull requests welcome. For major changes, open an issue first to discuss.

