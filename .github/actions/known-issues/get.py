import os
import requests
import re
import sys

def fetch_known_issues():
    """Fetch issues labeled with specified label from the target repository."""
    token = os.environ.get('GITHUB_TOKEN')
    repository = os.environ.get('REPOSITORY', 'Cambigo/cambigo-flow')
    label = os.environ.get('LABEL', 'known issue')
    
    if not token:
        print("No GitHub token found, skipping known issues update")
        return []
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = f'https://api.github.com/repos/{repository}/issues'
    params = {
        'labels': label,
        'state': 'open'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        issues = response.json()
        
        print(f"Found {len(issues)} issues with label '{label}' in {repository}")
        return [{'title': issue['title'], 'url': issue['html_url'], 'number': issue['number']} for issue in issues]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching issues from {repository}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        return []

def update_releases_page(issues):
    """Update the releases.md file with known issues."""
    releases_path = os.environ.get('RELEASES_FILE', 'docs/releases.md')
    
    if not os.path.exists(releases_path):
        print(f"Releases file not found at {releases_path}")
        return
    
    with open(releases_path, 'r') as f:
        content = f.read()
    
    if issues:
        known_issues_section = "\n## Known Issues\n\n"
        for issue in issues:
            if issue['state'] == 'closed':
                known_issues_section += f"- [x] {issue['title']} (**{issue['state']}**) {issue['created_at']}\n"
            else:
                known_issues_section += f"- [ ] {issue['title']} (**{issue['state']}**) {issue['created_at']}\n"

        known_issues_section += "\n"
    else:
        known_issues_section = "\n## Known Issues\n\n*No known issues at this time.*\n\n"
    
    pattern = r'\n## Known Issues\n\n.*?(?=\n## |\n> |\Z)'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    if '%%KNOWN_ISSUES%%' in content:
        content = content.replace('%%KNOWN_ISSUES%%', known_issues_section)
    
    with open(releases_path, 'w') as f:
        f.write(content)
    
    print(f"Updated {releases_path} with {len(issues)} known issues")

def main():
    """Main function to fetch issues and update releases page."""
    try:
        issues = fetch_known_issues()
        update_releases_page(issues)
        print("Successfully updated releases page with known issues")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()