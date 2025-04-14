import os
import base64
import requests
import json

# Read values from environment variables
user = os.environ["CONFLUENCE_USER"]
pat = os.environ["CONFLUENCE_PAT"]
url = os.environ["CONFLUENCE_URL"]
space = os.environ["SPACE_KEY"]
parent = os.environ["PARENT_ID"]
module = os.environ["MODULE_NAME"]
prev = os.environ["PREVIOUS_VERSION"]
new = os.environ["NEW_VERSION"]

title = f"Release - {module} {new}"

# Create table HTML
table_html = f'''
<table>
  <tr><th>Module</th><th>Previous Version</th><th>New Version</th></tr>
  <tr><td>{module}</td><td>{prev}</td><td>{new}</td></tr>
</table>
'''

# Prepare the request
payload = {
    "type": "page",
    "title": title,
    "ancestors": [{"id": parent}],
    "space": {"key": space},
    "body": {
        "storage": {
            "value": table_html,
            "representation": "storage"
        }
    }
}

encoded = base64.b64encode(f"{user}:{pat}".encode()).decode()
headers = {
    "Authorization": f"Basic {encoded}",
    "Content-Type": "application/json"
}

print(f"📤 Creating page under parent {parent} with title '{title}'")
r = requests.post(f"{url}/rest/api/content", headers=headers, json=payload)

if r.status_code in [200, 201]:
    print("✅ Confluence page created successfully.")
else:
    print(f"❌ Failed with status {r.status_code}")
    print(r.text)
