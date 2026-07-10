import inspect
import json
import subprocess
from fractions import Fraction

from config import RECIPE_DATABASE_ID
from notion import patch, post
from .. import recipes_list as recipe_library

DEFAULT_STATUS = "Keep"

NON_PLURAL_UNITS = {"g", "kg", "mg", "ml", "oz", "lb"}


def rt(text):
    return [{"type": "text", "text": {"content": str(text)}}]


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


def recipe_constants():
    recipes = []

    for name, value in inspect.getmembers(recipe_library):
        if not name.isupper():
            continue
        if not isinstance(value, dict):
            continue
        if "title" not in value or "items" not in value:
            continue

        recipes.append((name, value))

    return recipes


def find_recipe_page(title):
    data = post(
        f"/databases/{RECIPE_DATABASE_ID}/query",
        {
            "filter": {
                "property": "Recipe",
                "title": {
                    "equals": title,
                },
            },
            "page_size": 1,
        },
    )

    results = data.get("results", [])
    return results[0] if results else None


def recipe_properties(recipe):
    props = {
        "Recipe": {
            "title": [
                {"type": "text", "text": {"content": recipe["title"]}}
            ]
        },
        "Status": {
            "select": {"name": DEFAULT_STATUS}
        },
    }

    if recipe.get("recipe_link"):
        props["Recipe URL"] = {"url": recipe["recipe_link"]}

    return props


def recipe_body(recipe):
    ingredient_blocks = []

    for item in recipe["items"]:
        ingredient = item["ingredient"]
        serving = item["serving"]

        ingredient_blocks.append(
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": rt(
                        f"{ingredient['name']} — {serving_text(ingredient, serving)}"
                    )
                },
            }
        )

    return [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": rt("🍽 Overview")},
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": rt("")},
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": rt("📋 Ingredients")},
        },
        *ingredient_blocks,
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": rt("👩‍🍳 Instructions")},
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {"rich_text": rt("")},
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": rt("💡 Notes")},
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": rt("")},
        },
    ]


def create_recipe_page(recipe):
    return post(
        "/pages",
        {
            "parent": {"database_id": RECIPE_DATABASE_ID},
            "properties": recipe_properties(recipe),
            "children": recipe_body(recipe),
        },
    )


def update_recipe_page(page, recipe):
    return patch(
        f"/pages/{page['id']}",
        {
            "properties": recipe_properties(recipe),
        },
    )


def import_recipes():
    created = []
    updated = []

    for constant_name, recipe in recipe_constants():
        existing_page = find_recipe_page(recipe["title"])

        if existing_page:
            update_recipe_page(existing_page, recipe)
            updated.append(recipe["title"])
            print(f"✅ Updated recipe: {recipe['title']}")
        else:
            create_recipe_page(recipe)
            created.append(recipe["title"])
            print(f"✅ Created recipe: {recipe['title']}")

    return {
        "success": True,
        "created": created,
        "updated": updated,
        "created_count": len(created),
        "updated_count": len(updated),
    }


if __name__ == "__main__":
    result = import_recipes()

    pretty = json.dumps(result, indent=2)
    print(pretty)
    subprocess.run(["pbcopy"], input=pretty.encode())
    print("\n✅ Copied to clipboard")