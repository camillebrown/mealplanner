import importlib

from config import SUMMARY_DATABASE_ID
from constants import DAYS, GOALS, MEALS
from meal_plans.helpers import flatten_items
from notion import cell_text, diff_color, get, patch, post, rt, log_cell_changes


def fmt(value):
    value = round(value, 1)
    return int(value) if value == int(value) else value


def load_meal_plan(plan_name):
    module = importlib.import_module(f"meal_plans.{plan_name}")
    return module.MEAL_PLAN


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


def calculate_totals(meal_plan):
    totals = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0, "fiber": 0}
    day_count = 0

    for day in DAYS:
        if day not in meal_plan:
            continue

        day_count += 1

        for meal in MEALS:
            if meal not in meal_plan[day]:
                continue

            for entry in flatten_items(meal_plan[day][meal]["items"]):
                ingredient = entry["ingredient"]
                serving = entry["serving"]

                totals["calories"] += ingredient["calories"] * serving
                totals["protein"] += ingredient["protein"] * serving
                totals["fat"] += ingredient["fat"] * serving
                totals["carbs"] += ingredient["carbs"] * serving
                totals["fiber"] += ingredient["fiber"] * serving

    averages = {
        key: totals[key] / day_count if day_count else 0
        for key in totals
    }

    return totals, averages, day_count


def weekly_average_cells(averages, day_count):
    return [
        rt(f"Daily Average ({day_count} days)", bold=True),
        rt(fmt(averages["calories"]), bold=True),
        rt(f'{fmt(averages["protein"])}g', bold=True),
        rt(f'{fmt(averages["fat"])}g', bold=True),
        rt(f'{fmt(averages["carbs"])}g', bold=True),
        rt(f'{fmt(averages["fiber"])}g', bold=True),
    ]


def difference_cells(averages):
    diffs = {
        "calories": averages["calories"] - GOALS["calories"],
        "protein": averages["protein"] - GOALS["protein"],
        "fat": averages["fat"] - GOALS["fat"],
        "carbs": averages["carbs"] - GOALS["carbs"],
        "fiber": averages["fiber"] - GOALS["fiber"],
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


def calculate_week(plan_name):
    meal_plan = load_meal_plan(plan_name)
    page = find_week()
    totals, averages, day_count = calculate_totals(meal_plan)

    page_blocks = children(page["id"])
    weekly_table = None

    for block in page_blocks:
        if block["type"] == "table":
            weekly_table = block

    avg_changed = False
    diff_changed = False
    
    if weekly_table:
        rows = children(weekly_table["id"])

        if len(rows) >= 3:
            avg_cells = weekly_average_cells(averages, day_count)
            diff_cells_result = difference_cells(averages)
            
            headers = ["Label", "Calories", "Protein", "Fat", "Carbs", "Fiber"]

            old_avg = cell_text(rows[1]["table_row"]["cells"])
            new_avg = cell_text(avg_cells)

            old_diff = cell_text(rows[2]["table_row"]["cells"])
            new_diff = cell_text(diff_cells_result)

            avg_changed = old_avg != new_avg
            diff_changed = old_diff != new_diff

            if avg_changed or diff_changed:
                print("✅ Weekly summary updated")
                log_cell_changes(headers, old_avg, new_avg)
                log_cell_changes(headers, old_diff, new_diff)
            else:
                print("✅ Weekly summary unchanged")

            patch(
                f"/blocks/{rows[1]['id']}",
                {"table_row": {"cells": avg_cells}},
            )

            patch(
                f"/blocks/{rows[2]['id']}",
                {"table_row": {"cells": diff_cells_result}},
            )

            print(
                "✅ Weekly averages "
                + ("updated" if avg_changed or diff_changed else "unchanged")
            )

    patch(
        f"/pages/{page['id']}",
        {
            "properties": {
                "Calories (+/-)": {"number": fmt(averages["calories"] - GOALS["calories"])},
                "Protein (+/-)": {"number": fmt(averages["protein"] - GOALS["protein"])},
                "Fat (+/-)": {"number": fmt(averages["fat"] - GOALS["fat"])},
                "Carbs (+/-)": {"number": fmt(averages["carbs"] - GOALS["carbs"])},
                "Fiber (+/-)": {"number": fmt(averages["fiber"] - GOALS["fiber"])},
            }
        },
    )

    return {
        "success": True,
        "days_counted": day_count,
        "totals": {k: fmt(v) for k, v in totals.items()},
        "averages": {k: fmt(v) for k, v in averages.items()},
    }