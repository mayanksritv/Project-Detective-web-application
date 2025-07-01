import requests
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# ========================
# Configuration
# ========================
GITHUB_TOKEN = "GITHUB API KEY"  # Replace with your actual token
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# ========================
# GitHub API Functions
# ========================
def search_github_repos(query, language="python", max_results=500):
    """Search up to 500 GitHub repositories using pagination."""
    repos = []
    base_url = "https://api.github.com/search/repositories"

    for page in range(1, 11):  # 5 pages x 100 = 500
        params = {
            "q": f"{query} language:{language}",
            "sort": "stars",
            "order": "desc",
            "per_page": 100,
            "page": page
        }

        try:
            response = requests.get(base_url, headers=HEADERS, params=params)
            response.raise_for_status()
            items = response.json().get("items", [])
            repos.extend(items)
            print(f"✅ Fetched {len(items)} repos on page {page}")

            if len(items) < 100:
                break  # Fewer results means we're at the end
        except Exception as e:
            print(f"⚠️ API Error on page {page}: {str(e)}")
            break

    return repos[:max_results]



def get_repo_text(repo):
    """Extract relevant text from repository data"""
    return f"{repo['name']} {repo.get('description', '')} {' '.join(repo.get('topics', []))}".lower()

# ========================
# Text Processing
# ========================
def preprocess_text(text):
    """Clean and normalize text for comparison"""
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    words = [word for word in text.split() if len(word) > 3]
    return ' '.join(words)

# ========================
# Analysis Core
# ========================
def calculate_uniqueness(user_idea, repo_texts):
    """Calculate project uniqueness score"""
    if not repo_texts:
        return 100.0
    
    clean_idea = preprocess_text(user_idea.lower())
    clean_repos = [preprocess_text(text) for text in repo_texts]

    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    vectors = vectorizer.fit_transform([clean_idea] + clean_repos)

    similarity_scores = cosine_similarity(vectors[0:1], vectors[1:])
    max_similarity = similarity_scores.max()

    return max(0.0, 100.0 - (max_similarity * 100))

# ========================
# Main Workflow
# ========================
def analyze_project(idea, language="python"):
    """Complete analysis workflow"""
    print(f"\n🔍 Analyzing: '{idea}'")

    repos = search_github_repos(idea, language)
    if not repos:
        return {"error": "No relevant projects found or API response was empty."}

    repo_texts = [get_repo_text(repo) for repo in repos]
    uniqueness = calculate_uniqueness(idea, repo_texts)

    return {
        "idea": idea,
        "uniqueness_score": round(uniqueness, 1),
        "similar_projects": [
            {
                "name": repo['name'],
                "url": repo['html_url'],
                "stars": repo['stargazers_count']
            } for repo in repos[:3]
        ]
    }

# ========================
# Execution & Output
# ========================
def main():
    user_idea = input("Enter your project idea: ")
    language = input("Programming language (default: python): ") or "python"

    report = analyze_project(user_idea, language)

    if "error" in report:
        print(f"❌ {report['error']}")
        return

    print(f"\n📊 Uniqueness Score: {report['uniqueness_score']}%")

    if report['uniqueness_score'] < 40:
        print("\n🔴 High Similarity Warning!")
        print("Most similar projects:")
        for idx, proj in enumerate(report['similar_projects'], 1):
            print(f" {idx}. {proj['name']} ({proj['stars']}⭐) - {proj['url']}")

    # Save to CSV
    pd.DataFrame([report]).to_csv("project_analysis.csv", index=False)
    print("\n📄 Report saved to project_analysis.csv")

if __name__ == "__main__":
    main()
