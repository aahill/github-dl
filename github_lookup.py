import requests
import re

def add_issues(json_results):
    # get the actual issues from the JSON response
    for issue in results:
        html_url = issue["html_url"]

        issue_obj = {
                "github_url": html_url,
                "article": "",
                "content_area": "",
                "message": issue["body"]
            }

        if "pull" not in html_url:
            try:
                article = re.search(r"Content Source: \[([^\]]*?\.md)", issue["body"]).group(1)
                content_area = re.search(r"cognitive-services\/(\S+?)\/", article).group(1)
                issue_obj["content_area"] = content_area
                issue_obj["article"] = article
                #organize the dictionary of issues by content area
                if not content_area in issues:
                    issues[content_area] = [issue_obj]
                else:
                    issues[content_area].append(issue_obj)
            except:
                issue_obj["article"] = "unknown"
                issue_obj["content_area"] = "unknown"
        else:
            pull_requests.append(issue_obj)


issues_endpoint = "https://api.github.com/repos/MicrosoftDocs/azure-docs/issues"
headers = {'Content-type': 'application/json'}
params = {
    "per_page": "100",
    "filter": "all", 
    "labels": "cognitive-services/svc"
    }
issues = {}
pull_requests = []


next_page = issues_endpoint

while next_page:
    response = requests.get(next_page, params=params, headers=headers)
    response.raise_for_status()
    results = response.json()
    if "next" in response.links:
        next_page = response.links["next"]['url']
    else:
        next_page = None
    results = response.json()
    add_issues(results)  

print("pull requests: ", len(pull_requests))

issue_total = len(pull_requests)
for content_area, issue in issues.items():
    print(content_area, len(issues[content_area]))
    issue_total += len(issues[content_area])

print('issue total: ', issue_total)




