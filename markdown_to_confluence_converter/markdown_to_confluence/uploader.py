import requests
from requests.auth import HTTPBasicAuth

def add_or_update_page(title, content, space_key, parent_id, base_url, username, api_token):
    """
    Add a new page to Confluence or update it if it already exists.

    Args:
    - title (str): The title of the page.
    - content (str): The HTML content of the page.
    - space_key (str): The key of the space in Confluence.
    - parent_id (int): The ID of the parent page in Confluence.
    - base_url (str): The base URL of the Confluence instance.
    - username (str): The Confluence username.
    - api_token (str): The API token for authentication.
    """
    # Initialize the variable to track if the page exists
    page_exists = False

    # Construct the URL for checking if the page exists
    url = f"{base_url}/rest/api/content?title={title}&spaceKey={space_key}&expand=version"
    response = requests.get(url, auth=HTTPBasicAuth(username, api_token))

    # If the page exists, prepare to update it
    if response.status_code == 200 and response.json()['results']:
        page = response.json()['results'][0]
        page_id = page['id']
        version = page['version']['number'] + 1
        page_exists = True
        url = f"{base_url}/rest/api/content/{page_id}"
        data = {
            "version": {"number": version},
            "title": title,
            "type": "page",
            "body": {
                "storage": {
                    "value": content,
                    "representation": "storage"
                }
            }
        }
        response = requests.put(url, json=data, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth(username, api_token))
    else:
        # If the page does not exist, create a new one
        data = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "ancestors": [{"id": parent_id}],
            "body": {
                "storage": {
                    "value": content,
                    "representation": "storage"
                }
            }
        }
        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth(username, api_token))

    # Log the outcome of the operation
    if response.status_code in [200, 201]:
        print(f"Page '{title}' successfully {'updated' if page_exists else 'created'} in Confluence.")
        return response.json()['id']
    else:
        print(f"Failed to {'update' if page_exists else 'create'} page in Confluence. Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return None
