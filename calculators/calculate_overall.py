from config import SUMMARY_DATABASE_ID
from notion import cell_text, diff_color, get, log_cell_changes, patch, post, rt

PARENT_PAGE_ID = "12a09d0c-5d76-44ad-aa3c-dd545b3b0c20"


def fmt(value):
    value = round(value, 1)
    return int(value) if value == int(value) else value


def children(block_id):
    return get(f"/blocks/{block_id}/children?page_size=100")["results"]


def signed(value, suffix=""):
    value = fmt(value)
    sign = "+" if value > 0 else ""
    return f"{sign}{value}{suffix}"


def avg_difference_cells(averages):
    return [
        rt("Avg Difference", bold=True),
        rt(signed(averages["calories"]), bold=True, color=diff_color("calories", averages["calories"])),
        rt(signed(averages["protein"], " g"), bold=True, color=diff_color("protein", averages["protein"])),
        rt(signed(averages["fat"], " g"), bold=True, color=diff_color("fat", averages["fat"])),
        rt(signed(averages["carbs"], " g"), bold=True, color=diff_color("carbs", averages["carbs"])),
        rt(signed(averages["fiber"], " g"), bold=True, color=diff_color("fiber", averages["fiber"])),
    ]


def find_overall_table():
    page_blocks = children(PARENT_PAGE_ID)

    for index, block in enumerate(page_blocks):
        if block["type"] == "heading_2":
            text = "".join(t.get("plain_text", "") for t in block["heading_2"]["rich_text"])

            if "Overall Average vs. Goal" in text:
                for next_block in page_blocks[index + 1:]:
                    if next_block["type"] == "table":
                        return next_block

    raise Exception("Overall Average vs. Goal table not found.")


def get_weeks():
    data = post(
        f"/databases/{SUMMARY_DATABASE_ID}/query",
        {
            "filter": {"property": "Start", "date": {"is_not_empty": True}},
            "page_size": 100,
        },
    )

    return data.get("results", [])


def calculate_overall():
    weeks = get_weeks()

    totals = {
        "calories": 0,
        "protein": 0,
        "fat": 0,
        "carbs": 0,
        "fiber": 0,
    }

    count = 0

    for week in weeks:
        props = week["properties"]

        values = {
            "calories": props["Calories (+/-)"]["number"],
            "protein": props["Protein (+/-)"]["number"],
            "fat": props["Fat (+/-)"]["number"],
            "carbs": props["Carbs (+/-)"]["number"],
            "fiber": props["Fiber (+/-)"]["number"],
        }

        if any(value is None for value in values.values()):
            continue

        count += 1

        for key in totals:
            totals[key] += values[key]

    if count == 0:
        raise Exception("No completed weeks found with +/- values.")

    averages = {key: totals[key] / count for key in totals}

    table = find_overall_table()
    rows = children(table["id"])

    avg_row = rows[2]
    new_cells = avg_difference_cells(averages)

    old_text = cell_text(avg_row["table_row"]["cells"])
    new_text = cell_text(new_cells)

    changed = old_text != new_text

    if changed:
        print("✅ Overall averages updated")
        log_cell_changes(
            ["Label", "Calories", "Protein", "Fat", "Carbs", "Fiber"],
            old_text,
            new_text,
        )
    else:
        print("✅ Overall averages unchanged")

    patch(
        f"/blocks/{avg_row['id']}",
        {"table_row": {"cells": new_cells}},
    )

    return {
        "success": True,
        "weeks_counted": count,
        "changed": changed,
        "averages": {key: fmt(value) for key, value in averages.items()},
    }