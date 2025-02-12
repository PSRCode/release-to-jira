import os

import requests
from requests.auth import HTTPBasicAuth

BASE = os.environ["INPUT_JIRA_SERVER"]
PROJECT = os.environ["INPUT_JIRA_PROJECT"]
TOKEN = os.environ["INPUT_JIRA_TOKEN"]

base_url = f"{BASE}/rest/api/2/"
project_path = f"project/{PROJECT}"
headers = {"Authorization": f"Bearer {TOKEN}"}


def get(endpoint, params=None):
    return requests.get(
        base_url + project_path + "/" + endpoint, params=params, headers=headers
    ).json()


def post(endpoint, body):
    return requests.post(base_url + endpoint, json=body, headers=headers)


def put(endpoint, body):
    return requests.put(base_url + endpoint, json=body, headers=headers)


def get_project_id():
    return get("")["id"]


def get_or_create_release(release_name):
    result = get("versions", {})
    for release in result:
        if release["name"] == release_name:
            # Found the release by name
            return release["name"]
    
    # No release found, create a new one
    return post(
        "version",
        {"name": release_name, "projectId": get_project_id(), "released": "true"},
    ).json()


def add_release_to_issue(release_name, issue):
    response = put(
        f"issue/{issue}",
        {"update": {"fixVersions": [{"add": {"name": release_name}}]}},
    )
    response.raise_for_status()
    return response.status_code == 204
