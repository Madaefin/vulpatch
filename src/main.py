import functions
import json


### Preliminary data analysis. Scan the CVE JSON and extract github CVE's, rank projects by number of CVE's 
# Usage
json_file = 'data\\nvdcve-1.1-2023.json'
github_cves = functions.extract_github_references(json_file)

# Output the number of entries with GitHub URLs and optionally print some of them
print(f"Entries with GitHub URLs: {len(github_cves)}")
print(json.dumps(github_cves[:5], indent=4))  # Print the first 5 for inspection

# Usage
ranked_projects = functions.rank_github_projects(github_cves)

# Print the top projects
for project, count in ranked_projects[:10]:  # Adjust number as needed
    print(f"{project}: {count} CVEs")

# Usage
csv_file_name = 'github_cve_descriptions.csv'
functions.save_descriptions_to_csv(github_cves, csv_file_name)

print(f"Descriptions have been saved to {csv_file_name}")