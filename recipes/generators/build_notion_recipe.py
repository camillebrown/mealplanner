import inspect
import re
import json
from fractions import Fraction

import recipes.ingredients.index as ingredient_library

UNICODE_FRACTIONS = {
    "¼": "1/4",
    "½": "1/2",
    "¾": "3/4",
    "⅓": "1/3",
    "⅔": "2/3",
    "⅛": "1/8",
    "⅜": "3/8",
    "⅝": "5/8",
    "⅞": "7/8",
}

def normalize_quantity_text(value):
    text = normalize_fractions(value)
    text = str(text).lower()
    text = text.replace("_", " ")
    text = re.sub(r"[^a-z0-9/\.\s]+", " ", text)

    return re.sub(r"\s+", " ", text).strip()

def normalize_fractions(value):
    text = str(value)

    for symbol, fraction in UNICODE_FRACTIONS.items():
        text = text.replace(symbol, fraction)

    return text

def normalize_name(value):
    value = str(value).lower()
    value = value.replace("_", " ")
    value = re.sub(r"[^a-z0-9]+", " ", value)

    return re.sub(r"\s+", " ", value).strip()

def source_ingredient_name(source_text):
    normalized = normalize_name(source_text)

    normalized = re.sub(
        r"""^
        \d+(?:\.\d+)?          # 1 or 1.5
        (?:\s+\d+/\d+)?        # optional mixed fraction
        \s*
        """,
        "",
        normalized,
        flags=re.VERBOSE,
    )

    units = {
        "g",
        "kg",
        "mg",
        "ml",
        "l",
        "oz",
        "lb",
        "tsp",
        "tbsp",
        "cup",
        "cups",
        "pack",
        "packet",
        "tin",
        "can",
        "fillet",
        "fillets",
        "cube",
        "cubes",
    }

    words = normalized.split()

    if words and words[0] in units:
        words = words[1:]

    return " ".join(words)

def ingredient_constants():
    constants = []

    for constant_name, ingredient in inspect.getmembers(
        ingredient_library
    ):
        if not constant_name.isupper():
            continue

        if not isinstance(ingredient, dict):
            continue

        if "name" not in ingredient:
            continue

        if "serving_size" not in ingredient:
            continue

        names = [
            normalize_name(constant_name),
            normalize_name(ingredient["name"]),
        ]

        for alternative_name in ingredient.get(
            "alternative_names",
            [],
        ):
            names.append(
                normalize_name(alternative_name)
            )

        constants.append(
            {
                "constant_name": constant_name,
                "ingredient": ingredient,
                "names": names,
            }
        )

    return constants


def find_ingredient_matches(source_text):
    recipe_name = source_ingredient_name(source_text)

    if not recipe_name:
        return []

    matches = []

    for entry in ingredient_constants():
        ingredient = entry["ingredient"]

        possible_names = set()

        possible_names.update(
            name_variants(entry["constant_name"])
        )

        possible_names.update(
            name_variants(ingredient["name"])
        )

        for name in ingredient.get(
            "alternative_names",
            [],
        ):
            possible_names.update(
                name_variants(name)
            )

        matched_names = [
            name
            for name in possible_names
            if (
                name
                and (
                    recipe_name in name
                    or name in recipe_name
                )
            )
        ]

        if matched_names:
            best_name = max(
                matched_names,
                key=len,
            )

            matches.append(
                {
                    **entry,
                    "matched_name": best_name,
                }
            )

    matches.sort(
        key=lambda entry: len(
            entry["matched_name"]
        ),
        reverse=True,
    )

    return matches

UNIT_TO_BASE = {
    "tsp": ("volume", 1),
    "tbsp": ("volume", 3),
    "cup": ("volume", 48),
    "ml": ("volume_ml", 1),
    "l": ("volume_ml", 1000),
    "mg": ("weight_g", 0.001),
    "g": ("weight_g", 1),
    "kg": ("weight_g", 1000),
    "oz": ("weight_oz", 1),
    "lb": ("weight_oz", 16),
}

UNIT_ALIASES = {
    "teaspoon": "tsp",
    "teaspoons": "tsp",
    "tablespoon": "tbsp",
    "tablespoons": "tbsp",
    "gram": "g",
    "grams": "g",
    "kilogram": "kg",
    "kilograms": "kg",
    "milligram": "mg",
    "milligrams": "mg",
    "milliliter": "ml",
    "milliliters": "ml",
    "liter": "l",
    "liters": "l",
    "ounce": "oz",
    "ounces": "oz",
    "pound": "lb",
    "pounds": "lb",
    "cups": "cup",
    "fillets": "fillet",
    "carrots": "carrot",
    "cubes": "cube",
    "packs": "pack",
    "packets": "packet",
    "tins": "tin",
    "cans": "can",
}


