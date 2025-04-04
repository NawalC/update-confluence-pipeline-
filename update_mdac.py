import os
import sys
import requests
import base64
import hashlib

def update_confluence(page_id, modules):
    # Get Confluence URL, username and personal access token (PAT) from environment variables
    confluence_url = os.environ["CONFLUENCE_URL"]
    username = os.environ["CONFLUENCE_USER"]
    pat = os.environ["CONFLUENCE_PAT"]

    # Create a basic authentication token
    credentials = f"{username}:{pat}"
    token = base64.b64encode(credentials.encode()).decode()

    # Set up the headers for the HTTP request
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json"
    }

    # Create the URL to fetch the current page content including its body and version
    url = f"{confluence_url}/rest/api/content/{page_id}?expand=body.storage,version"
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        return

    try:
        # Parse the JSON response
        data = response.json()
    except Exception:
        return

    # Increment the version number for the page update
    version = data["version"]["number"] + 1

    # Create an HTML table with the module information
    table_html = "<table><tr><th>Name</th><th>Version</th><th>Type</th></tr>"
    for m in modules:
        table_html += f"<tr><td>{m['name']}</td><td>{m['version']}</td><td>{m['type']}</td></tr>"
    table_html += "</table>"

    # Create the payload for the page update
    payload = {
        "version": {"number": version},
        "title": data["title"],
        "type": "page",
        "body": {
            "storage": {
                "value": table_html,
                "representation": "storage"
            }
        }
    }

    # Create the URL to update the page content
    update_url = f"{confluence_url}/rest/api/content/{page_id}"
    result = requests.put(update_url, headers=headers, json=payload)

def main():
    # Get the page ID and namespace from command-line arguments
    page_id = sys.argv[1]
    namespace = sys.argv[2]

    # Create a list of modules with their name, version, and type
    modules = [
        {"name": f"module-{namespace}", "version": "1.0.0", "type": "operator"},
        {"name": f"ui-{namespace}", "version": "2.0.1", "type": "frontend"}
    ]
    update_confluence(page_id, modules)

if __name__ == "__main__":
    main()
