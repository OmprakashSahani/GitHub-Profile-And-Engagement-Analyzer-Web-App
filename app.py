from flask import Flask, render_template, request, redirect, url_for # Added redirect, url_for
import os
from datetime import datetime, timedelta, timezone 
from collections import Counter
import requests

app = Flask(__name__)

# --- Configuration ---
# Your GitHub Personal Access Token (PAT) should be set as an environment variable.
# For Windows PowerShell: $env:GITHUB_TOKEN="YOUR_ACTUAL_GITHUB_TOKEN_HERE"
# For macOS/Linux/Git Bash: export GITHUB_TOKEN="YOUR_ACTUAL_GITHUB_TOKEN_HERE"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN') 

# --- Base URL for GitHub API ---
BASE_API_URL = 'https://api.github.com'

# --- Headers for Authentication and API Version ---
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json' 
}

# --- Helper Functions (Copied from github_profile.py) ---

def get_github_data(endpoint):
    """
    Helper function to make authenticated GET requests to the GitHub API.
    """
    url = f'{BASE_API_URL}{endpoint}'
    print(f"Fetching data from: {url}...") # This print will go to your terminal where Flask is running
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from {url}: {response.status_code}")
        try:
            error_message = response.json().get('message', response.text)
            print(f"GitHub Error: {error_message}")
            if response.status_code == 403 and 'rate limit exceeded' in error_message.lower():
                print("You might have hit the GitHub API rate limit. Please wait and try again.")
        except requests.exceptions.JSONDecodeError:
            print(response.text) 
        return None

def calculate_recency_score(repos_data):
    """
    Calculates a recency score based on the 'pushed_at' timestamp of repositories.
    More recent pushes contribute higher to the score.
    """
    if not repos_data:
        return 0

    total_recency_score = 0
    now = datetime.now(timezone.utc) # Use timezone.utc for awareness

    for repo in repos_data:
        pushed_at_str = repo.get('pushed_at')
        if pushed_at_str:
            try:
                pushed_at = datetime.fromisoformat(pushed_at_str.replace('Z', '+00:00'))
                
                days_ago = (now - pushed_at).days

                if days_ago <= 7:
                    total_recency_score += 10 
                elif days_ago <= 30:
                    total_recency_score += 5  
                elif days_ago <= 90:
                    total_recency_score += 2  
                elif days_ago <= 365:
                    total_recency_score += 0.5 
            except ValueError:
                print(f"Warning: Could not parse pushed_at for repo {repo.get('name')}: {pushed_at_str}")
    
    num_active_repos = 0
    for repo in repos_data:
        pushed_at_str = repo.get('pushed_at', '1970-01-01T00:00:00Z') 
        try:
            pushed_at = datetime.fromisoformat(pushed_at_str.replace('Z', '+00:00'))
            if (now - pushed_at).days <= 365:
                num_active_repos += 1
        except ValueError:
            pass 

    return total_recency_score / num_active_repos if num_active_repos > 0 else 0


def calculate_user_engagement_score(user_data, repos_data):
    """
    Calculates an overall engagement score for a GitHub user.
    """
    score = 0

    # Component 1: Follower Ratio (max contribution: 30 points)
    followers = user_data.get('followers', 0)
    following = user_data.get('following', 0)
    follower_ratio = 0
    if (followers + following) > 0:
        follower_ratio = followers / (followers + following)
    score += follower_ratio * 30 

    # Component 2: Average Stars per Public Repo (max contribution: 40 points)
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)
    public_repos_count = user_data.get('public_repos', 0)
    avg_stars_per_repo = 0
    if public_repos_count > 0:
        avg_stars_per_repo = total_stars / public_repos_count
    
    max_avg_stars_for_score = 10 
    normalized_avg_stars = min(avg_stars_per_repo / max_avg_stars_for_score, 1) 
    score += normalized_avg_stars * 40 

    # Component 3: Recency of Pushes (max contribution: 30 points)
    recency_score_value = calculate_recency_score(repos_data)
    
    max_recency_score_for_user = 50 
    normalized_recency = min(recency_score_value / max_recency_score_for_user, 1)
    score += normalized_recency * 30 

    return round(score, 2) 


