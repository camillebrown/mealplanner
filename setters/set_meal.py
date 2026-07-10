import json
import subprocess
import sys
import importlib
from fractions import Fraction

from calculators.calculate_day import calculate_day
from config import SUMMARY_DATABASE_ID
from constants import ICONS, MEALS
from notion import cell_text, get, patch, post

NON_PLURAL_UNITS = {"g", "kg", "mg", "ml", "oz", "lb"}


def load_meal_plan(plan_name):
    module = importlib.import_module(f"meal_plans.{plan_name}")
    return module.MEAL_PLAN


def rt(text, bold=False):
    return [
        {
            "type": "text",
            "text": {"content": str(text)},
            "annotations": {"bold": bold},
        }
    ]


def fmt(value):
    value = round(value, 1)
    return int(value) if value == int(value) else value


def serving_text(ingredient, serving):
    amount, unit = ingredient["serving_size"].split(" ", 1)
    total = fmt(float(Fraction(amount)) * serving)

    if unit in NON_PLURAL_UNITS:
        return f"{total} {unit}"
    if total == 1:
        return f"{total} {unit}"
    if unit.endswith("s"):
        return f"{total} {unit}"
    return f"{total} {unit}s"


def cells_for_item(item, bold_all=False):
    return [
        rt(item["name"], bold=bold_all),
        rt(item["serving_text"], bold=bold_all),
        rt(item["calories"], bold=bold_all),
        rt(item["protein"], bold=bold_all),
        rt(item["fat"], bold=bold_all),
        rt(item["carbs"], bold=bold_all),
        rt(item["fiber"], bold=bold_all),
    ]


def empty_cells():
    return [rt(""), rt(""), rt(""), rt(""), rt(""), rt(""), rt("")]


def first_cell_text(row):
    cell = row["table_row"]["cells"][0]
    return "".join(part.get("plain_text", "") for part in cell)


