import json
import requests
import sys

def fetch_github_repositories(username):
    # Fetch public repositories sorted by recent updates
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    
    try:
        print(f"Connecting to GitHub REST API for user: {username}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data from GitHub: {e}")
        return None

def parse_and_filter_projects(raw_repos):
    project_list = []
    
    for repo in raw_repos:
        # Filter out forks or profile readme files to keep it clean
        if repo.get("fork", False) or repo.get("name") == repo.get("owner", {}).get("login"):
            continue
            
        # Standardize structural properties for front-end parsing
        project_data = {
            "name": repo.get("name"),
            "description": repo.get("description") or "An automated technical engineering project.",
            "url": repo.get("html_url"),
            "stars": repo.get("stargazers_count", 0),
            "language": repo.get("language") or "Mixed",
            "topics": repo.get("topics", [])
        }
        project_list.append(project_data)
        
    return project_list

def run():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    target_user = "awishpinto-cmd"
    raw_data = fetch_github_repositories(target_user)
    
    if raw_data is not None:
        clean_projects = parse_and_filter_projects(raw_data)
        
        # Output clean, pretty-printed JSON data file
        output_filename = "projects.json"
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(clean_projects, f, indent=4, ensure_ascii=False)
            
        print(f"Success! {len(clean_projects)} public projects written to {output_filename}.")

if __name__ == "__main__":
    run()