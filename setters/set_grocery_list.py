import importlib
from collections import defaultdict
from fractions import Fraction

from config import SUMMARY_DATABASE_ID
from notion import get, patch, post, rt

CATEGORIES = [
    "proteins",
    "dairy",
    "frozen products",
    "grains & starches",
    "produce",
    "pantry, canned goods & condiments",
]

NON_PLURAL_UNITS = {"g", "kg", "mg", "ml", "oz", "lb"}


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


def parse_serving_size(serving_size):
    amount, unit = serving_size.split(" ", 1)
    return float(Fraction(amount)), unit


def pluralize(unit, amount):
    if unit in NON_PLURAL_UNITS:
        return unit
    if amount == 1:
        return unit
    if unit.endswith("s"):
        return unit
    return f"{unit}s"


def quantity_text(amount, unit):
    amount = fmt(amount)
    return f"{amount} {pluralize(unit, amount)}"


def row(item, quantity):
    return {
        "object": "block",
        "type": "table_row",
        "table_row": {
            "cells": [
                rt(item),
                rt(quantity),
            ]
        },
    }


def empty_row():
    return {
        "table_row": {
            "cells": [
                rt(""),
                rt(""),
            ]
        }
    }


def build_grocery_items(plan_name):
    meal_plan = load_meal_plan(plan_name)

    groceries = defaultdict(dict)

    for day_data in meal_plan.values():
        for meal_data in day_data.values():
            for entry in meal_data["items"]:
                ingredient = entry["ingredient"]

                if "restaurant" in ingredient:
                    continue

                category = ingredient.get("category", "Uncategorized")
                name = ingredient["name"]
                serving = entry["serving"]

                base_amount, unit = parse_serving_size(ingredient["serving_size"])
                total_amount = base_amount * serving

                if name not in groceries[category]:
                    groceries[category][name] = {
                        "amount": 0,
                        "unit": unit,
                    }

                groceries[category][name]["amount"] += total_amount

    return groceries


def normalize_category(text):
    return text.split(" ", 1)[1].strip().lower()


def find_grocery_tables(page):
    page_blocks = children(page["id"])

    grocery_heading = next(
        (
            block
            for block in page_blocks
            if block["type"] == "heading_2"
            and block["heading_2"]["rich_text"]
            and "Grocery List" in block["heading_2"]["rich_text"][0]["plain_text"]
        ),
        None,
    )

    if grocery_heading is None:
        raise Exception(f"Grocery List heading not found on page: {page['url']}")

    grocery_children = children(grocery_heading["id"])

    tables = {}
    current_category = None

    for block in grocery_children:
        if block["type"] == "heading_4":
            text = block["heading_4"]["rich_text"][0]["plain_text"]
            current_category = normalize_category(text)

        elif block["type"] == "table" and current_category:
            tables[current_category] = block
            current_category = None

    return tables


def fill_table(table_id, items):
    existing_rows = children(table_id)

    if not existing_rows:
        raise Exception(f"Grocery table {table_id} has no header row.")

    # Preserve first/header row and only edit rows underneath it.
    item_rows = existing_rows[1:]

    new_rows = [
        row(name, quantity_text(data["amount"], data["unit"]))
        for name, data in sorted(items.items())
    ]

    for existing, new_row in zip(item_rows, new_rows):
        patch(f"/blocks/{existing['id']}", {"table_row": new_row["table_row"]})

    if len(new_rows) > len(item_rows):
        patch(
            f"/blocks/{table_id}/children",
            {"children": new_rows[len(item_rows):]},
        )

    if len(item_rows) > len(new_rows):
        for extra in item_rows[len(new_rows):]:
            patch(f"/blocks/{extra['id']}", {"archived": True})

    return len(new_rows)


def update_grocery_list(plan_name):
    page = find_week()
    groceries = build_grocery_items(plan_name)
    tables = find_grocery_tables(page)

    updated = {}
    missing_categories = []

    for category, items in sorted(groceries.items()):
        if category not in tables:
            missing_categories.append(category)
            continue

        count = fill_table(tables[category]["id"], items)
        updated[category] = count
        print(f"✅ Grocery {category}: {count} item(s)")

    if missing_categories:
        print("⚠️ Missing grocery category table(s):")
        for category in sorted(missing_categories):
            print(f" - {category}")

    return {
        "success": True,
        "plan": plan_name,
        "updated": updated,
        "missing_categories": missing_categories,
        "url": page["url"],
    }