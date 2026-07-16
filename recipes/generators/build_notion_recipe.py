from recipes.generators.helpers import (
    classify_ingredient_names,
    empty_recipe_output,
)


def build_notion_recipe(
    recipe,
    source,
    recipe_link,
    image_url="",
    target_servings=1,
    notes=None,
):
    """
    Builds the final recipe data from extracted recipe fields.

    Args:
        recipe: Extracted recipe fields.
        source: Recipe source, such as "tiktok" or "website".
        recipe_link: Original recipe URL.
        image_url: Recipe image URL.
        target_servings: Servings represented by the generated recipe.
        notes: Optional notes to include.

    Returns:
        dict: Final recipe data and ingredient classifications.
    """
    source_servings = recipe.get("servings")

    result = empty_recipe_output()

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

    return result