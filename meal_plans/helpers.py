def is_recipe(value):
    return (
        isinstance(value, dict)
        and "title" in value
        and "items" in value
    )


def is_ingredient_entry(value):
    return (
        isinstance(value, dict)
        and "ingredient" in value
        and "serving" in value
    )


def flatten_items(items):
    flattened = []

    for item in items:
        if is_recipe(item):
            flattened.extend(flatten_items(item["items"]))
        elif is_ingredient_entry(item):
            flattened.append(item)
        else:
            raise ValueError(
                f"Unsupported meal item structure: {item}"
            )

    return flattened


def recipe_titles(items):
    titles = []

    for item in items:
        if is_recipe(item):
            titles.append(item["title"])
            titles.extend(recipe_titles(item["items"]))

    return titles