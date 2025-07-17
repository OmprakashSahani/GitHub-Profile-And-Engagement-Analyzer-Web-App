
# GitHub Profile & Engagement Analyzer Web App

## 🚀 Project Overview

The **GitHub Profile & Engagement Analyzer** is a powerful and interactive web application designed to provide comprehensive insights into any public GitHub user's profile and their repositories. Beyond standard GitHub statistics, this tool introduces unique metrics like a custom **Engagement Score** and visualizes a developer's most used programming languages, all presented through a modern, "coder-friendly" web interface.

This application is built with Python (Flask) on the backend, interacting with the GitHub REST API, and a dynamic frontend utilizing HTML, CSS, and locally-served Bootstrap.

**Live Demo:** [https://github-analyzer-app.el.r.appspot.com](https://github-analyzer-app.el.r.appspot.com)

---

## ✨ Features

-   **🔍 GitHub Profile Analysis:** Fetch and display core information about a GitHub user, including their name, bio, follower/following count, public repository count, and avatar.
-   **📈 Custom GitHub Engagement Score:** A unique, calculated score out of 100 that provides a qualitative assessment of a developer's activity and community interaction. This score is derived from:
    -   **Follower-to-Following Ratio:** Reflects community engagement.
    -   **Average Stars per Public Repository:** Indicates the popularity and impact of their work.
    -   **Recency of Code Pushes:** Measures recent activity across their public repositories.
-   **📊 Top N Most Used Languages:** Analyzes all public repositories to identify and display the top 5 (or configurable N) programming languages a developer primarily uses, offering insight into their skillset.
-   **🔎 Repository Deep Dive:** Allows users to select any public repository by a given user and fetch detailed information about it, including:
    -   Description, creation, update, and push dates.
    -   Open issues count (including Pull Requests).
    -   Forks, stars, and watchers.
    -   License and topics.
    -   A list of top contributors and their commit counts.
-   **🖥️ Modern Web Interface:** A sleek, dark-themed, and responsive design with a "coder/developer" aesthetic, providing an intuitive user experience. All main sections are visible on a single page, with longer lists being scrollable within their containers.

---

## 🛠️ Technologies Used

-   **Backend:**
    -   **Python 3.7+:** Core programming language.
    -   **Flask:** Lightweight web framework for building the API endpoints and serving the web interface.
    -   **Requests:** HTTP library for making API calls to GitHub.
-   **Frontend:**
    -   **HTML5:** Structure of the web pages.
    -   **CSS3:** Custom styling for the "coder vibe" theme.
    -   **Bootstrap 5.3.3:** Responsive design framework for modern UI components (served locally).
    -   **Jinja2:** Flask's templating engine for dynamic content rendering.
    -   **Google Fonts:** For modern typography (`Inter`, `Roboto Mono`).
-   **API:**
    -   **GitHub REST API:** For fetching all user and repository data.
-   **Tools:**
    -   **Git:** Version control.
    -   **pip:** Python package installer.
    -   **Virtual Environments (venv):** For dependency management.

---

## 🚀 Getting Started

Follow these step-by-step instructions to set up and run the GitHub Profile & Engagement Analyzer locally on your machine.

### Prerequisites

Before you begin, ensure you have the following installed on your system:

-   **Python 3.7 or higher:**
    -   Download from [python.org/downloads](https://www.python.org/downloads/).
    -   **Important:** During installation, make sure to check the box that says "Add Python to PATH".
-   **Git:**
    -   Download from [git-scm.com/downloads](https://git-scm.com/downloads).

### Step 1: Clone the Repository

Open your terminal or command prompt and clone this project:

```bash
git clone [https://github.com/OmprakashSahani/GitHub-Profile-And-Engagement-Analyzer-Web-App.git](https://github.com/OmprakashSahani/GitHub-Profile-And-Engagement-Analyzer-Web-App.git) # Replace with your actual repo URL
cd GitHub-Profile-And-Engagement-Analyzer-Web-App
````

### Step 2: Set up a Python Virtual Environment

A virtual environment is crucial for managing project dependencies, preventing conflicts with other Python projects or your system's global Python installation.

```bash
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
# On Windows (PowerShell in VS Code Terminal or Git Bash):
.\venv\Scripts\Activate
# On macOS/Linux/Git Bash:
source venv/bin/activate
```

You will know the virtual environment is active when you see `(venv)` at the beginning of your terminal prompt.

  * **Troubleshooting Activation on Windows (PowerShell):** If you encounter an error like "running scripts is disabled on this system," you might need to change your PowerShell Execution Policy.
    1.  Open **PowerShell as Administrator** (search for PowerShell, right-click, select "Run as administrator").
    2.  Run: `Set-ExecutionPolicy RemoteSigned`
    3.  Type `Y` and press Enter to confirm.
    4.  Close the Administrator PowerShell and try activating the `venv` again in your regular terminal.

### Step 3: Install Python Dependencies

With your virtual environment active, install the necessary Python libraries:

```bash
pip install Flask requests
```

### Step 4: GitHub Personal Access Token (PAT) Setup

To allow the application to make authenticated requests to the GitHub API (which provides higher rate limits and access to more data like user's own private repos if given permissions), you need a Personal Access Token.

1.  **Generate Your PAT:**

      - Log in to your GitHub account.
      - Go to your GitHub Settings: [https://github.com/settings/tokens](https://github.com/settings/tokens)
      - Click on **"Generate new token (classic)"**.
      - Provide a descriptive **Note** for your token (e.g., `GitHub Analyzer Web App`).
      - Set an **Expiration** date (e.g., 30 days, 90 days, or "No expiration" for development convenience, but consider security for longer terms).
      - **Select the necessary scopes (permissions) for the token:**
          - Under the `repo` section, check `public_repo` (Allows read access to public repositories).
          - Under the `user` section, check `read:user` (Allows read access to user profile data).
      - Click the **"Generate token"** button at the bottom.
      - **CRITICAL: Immediately copy the displayed token string\!** This is the **only time** GitHub will show you the full token. If you lose it, you'll have to generate a new one.

2.  **Set the PAT as an Environment Variable:**
    Your Flask application reads the PAT from an environment variable named `GITHUB_TOKEN`. **You must set this variable in your terminal session *before* running the Flask application.**

      - **On Windows (PowerShell in VS Code Terminal or Git Bash):**
        ```powershell
        $env:GITHUB_TOKEN="YOUR_ACTUAL_GITHUB_TOKEN_HERE"
        ```
      - **On macOS/Linux/Git Bash:**
        ```bash
        export GITHUB_TOKEN="YOUR_ACTUAL_GITHUB_TOKEN_HERE"
        ```

    (Remember to replace `YOUR_ACTUAL_GITHUB_TOKEN_HERE` with the token you copied from GitHub.)

### Step 5: Download & Serve Bootstrap/Popper.js Locally

To ensure the web interface's design loads correctly and to avoid potential Subresource Integrity (SRI) issues or reliance on external CDNs during development, Bootstrap's CSS and JavaScript files are served directly by your Flask application. These files are already referenced in `templates/index.html` via `url_for('static', filename='...')`.

You need to download these files once and place them in the `static/` folder:

1.  Navigate into the `static` folder within your project:
    ```bash
    cd static
    ```
2.  Download the following minified files and save them directly into this `static/` folder:
      - `bootstrap.min.css`: [https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css](https://www.google.com/search?q=https://cdn.jsdelivr.net/npm/bootstrap%405.3.3/dist/css/bootstrap.min.css)
      - `bootstrap.min.js`: [https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.min.js](https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.min.js)
      - `popper.min.js`: [https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js](https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js)
3.  After downloading, navigate back to the root of your project:
    ```bash
    cd ..
    ```

### Step 6: Run the Flask Application

With your virtual environment active and the `GITHUB_TOKEN` environment variable set, you can now start the Flask development server:

```bash
python app.py
```

You should see output in your terminal similar to:
`* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`

### Step 7: Access the Web Interface

Open your web browser and navigate to the address provided by Flask, which is typically:

```
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)
```

Now, enter any public GitHub username (e.g., `octocat`, `torvalds`, or your own: `OmprakashSahani`) in the input field and click "Analyze Profile" to see the magic happen\!

-----

## 📸 Screenshot

-----
Here are a few screenshots showcasing the application's interface and features:

### Initial Input Page
![Initial Input Page](https://github.com/OmprakashSahani/GitHub-Profile-And-Engagement-Analyzer-Web-App/blob/main/images/github-analyzer-demo%201.png)
*This image displays the clean, coder-themed initial input form.*

### Analyze Profile Page
![Analyze Profile Page](https://github.com/OmprakashSahani/GitHub-Profile-And-Engagement-Analyzer-Web-App/blob/main/images/github-analyzer-demo%202.png)  

![Analyze Profile Page](https://github.com/OmprakashSahani/GitHub-Profile-And-Engagement-Analyzer-Web-App/blob/main/images/github-analyzer-demo%203.png)

*This screenshot shows the main analysis output for a user's profile.*

### Repository Deep Dive
![Repository Deep Dive](https://github.com/OmprakashSahani/GitHub-Profile-And-Engagement-Analyzer-Web-App/blob/main/images/github-analyzer-demo%204.png)
*This screenshot highlights the detailed information provided for a specific repository.*


## 🔮 Future Enhancements

This project can be further expanded with exciting new features:

  - **Interactive Data Visualizations:** Integrate JavaScript charting libraries (e.g., Chart.js, D3.js) to create dynamic graphs for language distribution, contribution trends, or follower growth.
  - **User Authentication (OAuth):** Allow users to log in directly with their GitHub accounts to analyze private repositories (with appropriate permissions) and manage their own data within the app.
  - **Advanced Repository Metrics:** Implement analysis of pull request and issue statistics (e.g., average time to close issues, most active contributors by lines of code).
  - **Historical Data Tracking:** Store and display historical data for profiles/repositories to show trends over time.
  - **Deployment to Cloud Platform:** Host the application on a public cloud service (e.g., Google Cloud Platform, Heroku, Vercel) for wider accessibility.
  - **Cross-Profile Comparison:** Add functionality to compare metrics of two different GitHub profiles side-by-side.
  - **Optimized API Usage:** Implement more robust pagination handling for users with thousands of repositories/followers and explore GitHub GraphQL API for more efficient data fetching.

-----

## 📄 License

This project is open-source and licensed under the MIT License.

**MIT License Text:**

```
MIT License

Copyright (c) 2025 Omprakash Sahani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**To include the license in your repository:**

1.  In your `github-profile-analyzer-web` repository on GitHub.com, click the **"Add file"** button, then **"Create new file"**.
2.  Name the file exactly: `LICENSE.md`
3.  Copy the entire `MIT License Text` block (from `MIT License` down to `THE SOFTWARE.`) provided above and paste it into the `LICENSE.md` file.
4.  Commit the new file.

-----

## 📧 Contact

For any questions, feedback, or collaborations, feel free to reach out\!

  - **Omprakash Sahani**
  - GitHub: [https://github.com/OmprakashSahani](https://www.google.com/search?q=https://github.com/OmprakashSahani)
  - Email: Omprakash.Sahani7991@gmail.com

-----
