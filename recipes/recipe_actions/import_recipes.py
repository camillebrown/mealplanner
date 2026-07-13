import inspect
import json
import subprocess
import sys
from fractions import Fraction

from config import RECIPE_DATABASE_ID
from notion import get, patch, post
from .. import recipes_list as recipe_library

DEFAULT_STATUS = "Want to Try"

NON_PLURAL_UNITS = {"g", "kg", "mg", "ml", "oz", "lb"}


def rt(text):
    return [{"type": "text", "text": {"content": str(text)}}]


def fmt(value):
    value = round(value, 1)
    return int(value) if value == int(value) else value

def option_name(value):
    return " ".join(word.capitalize() for word in value.split())


def select_value(value):
    if not value:
        return {"select": None}

    return {
        "select": {
            "name": option_name(value)
        }
    }
    
def children(block_id):
    data = get(f"/blocks/{block_id}/children?page_size=100")

    if not data:
        raise Exception(f"Could not load children for block: {block_id}")

    return data.get("results", [])

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


def get_all_notion_recipe_titles():
    data = post(
        f"/databases/{RECIPE_DATABASE_ID}/query",
        {
            "page_size": 100,
        },
    )

    titles = []

    for page in data.get("results", []):
        title_parts = page["properties"]["Recipe"]["title"]
        title = "".join(part.get("plain_text", "") for part in title_parts)

        if title:
            titles.append(title)

    return titles

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



def recipe_properties(recipe, include_status=False):
    props = {
        "Recipe": {
            "title": [
                {
                    "type": "text",
                    "text": {"content": recipe["title"]},
                }
            ]
        },
        "Category": select_value(recipe.get("category", "")),
        "Cuisine": select_value(recipe.get("cuisine", "")),
        "Source": select_value(recipe.get("source", "")),
        "Restaurant": {
            "rich_text": rt(recipe.get("restaurant", "")),
        },
        "Recipe URL": {
            "url": recipe.get("recipe_link") or None,
        },
        "Prep Time": {
            "number": recipe.get("prep_time"),
        },
        "Cook Time": {
            "number": recipe.get("cook_time"),
        },
        "Servings": {
            "number": recipe.get("servings"),
        },
        "Tags": {
            "multi_select": [
                {"name": option_name(tag)}
                for tag in recipe.get("tags", [])
            ]
        },
    }

    image_url = recipe.get("image_url")

    props["Image"] = {
        "files": (
            [
                {
                    "name": f"{recipe['title']} image",
                    "type": "external",
                    "external": {"url": image_url},
                }
            ]
            if image_url
            else []
        )
    }

    if include_status:
        props["Status"] = {
            "select": {"name": DEFAULT_STATUS}
        }

    return props


def recipe_body(recipe):
    blocks = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": rt("🍽 Overview")},
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": rt(recipe.get("overview", ""))
            },
        },
        {
            "object": "block",
            "type": "divider",
            "divider": {},
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": rt("📋 Ingredients")},
        },
    ]

    for item in recipe.get("items", []):
        ingredient = item["ingredient"]
        serving = item["serving"]

        blocks.append(
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": rt(
                        f"{serving_text(ingredient, serving)} "
                        f"{ingredient['name'].lower()}"
                    )
                },
            }
        )

    blocks.extend(
        [
            {
                "object": "block",
                "type": "divider",
                "divider": {},
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": rt("👩‍🍳 Instructions")},
            },
        ]
    )

    instructions = recipe.get("instructions", [])

    if instructions:
        for instruction in instructions:
            blocks.append(
                {
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": rt(instruction)
                    },
                }
            )
    else:
        blocks.append(
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": rt("")},
            }
        )

    blocks.extend(
        [
            {
                "object": "block",
                "type": "divider",
                "divider": {},
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": rt("💡 Notes")},
            },
        ]
    )

    notes = recipe.get("notes", [])

    if notes:
        for note in notes:
            blocks.append(
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": rt(note)
                    },
                }
            )
    else:
        blocks.append(
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": rt("")},
            }
        )

    return blocks


def create_recipe_page(recipe):
    page_data = {
        "parent": {"database_id": RECIPE_DATABASE_ID},
        "properties": recipe_properties(
            recipe,
            include_status=True,
        ),
        "children": recipe_body(recipe),
    }

    image_url = recipe.get("image_url")

    if image_url:
        page_data["cover"] = {
            "type": "external",
            "external": {
                "url": image_url,
            },
        }

    return post("/pages", page_data)


def replace_recipe_body(page_id, recipe):
    data = get(f"/blocks/{page_id}/children?page_size=100")

    if not data or data.get("object") == "error":
        raise Exception(
            f"Failed to load recipe page body for {page_id}: {data}"
        )

    for block in data.get("results", []):
        result = patch(
            f"/blocks/{block['id']}",
            {
                "archived": True,
            },
        )

        if not result or result.get("object") == "error":
            raise Exception(
                f"Failed to archive block "
                f"{block['id']} ({block['type']}): {result}"
            )

    new_blocks = recipe_body(recipe)

    if new_blocks:
        result = patch(
            f"/blocks/{page_id}/children",
            {
                "children": new_blocks,
            },
        )

        if not result or result.get("object") == "error":
            raise Exception(
                f"Failed to append recipe body to page "
                f"{page_id}: {result}"
            )

def update_recipe_page(page, recipe):
    page_data = {
        "properties": recipe_properties(
            recipe,
            include_status=False,
        ),
    }

    image_url = recipe.get("image_url")

    if image_url:
        page_data["cover"] = {
            "type": "external",
            "external": {
                "url": image_url,
            },
        }

    updated_page = patch(
        f"/pages/{page['id']}",
        page_data,
    )

    replace_recipe_body(page["id"], recipe)

    return updated_page


def import_recipes(recipe_name=None):
    created = []
    updated = []

    for constant_name, recipe in recipe_constants():
        if recipe_name and constant_name != recipe_name:
            continue
    
        existing_page = find_recipe_page(recipe["title"])

        if existing_page:
            update_recipe_page(existing_page, recipe)
            updated.append(recipe["title"])
            print(f"✅ Updated recipe: {recipe['title']}")
        else:
            create_recipe_page(recipe)
            created.append(recipe["title"])
            print(f"✅ Created recipe: {recipe['title']}")

    if recipe_name and not created and not updated:
        raise ValueError(f"Recipe '{recipe_name}' not found.")
    
    
    python_titles = {
        recipe["title"]
        for _, recipe in recipe_constants()
    }

    notion_titles = set(get_all_notion_recipe_titles())

    not_defined = sorted(notion_titles - python_titles)

    if not_defined:
        print("\n⚠️ Not defined in recipes.py:")
        for title in not_defined:
            print(f"  • {title}")
    else:
        print("\n✅ Every Notion recipe is defined in recipes.py")

    return {
        "success": True,
        "created": created,
        "updated": updated,
        "created_count": len(created),
        "updated_count": len(updated),
        "not_defined_in_python": not_defined,
    }


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage:")
        print("python3 -m recipes.recipe_actions.import_recipes")
        print("python3 -m recipes.recipe_actions.import_recipes COTTAGE_CHEESE_BREAKFAST_TACOS")
        sys.exit(1)

    recipe_name = sys.argv[1] if len(sys.argv) == 2 else None

    result = import_recipes(recipe_name)

    pretty = json.dumps(result, indent=2)
    print(pretty)
    subprocess.run(["pbcopy"], input=pretty.encode())
    print("\n✅ Copied to clipboard")