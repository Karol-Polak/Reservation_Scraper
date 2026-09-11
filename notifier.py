import os

import requests


API_URL = "https://api.github.com"


def _get_github_config():
    repository = os.getenv("GITHUB_REPOSITORY")
    token = os.getenv("GITHUB_TOKEN")

    return repository, token


def notification_exists(slot_id):
    repository, token = _get_github_config()

    if not repository or not token:
        return False

    url = f"{API_URL}/repos/{repository}/issues"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    params = {
        "state": "all",
        "per_page": 100,
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    issues = response.json()

    marker = f"<!-- SLOT_ID:{slot_id} -->"

    return any(
        marker in (issue.get("body") or "")
        for issue in issues
    )


def send_notification(title, body, slot_id):
    repository, token = _get_github_config()

    if not repository or not token:
        print("GitHub notification skipped - running locally.")
        print()
        print(body)
        return

    url = f"{API_URL}/repos/{repository}/issues"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    body_with_marker = (
        f"{body}\n\n"
        f"<!-- SLOT_ID:{slot_id} -->"
    )

    payload = {
        "title": title,
        "body": body_with_marker,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=15,
    )

    response.raise_for_status()