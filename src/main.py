from functions import functions

owner = 'comfyanonymous'
repo = 'ComfyUI'

#Obtaining the username and repo for the top GitHub project
project_info_list=functions.get_top_github_projects('10') # Input is the top project range

#Iterating over the project and obtaining the issues data
for i in range(len(project_info_list)):  
    owner = project_info_list[i]['username']
    repo = project_info_list[i]['repo']
    functions.download_github_issues(owner, repo)