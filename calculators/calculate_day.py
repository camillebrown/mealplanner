import importlib

from config import SUMMARY_DATABASE_ID
from constants import GOALS, MEALS
from meal_plans.helpers import flatten_items
from notion import diff_color, get, patch, post, rt, cell_text, log_cell_changes

def fmt(value):
    value = round(value, 1)
    return int(value) if value == int(value) else value


def load_meal_plan(plan_name):
    module = importlib.import_module(f"meal_plans.{plan_name}")
    return module.MEAL_PLAN


def build_item(entry):
    ingredient = entry["ingredient"]
    serving = entry["serving"]

    return {
        "calories": ingredient["calories"] * serving,
        "protein": ingredient["protein"] * serving,
        "fat": ingredient["fat"] * serving,
        "carbs": ingredient["carbs"] * serving,
        "fiber": ingredient["fiber"] * serving,
    }


def children(block_id):
    return get(f"/blocks/{block_id}/children?page_size=100")["results"]


def find_week():
    data = post(
        f"/databases/{SUMMARY_DATABASE_ID}/query",
        {
            "sorts": [{"property": "Start", "direction": "descending"}],
            "filter": {"property": "Start", "date": {"is_not_empty": True}},
            "page_size": 1,
        },
    )
    return data["results"][0]


def first_cell_text(row):
    cell = row["table_row"]["cells"][0]
    return "".join(part.get("plain_text", "") for part in cell)


def total_cells(label, totals):
    return [
        rt(label, bold=True),
        rt(fmt(totals["calories"]), bold=True),
        rt(f'{fmt(totals["protein"])}g', bold=True),
        rt(f'{fmt(totals["fat"])}g', bold=True),
        rt(f'{fmt(totals["carbs"])}g', bold=True),
        rt(f'{fmt(totals["fiber"])}g', bold=True),
    ]


def diff_cells(totals):
    diffs = {
        "calories": totals["calories"] - GOALS["calories"],
        "protein": totals["protein"] - GOALS["protein"],
        "fat": totals["fat"] - GOALS["fat"],
        "carbs": totals["carbs"] - GOALS["carbs"],
        "fiber": totals["fiber"] - GOALS["fiber"],
    }

    def signed(value, suffix=""):
        value = fmt(value)
        sign = "+" if value > 0 else ""
        return f"{sign}{value}{suffix}"

    return [
        rt("Difference", bold=True),
        rt(signed(diffs["calories"]), bold=True, color=diff_color("calories", diffs["calories"])),
        rt(signed(diffs["protein"], " g"), bold=True, color=diff_color("protein", diffs["protein"])),
        rt(signed(diffs["fat"], " g"), bold=True, color=diff_color("fat", diffs["fat"])),
        rt(signed(diffs["carbs"], " g"), bold=True, color=diff_color("carbs", diffs["carbs"])),
        rt(signed(diffs["fiber"], " g"), bold=True, color=diff_color("fiber", diffs["fiber"])),
    ]


def calculate_day(plan_name, day):
    meal_plan = load_meal_plan(plan_name)
    page = find_week()

    totals = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0, "fiber": 0}

    for meal in MEALS:
        if meal not in meal_plan.get(day, {}):
            continue

        for entry in flatten_items(meal_plan[day][meal]["items"]):
            item = build_item(entry)
            for key in totals:
                totals[key] += item[key]

    page_blocks = children(page["id"])

    day_block = next(
        b for b in page_blocks
        if b["type"] == "heading_2"
        and b["heading_2"]["rich_text"][0]["plain_text"] == day
    )

    day_children = children(day_block["id"])
    tables = [b for b in day_children if b["type"] == "table"]
    totals_table = tables[-1]
    rows = children(totals_table["id"])

    new_total = total_cells("Total", totals)
    new_diff = diff_cells(totals)

    headers = ["Label", "Calories", "Protein", "Fat", "Carbs", "Fiber"]

    old_total = cell_text(rows[1]["table_row"]["cells"])
    new_total_text = cell_text(new_total)

    old_diff = cell_text(rows[2]["table_row"]["cells"])
    new_diff_text = cell_text(new_diff)

    total_changed = old_total != new_total_text
    diff_changed = old_diff != new_diff_text

    if total_changed or diff_changed:
        print(f"✅ {day} totals updated")
        log_cell_changes(headers, old_total, new_total_text)
        log_cell_changes(headers, old_diff, new_diff_text)
    else:
        print(f"✅ {day} totals unchanged")

    patch(
        f"/blocks/{rows[1]['id']}",
        {"table_row": {"cells": new_total}},
    )

    patch(
        f"/blocks/{rows[2]['id']}",
        {"table_row": {"cells": new_diff}},
    )

    print(
        f"✅ {day} totals "
        f"{'updated' if total_changed or diff_changed else 'unchanged'}"
    )

    return {
        "success": True,
        "day": day,
        "changed": total_changed or diff_changed,
        "totals": {key: fmt(value) for key, value in totals.items()},
    }