def parse_amount(value):
    value = value.strip()

    if " " in value and "/" in value:
        whole, fraction = value.split(" ", 1)
        return float(whole) + float(Fraction(fraction))

    if "/" in value:
        return float(Fraction(value))

    return float(value)


def normalize_unit(unit):
    unit = normalize_name(unit)

    return UNIT_ALIASES.get(unit, unit)


def parse_amount_and_unit(text):
    normalized = normalize_quantity_text(text)

    match = re.match(
        r"^(?P<amount>\d+(?:\.\d+)?|\d+/\d+|\d+\s+\d+/\d+)\s*(?P<unit>[a-z]+)\b",
        normalized,
    )

    if not match:
        return None

    return {
        "amount": parse_amount(match.group("amount")),
        "unit": normalize_unit(match.group("unit")),
    }
    
def convert_amount(amount, from_unit, to_unit):
    if from_unit == to_unit:
        return amount

    from_info = UNIT_TO_BASE.get(from_unit)
    to_info = UNIT_TO_BASE.get(to_unit)

    if not from_info or not to_info:
        return None

    from_group, from_factor = from_info
    to_group, to_factor = to_info

    if from_group != to_group:
        return None

    base_amount = amount * from_factor

    return base_amount / to_factor

def classify_ingredient_names(
    source_lines,
    source_servings,
    target_servings=1,
):
    matched = []
    defined_unmatching_units = []
    undefined = []

    for source_text in source_lines:
        matches = find_ingredient_matches(source_text)

        if not matches:
            undefined.append(
                {
                    "source": source_text,
                }
            )
            continue

        best_match = matches[0]
        ingredient = best_match["ingredient"]

        source_quantity = parse_source_quantity(
            source_text,
            ingredient["serving_size"],
        )
        serving_quantity = parse_amount_and_unit(
            ingredient["serving_size"]
        )

        if not source_quantity or not serving_quantity:
            defined_unmatching_units.append(
                {
                    "source": source_text,
                    "ingredient": best_match["constant_name"],
                    "reason": "Could not parse amount and unit.",
                }
            )
            continue

        converted_amount = convert_amount(
            source_quantity["amount"],
            source_quantity["unit"],
            serving_quantity["unit"],
        )

        if converted_amount is None:
            defined_unmatching_units.append(
                {
                    "source": source_text,
                    "ingredient": best_match["constant_name"],
                    "recipe_unit": source_quantity["unit"],
                    "ingredient_unit": serving_quantity["unit"],
                    "reason": "Units could not be converted.",
                }
            )
            continue

        if not source_servings:
            defined_unmatching_units.append(
                {
                    "source": source_text,
                    "ingredient": best_match["constant_name"],
                    "reason": "Recipe serving count is missing.",
                }
            )
            continue

        serving_multiplier = (
            converted_amount
            / source_servings
            / serving_quantity["amount"]
        )

        matched.append(
            {
                "source": source_text,
                "item": {
                    "ingredient": best_match["constant_name"],
                    "serving": round(serving_multiplier, 3),
                },
            }
        )

    return {
        "matched": matched,
        "defined_unmatching_units": defined_unmatching_units,
        "undefined": undefined,
    }
    
def unit_variants(unit):
    normalized = normalize_unit(unit)

    variants = {normalized}

    if normalized.endswith("s"):
        variants.add(normalized[:-1])
    else:
        variants.add(f"{normalized}s")

    return variants

