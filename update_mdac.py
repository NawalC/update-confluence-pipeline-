import os
import sys
import requests

def update_confluence(page_id, modules):
    confluence_url = os.environ["CONFLUENCE_URL"]
    jsessionid = os.environ["JSESSIONID"]

    session = requests.Session()
    session.cookies.set("JSESSIONID", jsessionid)

    headers = {
        "Content-Type": "application/json"
    }

    url = f"{confluence_url}/rest/api/content/{page_id}?expand=body.storage,version"

    print("📡 Requesting page info from:", url)
    response = session.get(url, headers=headers)

    print("🔎 Status Code:", response.status_code)
    print("📄 Response Preview (first 200 chars):", response.text[:200])

    if response.status_code != 200:
        print("❌ Failed to get page info — check cookie or session expiry")
        return

    data = response.json()
    version = data["version"]["number"] + 1

    table_html = "<table><tr><th>Name</th><th>Version</th><th>Type</th></tr>"
    for m in modules:
        table_html += f"<tr><td>{m['name']}</td><td>{m['version']}</td><td>{m['type']}</td></tr>"
    table_html += "</table>"

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

    update_url = f"{confluence_url}/rest/api/content/{page_id}"
    update_response = session.put(update_url, headers=headers, json=payload)

    if update_response.status_code == 200:
        print("✅ Page updated successfully.")
    else:
        print("❌ Failed to update page:", update_response.status_code)
        print("🔍 Response:", update_response.text[:300])

def main():
    page_id = sys.argv[1]
    namespace = sys.argv[2]
    modules = [
        {"name": f"module-{namespace}", "version": "1.0.0", "type": "operator"},
        {"name": f"ui-{namespace}", "version": "2.0.1", "type": "frontend"}
    ]
    update_confluence(page_id, modules)

if __name__ == "__main__":
    main()
