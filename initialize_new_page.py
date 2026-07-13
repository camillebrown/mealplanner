import json
import subprocess
import sys
import importlib.util
import os
from datetime import datetime, timedelta


from config import SUMMARY_DATABASE_ID
from notion import patch, post

def parse_plan_name(plan_name):
    try:
        start_date = datetime.strptime(
            plan_name.title(),
            "%B_%d_%Y",
        ).date()
    except ValueError:
        raise ValueError(
            "Meal plan name must use this format: july_20_2026"
        )

    return start_date

def validate_meal_plan_exists(plan_name):
    path = os.path.join(
        "meal_plans",
        f"{plan_name}.py",
    )

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Meal plan '{plan_name}' was not found at {path}"
        )

def build_week_info(start_date):
    start = datetime.combine(start_date, datetime.min.time())
    end = start + timedelta(days=6)

    if start.year == end.year:
        if start.month == end.month:
            title = f"{start.strftime('%B')} {start.day}-{end.day}, {start.year}"
        else:
            title = (
                f"{start.strftime('%b')} {start.day} - "
                f"{end.strftime('%b')} {end.day}, {start.year}"
            )
    else:
        title = (
            f"{start.strftime('%b')} {start.day}, {start.year} - "
            f"{end.strftime('%b')} {end.day}, {end.year}"
        )

    return {
        "title": title,
        "start_date": start.strftime("%Y-%m-%d"),
        "end_date": end.strftime("%Y-%m-%d"),
    }


def find_latest_blank_week():
    data = post(
        f"/databases/{SUMMARY_DATABASE_ID}/query",
        {
            "sorts": [{"timestamp": "created_time", "direction": "descending"}],
            "page_size": 20,
        },
    )

    for page in data.get("results", []):
        props = page["properties"]
        start = props["Start"]["date"]
        end = props["End"]["date"]

        if start is None or end is None:
            return page

    return None


def main(plan_name=None):
    if plan_name is None and len(sys.argv) != 2:
        print("Usage:")
        print("python3 initialize_new_page.py july_20_2026")
        sys.exit(1)

    plan_name = plan_name or sys.argv[1]

    validate_meal_plan_exists(plan_name)

    start_date = parse_plan_name(plan_name)

    week = build_week_info(start_date)
    
    blank_page = find_latest_blank_week()

    if not blank_page:
        result = {"success": False, "message": "No blank week found."}
    else:
        page_id = blank_page["id"]

        updated = patch(
            f"/pages/{page_id}",
            {
                "properties": {
                    "Week": {
                        "title": [
                            {"type": "text", "text": {"content": week["title"]}}
                        ]
                    },
                    "Start": {"date": {"start": week["start_date"]}},
                    "End": {"date": {"start": week["end_date"]}},
                }
            },
        )

        result = {
            "success": True,
            "title": week["title"],
            "start": week["start_date"],
            "end": week["end_date"],
            "page_id": page_id,
            "url": updated.get("url") if updated else None,
        }
        
        return result

    pretty = json.dumps(result, indent=2)
    print(pretty)
    subprocess.run(["pbcopy"], input=pretty.encode())
    print("\n✅ Copied to clipboard")


if __name__ == "__main__":
    main()