def parse_source_quantity(
    source_text,
    ingredient_serving_size,
):
    source = normalize_quantity_text(source_text)

    amount_match = re.match(
        r"""^
        (?P<amount>
            \d+\s+\d+/\d+
            |
            \d+/\d+
            |
            \d+(?:\.\d+)?
        )
        (?=\s|[a-z])
        """,
        source,
        re.VERBOSE,
    )

    if not amount_match:
        return None

    amount = parse_amount(
        amount_match.group("amount")
    )

    serving_quantity = parse_amount_and_unit(
        ingredient_serving_size
    )

    if not serving_quantity:
        return None

    serving_unit = serving_quantity["unit"]

    # First look for the ingredient's defined unit anywhere
    # in the source line, such as "2 cod fillets".
    for variant in unit_variants(serving_unit):
        if re.search(
            rf"(?:^|\s){re.escape(variant)}(?:\s|$)",
            source,
        ):
            return {
                "amount": amount,
                "unit": serving_unit,
            }

    # Otherwise read a measurement unit directly after the
    # amount, including forms such as "30g" and "200ml".
    remainder = source[
        amount_match.end():
    ].strip()

    unit_match = re.match(
        r"^(?P<unit>[a-z]+)\b",
        remainder,
    )

    if not unit_match:
        return {
            "amount": amount,
            "unit": None,
        }

    explicit_unit = normalize_unit(
        unit_match.group("unit")
    )

    known_units = {
        "tsp",
        "tbsp",
        "cup",
        "g",
        "kg",
        "mg",
        "ml",
        "l",
        "oz",
        "lb",
    }

    return {
        "amount": amount,
        "unit": (
            explicit_unit
            if explicit_unit in known_units
            else None
        ),
    }
    
def name_variants(value):
    normalized = normalize_name(value)
    variants = {normalized}

    words = normalized.split()

    if not words:
        return variants

    last_word = words[-1]

    if last_word.endswith("ies"):
        variants.add(
            " ".join(
                words[:-1] + [last_word[:-3] + "y"]
            )
        )

    elif last_word.endswith("s") and not last_word.endswith("ss"):
        variants.add(
            " ".join(
                words[:-1] + [last_word[:-1]]
            )
        )

    else:
        variants.add(
            " ".join(
                words[:-1] + [last_word + "s"]
            )
        )

    return variants

def empty_notion_object():
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
    return {
        "recipe": empty_notion_object(),
        "ingredients": {
            "matched": [],
            "defined_unmatching_units": [],
            "undefined": [],
        },
    }

def constant_name(title):
    value = re.sub(
        r"[^A-Za-z0-9]+",
        "_",
        title.upper(),
    )

    return value.strip("_") or "UNTITLED_RECIPE"


def python_string(value):
    return json.dumps(
        str(value),
        ensure_ascii=False,
    )


def format_serving(value):
    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    return str(value)


def render_import_report(report):
    recipe = report["recipe"]
    ingredients = report["ingredients"]

    name = constant_name(recipe["title"])

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
            "# REVIEW — ingredient found, but serving could not be calculated:"
        )

        for entry in unresolved:
            reason = entry.get("reason", "Review required.")

            lines.append(
                f"# - {entry['source']} "
                f"→ {entry['ingredient']} "
                f"({reason})"
            )

        lines.append("")

    undefined = ingredients["undefined"]

    if undefined:
        lines.append(
            "# REVIEW — ingredient not found in ingredients.py:"
        )

        for entry in undefined:
            lines.append(
                f"# - {entry['source']}"
            )

        lines.append("")

    return "\n".join(lines)




# from recipes.generators.helpers import (
#     classify_ingredient_names,
#     empty_recipe_output,
# )


# def build_notion_recipe(
#     recipe,
#     source,
#     recipe_link,
#     image_url="",
#     target_servings=1,
#     notes=None,
# ):
#     """
#     Builds the final recipe data from extracted recipe fields.

#     Args:
#         recipe: Extracted recipe fields.
#         source: Recipe source, such as "tiktok" or "website".
#         recipe_link: Original recipe URL.
#         image_url: Recipe image URL.
#         target_servings: Servings represented by the generated recipe.
#         notes: Optional notes to include.

#     Returns:
#         dict: Final recipe data and ingredient classifications.
#     """
#     source_servings = recipe.get("servings")

#     result = empty_recipe_output()

#     result["recipe"].update(
#         {
#             "title": recipe.get("title", ""),
#             "source": source,
#             "recipe_link": recipe_link,
#             "image_url": (
#                 image_url
#                 or recipe.get("image_url", "")
#             ),
#             "overview": recipe.get("overview", ""),
#             "prep_time": recipe.get("prep_time"),
#             "cook_time": recipe.get("cook_time"),
#             "servings": target_servings,
#             "instructions": recipe.get(
#                 "instructions",
#                 [],
#             ),
#             "notes": notes or [],
#         }
#     )

#     result["ingredients"] = classify_ingredient_names(
#         recipe.get("ingredients", []),
#         source_servings,
#         target_servings,
#     )

#     return result