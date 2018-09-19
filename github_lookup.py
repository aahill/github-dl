import requests
import re
issues_endpoint = "https://api.github.com/repos/MicrosoftDocs/azure-docs/issues"
params = {
    "filter": "all", 
    "labels": "cognitive-services/svc"
    }
issues = []
response = requests.get(issues_endpoint, params=params)
response.raise_for_status()
results = response.json()

for issue in results:

    article = re.search(r".*?Content Source: \[([^.md)]*\.md)", issue["body"]).group(1)
    content_area = re.search(r"cognitive-services/(\s+)/", article)
    issue_obj = {
        "github_url": issue["html_url"],
        "article": article,
        "content_area": content_area,
        "message": issue["body"]
    }
    print(issue_obj)
    issues.append(issue_obj)
#print (results)
