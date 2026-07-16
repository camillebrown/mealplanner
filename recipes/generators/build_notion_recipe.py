from recipes.generators.helpers.ingredient_matching import (
    classify_ingredient_names,
)

from recipes.generators.helpers.transform_to_python import (
    title_to_python_constant,
    format_serving,
    python_string,
)

def empty_notion_object():
    """
    Creates an empty recipe object matching the Notion recipe schema.

    Returns:
        dict: Empty Notion-ready recipe fields.
    """
    return {
        "title": "",
        "category": "",
        "cuisine": "",
        "source": "",
        "restaurant": "",
        "recipe_link": "",
        "image_url": "",
        "prep_time": None,
        "cook_time": None,
        "servings": None,
        "tags": [],
        "overview": "",
        "instructions": [],
        "notes": [],
        "items": [],
    }


def empty_extracted_recipe_output():
    """
    Creates an empty imported-recipe report.

    Returns:
        dict: Empty recipe object and ingredient-classification groups.
    """
    return {
        "recipe": empty_notion_object(),
        "ingredients": {
            "matched": [],
            "defined_unmatching_units": [],
            "undefined": [],
        },
    }

def build_python_recipe_config(report):
    """
    Renders an imported-recipe report as paste-ready Python code.

    Unresolved ingredients are appended as review comments.

    Args:
        report: Imported-recipe report returned by build_notion_recipe().

    Returns:
        str: Paste-ready recipe constant and review checklist.
    """
    recipe = report["recipe"]
    ingredients = report["ingredients"]

    name = title_to_python_constant(recipe["title"])

    lines = [
        f"{name} = {{",
        f'    "title": {python_string(recipe["title"])},',
        f'    "category": {python_string(recipe["category"])},',
        f'    "cuisine": {python_string(recipe["cuisine"])},',
        f'    "source": {python_string(recipe["source"])},',
        f'    "restaurant": {python_string(recipe["restaurant"])},',
        f'    "recipe_link": {python_string(recipe["recipe_link"])},',
        f'    "image_url": {python_string(recipe["image_url"])},',
        f'    "prep_time": {repr(recipe["prep_time"])},',
        f'    "cook_time": {repr(recipe["cook_time"])},',
        f'    "servings": {repr(recipe["servings"])},',
        f'    "tags": {repr(recipe["tags"])},',
        f'    "overview": {python_string(recipe["overview"])},',
        '    "instructions": [',
    ]

    for instruction in recipe["instructions"]:
        lines.append(
            f"        {python_string(instruction)},"
        )

    lines.extend(
        [
            "    ],",
            '    "notes": [',
        ]
    )

    for note in recipe["notes"]:
        lines.append(
            f"        {python_string(note)},"
        )

    lines.extend(
        [
            "    ],",
            '    "items": [',
        ]
    )

    for match in ingredients["matched"]:
        item = match["item"]

        lines.append(
            "        "
            f'{{"ingredient": {item["ingredient"]}, '
            f'"serving": {format_serving(item["serving"])}'
            "},"
        )

    lines.extend(
        [
            "    ],",
            "}",
            "",
        ]
    )

    unresolved = ingredients[
        "defined_unmatching_units"
    ]

    if unresolved:
        lines.append(
            "# REVIEW — ingredient found, but serving "
            "could not be calculated:"
        )

        for entry in unresolved:
            reason = entry.get(
                "reason",
                "Review required.",
            )

            lines.append(
                f"# - {entry['source']} "
                f"→ {entry['ingredient']} "
                f"({reason})"
            )

        lines.append("")

    undefined = ingredients["undefined"]

    if undefined:
        lines.append(
            "# REVIEW — ingredient not found "
            "in ingredients.py:"
        )

        for entry in undefined:
            lines.append(
                f"# - {entry['source']}"
            )

        lines.append("")

    return "\n".join(lines)

def build_notion_recipe(
    recipe,
    source,
    recipe_link,
    image_url="",
    target_servings=1,
    notes=None,
):
    """
    Builds the final imported-recipe report from standardized recipe data.

    Args:
        recipe: Standardized parsed recipe fields.
        source: Recipe source, such as "tiktok" or "website".
        recipe_link: Original recipe URL.
        image_url: Source image URL.
        target_servings: Desired number of servings.
        notes: Optional notes for the generated recipe.

    Returns:
        str: Editable Python recipe draft and ingredient review notes.
    """
    source_servings = recipe.get("servings")

    result = empty_extracted_recipe_output()

    result["recipe"].update(
        {
            "title": recipe.get("title", ""),
            "source": source,
            "recipe_link": recipe_link,
            "image_url": (
                image_url
                or recipe.get("image_url", "")
            ),
            "overview": recipe.get("overview", ""),
            "prep_time": recipe.get("prep_time"),
            "cook_time": recipe.get("cook_time"),
            "servings": target_servings,
            "instructions": recipe.get(
                "instructions",
                [],
            ),
            "notes": notes or [],
        }
    )

    result["ingredients"] = classify_ingredient_names(
        recipe.get("ingredients", []),
        source_servings,
        target_servings,
    )

    return build_python_recipe_config(result)