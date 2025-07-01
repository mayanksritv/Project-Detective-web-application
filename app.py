from flask import Flask, render_template, request, redirect
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import re

app = Flask(__name__)

# GitHub API Configuration
GITHUB_TOKEN = "GITHUB API KEY"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def search_github_repos(query, language="python", max_results=1000):
    base_url = "https://api.github.com/search/repositories"
    params = {
        "q": f"{query} language:{language}",
        "sort": "stars",
        "order": "desc",
        "per_page": min(max_results, 100)
    }
    try:
        response = requests.get(base_url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()["items"]
    except Exception as e:
        print(f"API Error: {str(e)}")
        return []

def get_repo_text(repo):
    return f"{repo['name']} {repo['description'] or ''} {repo['topics'] or ''}".lower()

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    words = [word for word in text.split() if len(word) > 3]
    return ' '.join(words)

def calculate_uniqueness(user_idea, repo_texts):
    if not repo_texts:
        return 100.0
    clean_idea = preprocess_text(user_idea.lower())
    clean_repos = [preprocess_text(text) for text in repo_texts]
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    vectors = vectorizer.fit_transform([clean_idea] + clean_repos)
    similarity_scores = cosine_similarity(vectors[0:1], vectors[1:])
    max_similarity = similarity_scores.max()
    return max(0.0, 100.0 - (max_similarity * 100))

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        idea = request.form.get("idea")
        language = request.form.get("language") or "python"

        repos = search_github_repos(idea, language)
        if not repos:
            result = {"error": f"No relevant projects found for '{idea}' in {language}"}
        else:
            repo_texts = [get_repo_text(repo) for repo in repos]
            uniqueness = calculate_uniqueness(idea, repo_texts)
            result = {
                "score": round(uniqueness, 1),
                "language": language,
                "similar_projects": [
                    {
                        "name": repo["name"],
                        "url": repo["html_url"],
                        "stars": repo["stargazers_count"]
                    } for repo in repos[:3]
                ]
            }
            pd.DataFrame([result]).to_csv("project_analysis.csv", index=False)
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
