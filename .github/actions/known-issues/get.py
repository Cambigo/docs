import os
import requests
import re
import sys
from datetime import datetime

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
        'labels': ['public', label]
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        issues = response.json()
        
        print(f"Found {len(issues)} issues with label '{label}' in {repository}")
        return issues
    except requests.exceptions.RequestException as e:
        print(f"Error fetching issues from {repository}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response content: {e.response.text}")
        return []

def format_date(iso_date_string):
    """Convert ISO date string to 'Month, Day Year' format."""
    try:
        # Parse the ISO date string (e.g., "2024-06-22T10:30:00Z")
        dt = datetime.fromisoformat(iso_date_string.replace('Z', '+00:00'))
        # Format as "Month, Day Year" (e.g., "June 22, 2024")
        return dt.strftime("%B %d, %Y")
    except (ValueError, AttributeError):
        return iso_date_string  

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
        known_issues_section += f"| Status      | Issue                                | Reported    |\n"
        known_issues_section += f"|-------------|--------------------------------------|-------------|\n"
        for issue in issues:
            formatted_date = format_date(issue['created_at'])
            if issue['state'] == 'closed':
                known_issues_section += f"| :material-check-decagram: Done | {issue['title']} | {formatted_date} |\n"
            else:
                known_issues_section += f"| :material-progress-wrench: Open | {issue['title']} | {formatted_date} |\n"

        known_issues_section += "\n"
    else:
        known_issues_section = "\n## Known Issues\n\n- [x] *No known issues at this time.*\n\n"
    

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