def build_item(entry):
    ingredient = entry["ingredient"]
    serving = entry["serving"]

    return {
        "name": ingredient["name"],
        "serving_text": serving_text(ingredient, serving),
        "calories": fmt(ingredient["calories"] * serving),
        "protein": fmt(ingredient["protein"] * serving),
        "fat": fmt(ingredient["fat"] * serving),
        "carbs": fmt(ingredient["carbs"] * serving),
        "fiber": fmt(ingredient["fiber"] * serving),
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

    if not data.get("results"):
        raise Exception("No week found with a Start date.")

    return data["results"][0]


def get_day_blocks(page, day):
    page_blocks = children(page["id"])

    day_block = next(
        (
            b for b in page_blocks
            if b["type"] == "heading_2"
            and b["heading_2"]["rich_text"]
            and b["heading_2"]["rich_text"][0]["plain_text"] == day
        ),
        None,
    )

    if day_block is None:
        raise Exception(f"Could not find '{day}' heading on page: {page['url']}")

    day_children = children(day_block["id"])
    return day_children


def update_meal_heading(meal_heading, meal, title=None, recipe_link=None):
    if title:
        heading_text = [
            {"type": "text", "text": {"content": f"{ICONS[meal]} "}},
            {
                "type": "text",
                "text": {"content": f"{meal} — {title}"},
                "annotations": {"bold": True},
            },
        ]

        if recipe_link:
            heading_text[1]["text"]["link"] = {"url": recipe_link}
    else:
        heading_text = [
            {"type": "text", "text": {"content": f"{ICONS[meal]} "}},
            {
                "type": "text",
                "text": {"content": meal},
                "annotations": {"bold": True},
            },
        ]

    patch(
        f"/blocks/{meal_heading['id']}",
        {
            "paragraph": {
                "rich_text": heading_text,
                "color": "default",
            }
        },
    )


def set_meal(plan_name, day, meal):
    meal_plan = load_meal_plan(plan_name)
    page = find_week()
    day_children = get_day_blocks(page, day)

    meal_index = MEALS.index(meal)
    paragraphs = [b for b in day_children if b["type"] == "paragraph"]
    tables = [b for b in day_children if b["type"] == "table"]

    meal_heading = paragraphs[meal_index]
    meal_table = tables[meal_index]
    meal_data = meal_plan[day][meal]

    update_meal_heading(
        meal_heading,
        meal,
        title=meal_data["title"],
        recipe_link=meal_data.get("recipe_link"),
    )

    rows = children(meal_table["id"])

    total_index = next(
        i for i, row in enumerate(rows)
        if "TOTAL" in first_cell_text(row).upper()
    )

    ingredient_slots = rows[1:total_index]
    items = [build_item(entry) for entry in meal_data["items"]]

    if len(items) > len(ingredient_slots):
        raise Exception(
            f"Not enough blank rows. Need {len(items)}, found {len(ingredient_slots)}."
        )

    meal_changed = False

    for slot, item in zip(ingredient_slots, items):
        new_cells = cells_for_item(item)
        if cell_text(slot["table_row"]["cells"]) != cell_text(new_cells):
            meal_changed = True

        patch(f"/blocks/{slot['id']}", {"table_row": {"cells": new_cells}})

    for slot in ingredient_slots[len(items):]:
        if any(cell_text(slot["table_row"]["cells"])):
            meal_changed = True

        patch(f"/blocks/{slot['id']}", {"table_row": {"cells": empty_cells()}})
        patch(f"/blocks/{slot['id']}", {"archived": True})

    total = {
        "name": f"{meal.upper()} TOTAL",
        "serving_text": "",
        "calories": fmt(sum(i["calories"] for i in items)),
        "protein": fmt(sum(i["protein"] for i in items)),
        "fat": fmt(sum(i["fat"] for i in items)),
        "carbs": fmt(sum(i["carbs"] for i in items)),
        "fiber": fmt(sum(i["fiber"] for i in items)),
    }

    total_row = rows[total_index]
    new_total_cells = cells_for_item(total, bold_all=True)

    if cell_text(total_row["table_row"]["cells"]) != cell_text(new_total_cells):
        meal_changed = True

    patch(
        f"/blocks/{total_row['id']}",
        {"table_row": {"cells": new_total_cells}},
    )

    day_totals = calculate_day(plan_name, day)

    print(f"✅ {day} {meal} {'updated' if meal_changed else 'unchanged'}")

    return {
        "success": True,
        "week": page["properties"]["Week"]["title"][0]["plain_text"],
        "day": day,
        "meal": meal,
        "changed": meal_changed,
        "rows_filled": len(items),
        "blank_rows_available": len(ingredient_slots),
        "total": total,
        "url": page["url"],
        "day_totals": day_totals,
    }


def clear_meal(plan_name, day, meal):
    page = find_week()
    day_children = get_day_blocks(page, day)

    meal_index = MEALS.index(meal)
    paragraphs = [b for b in day_children if b["type"] == "paragraph"]
    tables = [b for b in day_children if b["type"] == "table"]

    meal_heading = paragraphs[meal_index]
    meal_table = tables[meal_index]

    update_meal_heading(meal_heading, meal)

    rows = children(meal_table["id"])

    total_index = next(
        i for i, row in enumerate(rows)
        if "TOTAL" in first_cell_text(row).upper()
    )

    ingredient_slots = rows[1:total_index]
    changed = False

    for slot in ingredient_slots:
        if any(cell_text(slot["table_row"]["cells"])):
            changed = True

        patch(f"/blocks/{slot['id']}", {"table_row": {"cells": empty_cells()}})
        patch(f"/blocks/{slot['id']}", {"archived": True})

    empty_total = {
        "name": f"{meal.upper()} TOTAL",
        "serving_text": "",
        "calories": 0,
        "protein": 0,
        "fat": 0,
        "carbs": 0,
        "fiber": 0,
    }

    total_row = rows[total_index]
    new_cells = cells_for_item(empty_total, bold_all=True)

    if cell_text(total_row["table_row"]["cells"]) != cell_text(new_cells):
        changed = True

    patch(
        f"/blocks/{total_row['id']}",
        {"table_row": {"cells": new_cells}},
    )

    print(f"✅ {day} {meal} {'updated' if changed else 'unchanged'}")

    return {
        "success": True,
        "day": day,
        "meal": meal,
        "changed": changed,
        "cleared": True,
    }


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 -m setters.set_meal july_13_2026 Monday Breakfast")
        sys.exit(1)

    result = set_meal(sys.argv[1], sys.argv[2], sys.argv[3])

    pretty = json.dumps(result, indent=2)
    print(pretty)
    subprocess.run(["pbcopy"], input=pretty.encode())
    print("\n✅ Copied to clipboard")