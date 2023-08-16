import requests
import pandas as pd

def scrape_repository_commits(username, repository_name, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    base_url = f"https://api.github.com/repos/{username}/{repository_name}/commits"
    response = requests.get(base_url, headers=headers)
    commits = response.json()

    commits_data = []

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

    return commits_data

def save_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    username = "your_username_here"
    repository_name = "your_repository_name_here"
    token = "your_personal_access_token_here"
    filename = f"{repository_name}_commits.xlsx"
    
    commits_data = scrape_repository_commits(username, repository_name, token)
    save_to_excel(commits_data, filename)
    print(f"Data scraped and saved to {filename}")