def get_top_languages(repos_data, top_n=5):
    """
    Analyzes a list of repositories and returns the top N most used languages.
    Excludes repositories where the language is None (e.g., shell scripts, markdowns without primary language).
    """
    if not repos_data:
        return {}

    languages = []
    for repo in repos_data:
        language = repo.get('language')
        if language: 
            languages.append(language)
    
    language_counts = Counter(languages)
    
    return language_counts.most_common(top_n)

def get_repository_contributors(owner, repo_name, top_n=5):
    """
    Fetches and returns the top N contributors for a given repository.
    """
    endpoint = f'/repos/{owner}/{repo_name}/contributors'
    contributors_data = get_github_data(f'{endpoint}?per_page={top_n}') 
    
    if contributors_data:
        return [{'login': c.get('login'), 'contributions': c.get('contributions')} 
                for c in contributors_data]
    return []

# --- Flask Routes ---

@app.route('/')
def index():
    # Pass initial empty data to the template
    return render_template('index.html', user_data=None, repos_data=None, 
                           top_languages=None, engagement_score=None, 
                           repo_detail_data=None, contributors=None, 
                           error=None, current_username=None)

@app.route('/analyze', methods=['POST']) 
def analyze():
    # Ensure GITHUB_TOKEN is set
    if not GITHUB_TOKEN:
        error_message = "Error: GITHUB_TOKEN environment variable not set on the server." \
                        "Please configure it properly."
        return render_template('index.html', error=error_message)

    # Get username from the form submission
    username_input = request.form.get('username').strip()
    if not username_input:
        error_message = "Error: GitHub username cannot be empty."
        return render_template('index.html', error=error_message)

    # --- Fetch User Profile ---
    user_data = get_github_data(f'/users/{username_input}')

    if not user_data:
        error_message = f"Could not retrieve profile data for '{username_input}'. Please check the username or API permissions."
        return render_template('index.html', error=error_message)

    # --- Fetch Public Repositories ---
    repos_data = get_github_data(f'/users/{username_input}/repos?type=public&sort=pushed&per_page=100')

    # Calculate Engagement Score and Top Languages only if repos_data is available
    engagement_score = None
    top_languages = None
    if repos_data is not None:
        engagement_score = calculate_user_engagement_score(user_data, repos_data)
        top_languages = get_top_languages(repos_data, top_n=5)
    else:
        pass 

    # Pass all fetched data to the template for rendering
    return render_template('index.html', 
                           user_data=user_data, 
                           repos_data=repos_data, 
                           top_languages=top_languages, 
                           engagement_score=engagement_score,
                           current_username=username_input,
                           error=None) 

# --- Route for Repository Deep Dive ---
@app.route('/repo_deep_dive', methods=['POST'])
def repo_deep_dive():
    if not GITHUB_TOKEN:
        error_message = "Error: GITHUB_TOKEN environment variable not set on the server."
        return render_template('index.html', error=error_message)

    owner = request.form.get('owner').strip()
    repo_name = request.form.get('repo_name').strip()

    if not owner or not repo_name:
        error_message = "Error: Owner and repository name cannot be empty for deep dive."
        return render_template('index.html', error=error_message)
    
    repo_detail_data = get_github_data(f'/repos/{owner}/{repo_name}')
    contributors = []
    if repo_detail_data:
        contributors = get_repository_contributors(owner, repo_name, top_n=5)
    
    # We need to re-fetch main user data to keep the initial page context
    # This is important so the user profile and repo list remain on the page
    # when they perform a deep dive.
    user_data = get_github_data(f'/users/{owner}')
    repos_data = get_github_data(f'/users/{owner}/repos?type=public&sort=pushed&per_page=100')
    engagement_score = calculate_user_engagement_score(user_data, repos_data) if user_data and repos_data else None
    top_languages = get_top_languages(repos_data, top_n=5) if repos_data else None

    return render_template('index.html',
                           user_data=user_data,
                           repos_data=repos_data,
                           top_languages=top_languages,
                           engagement_score=engagement_score,
                           current_username=owner, 
                           repo_detail_data=repo_detail_data,
                           contributors=contributors,
                           error=None)


# --- Run the application ---
if __name__ == '__main__':
    app.run(debug=True)