import requests
import pandas as pd

def scrape_repository_commits(username, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    base_url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(base_url, headers=headers)
    repositories = response.json()

    all_commits_data = []

    for repo in repositories:
        repository_name = repo["name"]
        print(f"Scraping commits for repository: {repository_name}")

        commits_data = []
        repo_url = f"https://api.github.com/repos/{username}/{repository_name}/commits"
        repo_response = requests.get(repo_url, headers=headers)
        commits = repo_response.json()

        for commit in commits:
            commit_sha = commit["sha"]
            commit_date_full = commit["commit"]["author"]["date"]
            commit_date, commit_time = commit_date_full.split("T")
            commit_day = pd.to_datetime(commit_date_full).strftime('%A')
            commit_message = commit["commit"]["message"]

            diff_url = f"https://api.github.com/repos/{username}/{repository_name}/commits/{commit_sha}"
            diff_response = requests.get(diff_url, headers=headers)
            diff_data = diff_response.json()

            commit_diff = diff_data.get("files", [])
            commit_changes = "\n".join([file_change.get("patch", "") for file_change in commit_diff])

            commits_data.append({
                "Repository": repository_name,
                "Date": commit_date,
                "Time": commit_time,
                "Day": commit_day,
                "Commit Message": commit_message,
                "Changes": commit_changes
            })

        all_commits_data.extend(commits_data)

    return all_commits_data

def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    username = "your_username_here"
    token = "your_personal_access_token_here"
    filename = f"{username}_all_repositories_commits.xlsx"
    
    commits_data = scrape_repository_commits(username, token)
    save_to_excel(commits_data, filename)
    print(f"Data scraped and saved to {filename}")
