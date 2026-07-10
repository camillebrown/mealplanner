import requests
import json
from config import NOTION_TOKEN, NOTION_VERSION

BASE_URL = "https://api.notion.com/v1"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}

def post(path, payload):
    response = requests.post(f"{BASE_URL}{path}", headers=HEADERS, json=payload)
    try:
        data = response.json()
        if response.status_code >= 400:
            print(json.dumps(data, indent=2))
        return data
    except Exception:
        print(response.text)
        return None
def get(path):
    response = requests.get(f"{BASE_URL}{path}", headers=HEADERS)
    try:
        data = response.json()
        if response.status_code >= 400:
            print(json.dumps(data, indent=2))
        return data
    except Exception:
        print(response.text)
        return None
def patch(path, payload):
    response = requests.patch(f"{BASE_URL}{path}", headers=HEADERS, json=payload)
    try:
        data = response.json()
        if response.status_code >= 400:
            print(json.dumps(data, indent=2))
        return data
    except Exception:
        print(response.text)
        return None
def delete(path):
    response = requests.delete(f"{BASE_URL}{path}", headers=HEADERS)
    try:
        data = response.json()
        if response.status_code >= 400:
            print(json.dumps(data, indent=2))
        return data
    except Exception:
        print(response.text)
        return None
def rt(text, bold=False, color="default"):
    return [
    {
        "type": "text",
        "text": {"content": str(text)},
        "annotations": {
            "bold": bold,
            "color": color,
        },
    }
]

def diff_color(metric, value):
    if metric == "calories":
        return "green" if value <= 0 else "red"

    if metric == "protein":
        return "green" if value >= 0 else "red"

    if metric == "fat":
        return "green" if value <= 0 else "red"

    if metric == "carbs":
        return "blue"

    if metric == "fiber":
        return "green" if value >= 0 else "red"

    return "default"

def cell_text(cells):
    return [
        "".join(part["text"]["content"] for part in cell if part["type"] == "text")
        for cell in cells
    ]
    
def log_cell_changes(headers, old_cells, new_cells):
    changed = False

    for header, old_value, new_value in zip(headers, old_cells, new_cells):
        if old_value != new_value:
            changed = True
            print(f"  • {header}: {old_value} → {new_value}")

    return changed