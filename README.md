# 🕵️‍♂️ Project Detective

**Project Detective** is a Flask-based web application that analyzes the uniqueness of a project idea by comparing it to existing GitHub repositories.

## 🚀 Features

- Enter a project idea or title
- Searches GitHub repositories using GitHub API or scraping
- Uses NLP techniques to compare similarities
- Returns a uniqueness score or match report

## 🛠️ Tech Stack

- Python 3.x
- Flask
- HTML/CSS (Jinja templates)
- GitHub API or scraping
- Scikit-learn / SpaCy / NLTK (for NLP)

## 🔧 Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/project-detective.git
   cd project-detective
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask app**
   ```bash
   python app.py
   ```

5. **Open in browser**
   Navigate to `http://localhost:5000`

## 📁 Folder Structure

- `app.py` – Main Flask server
- `templates/` – HTML templates (index, result, etc.)
- `static/` – CSS, images
- `utils/` – Backend utility scripts

## ✅ Future Enhancements

- Add authentication (e.g., GitHub OAuth)
- Improve UI with JavaScript and AJAX
- Use advanced ML/NLP models for better similarity detection

## 📄 License

MIT License

---

> Made with ❤️ by [Your Name]
