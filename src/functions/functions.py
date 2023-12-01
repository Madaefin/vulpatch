import requests

def download_github_issues(owner, repo):
    api_url = f'https://api.github.com/repos/{owner}/{repo}/issues'
    
    # Make a GET request to the GitHub API
    response = requests.get(api_url)
    
    if response.status_code == 200:
        issues = response.json()
        
        # Print or process the issues as needed
        for issue in issues:
            #print(issue)
            print(f"Issue #{issue['number']}: {issue['title']}")
            
    else:
        print(f"Failed to fetch issues. Status code: {response.status_code}")
        print(response.text)

def get_top_github_projects(project_number):
    api_url = 'https://api.github.com/search/repositories'
    
    # Set up parameters for the search query
    params = {
        'q': 'stars:>0',  # Search for repositories with at least one star
        'sort': 'stars',  # Sort by stars
        'order': 'desc',  # Order in descending order (most stars first)
        'per_page': project_number    # Number of results per page
    }

    # Make a GET request to the GitHub API
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        projects = response.json()['items']
        
        # List to store project information
        project_info_list = []
        
        # Store the project information in the list
        for project in projects:
            project_info = {
                'username': project['owner']['login'],
                'repo': project['name'],
                'stars': project['stargazers_count']
            }
            project_info_list.append(project_info)
            
            # Print the information if needed
            print(f"Username: {project_info['username']}, Repo: {project_info['repo']}, Stars: {project_info['stars']}")
            
        return project_info_list
            
    else:
        print(f"Failed to fetch projects. Status code: {response.status_code}")
        print(response.text)
    