from urllib.parse import urlparse
from collections import Counter
import json
import csv

def extract_github_references(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Extract the CVE_Items list
    cve_items = data.get("CVE_Items", [])

    github_entries = []
    for entry in cve_items:
        if "cve" in entry and "references" in entry["cve"] and "reference_data" in entry["cve"]["references"]:
            for ref in entry["cve"]["references"]["reference_data"]:
                if "url" in ref and "github.com" in ref["url"]:
                    github_entries.append(entry)
                    break  # Found a GitHub URL, no need to check further

    return github_entries

def rank_github_projects(cve_entries):
    project_count = Counter()

    for entry in cve_entries:
        if "cve" in entry and "references" in entry["cve"] and "reference_data" in entry["cve"]["references"]:
            for ref in entry["cve"]["references"]["reference_data"]:
                if "url" in ref and "github.com" in ref["url"]:
                    url_path = urlparse(ref["url"]).path
                    parts = url_path.split('/')
                    if len(parts) >= 3:
                        # The format is typically /user/project
                        user, project = parts[1], parts[2]
                        project_identifier = f"{user}/{project}"
                        project_count[project_identifier] += 1

    # Convert the counter to a list of (project, count) tuples
    ranked_projects = project_count.most_common()

    return ranked_projects

def save_descriptions_to_csv(cve_entries, csv_file_name):
    with open(csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Description'])  # Writing the header

        for entry in cve_entries:
            if "cve" in entry and "description" in entry["cve"] and "description_data" in entry["cve"]["description"]:
                descriptions = entry["cve"]["description"]["description_data"]
                for desc in descriptions:
                    if desc.get("lang", "") == "en":  # Assuming we're interested in English descriptions
                        description = desc.get("value", "")
                        csvwriter.writerow([description])
