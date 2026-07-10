import json
import subprocess
import sys
from datetime import datetime, timedelta

from config import SUMMARY_DATABASE_ID
from notion import patch, post


def build_week_info(start_date_text):
    start = datetime.strptime(start_date_text, "%Y-%m-%d")
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


def main(start_date_arg=None):
    if start_date_arg is None and len(sys.argv) != 2:
        print("Usage:")
        print("python3 main.py 2026-07-13")
        sys.exit(1)

    week = build_week_info(start_date_arg or sys.argv[1])
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

    pretty = json.dumps(result, indent=2)
    print(pretty)
    subprocess.run(["pbcopy"], input=pretty.encode())
    print("\n✅ Copied to clipboard")


if __name__ == "__main__":
    main()