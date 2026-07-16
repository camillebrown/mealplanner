import inspect
import re

import recipes.ingredients.index as ingredient_library

from recipes.generators.helpers.formatters import (
    name_variants,
    normalize_name,
)
from recipes.generators.helpers.quantity_parsers import (
    convert_amount,
    parse_amount_and_unit,
    parse_source_quantity,
)

from recipes.generators.constants import SOURCE_UNITS

def source_ingredient_name(source_text):
    """
    Extracts the likely ingredient name from an imported source line.

    Leading quantities and recognized units are removed before matching.

    Args:
        source_text: Imported ingredient line.

    Returns:
        str: Normalized ingredient name used for library matching.
    """
    normalized = normalize_name(source_text)

    normalized = re.sub(
        r"""^
        \d+(?:\.\d+)?
        (?:\s+\d+/\d+)?
        \s*
        """,
        "",
        normalized,
        flags=re.VERBOSE,
    )

    words = normalized.split()

    if words and words[0] in SOURCE_UNITS:
        words = words[1:]

    return " ".join(words)


def ingredient_constants():
    """
    Collects valid ingredient constants from the ingredient index.

    A valid ingredient constant must be uppercase, contain a dictionary,
    and define both a name and serving size.

    Returns:
        list[dict]: Ingredient constants and their normalized names.
    """
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
    """
    Finds ingredient definitions matching an imported source line.

    Matches are ordered by the length of the matched name so that the
    most specific matching ingredient is returned first.

    Args:
        source_text: Imported ingredient line.

    Returns:
        list[dict]: Matching ingredient definitions ordered from most
        specific to least specific.
    """
    recipe_name = source_ingredient_name(
        source_text
    )

    if not recipe_name:
        return []

    matches = []

    for entry in ingredient_constants():
        ingredient = entry["ingredient"]
        possible_names = set()

        possible_names.update(
            name_variants(
                entry["constant_name"]
            )
        )

        possible_names.update(
            name_variants(
                ingredient["name"]
            )
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

        if not matched_names:
            continue

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


def classify_ingredient_names(
    source_lines,
    source_servings,
    target_servings=1,
):
    """
    Matches imported ingredient lines and calculates serving multipliers.

    Ingredients are separated into matched ingredients, known ingredients
    whose units cannot be converted, and undefined ingredients.

    Args:
        source_lines: Imported ingredient lines.
        source_servings: Number of servings represented by the source
            recipe.
        target_servings: Desired number of servings for the generated
            recipe.

    Returns:
        dict: Matched, unit-mismatched, and undefined ingredients.
    """
    matched = []
    defined_unmatching_units = []
    undefined = []

    for source_text in source_lines:
        matches = find_ingredient_matches(
            source_text
        )

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

        if (
            not source_quantity
            or not serving_quantity
        ):
            defined_unmatching_units.append(
                {
                    "source": source_text,
                    "ingredient": best_match[
                        "constant_name"
                    ],
                    "reason": (
                        "Could not parse amount "
                        "and unit."
                    ),
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
                    "ingredient": best_match[
                        "constant_name"
                    ],
                    "recipe_unit": source_quantity[
                        "unit"
                    ],
                    "ingredient_unit": serving_quantity[
                        "unit"
                    ],
                    "reason": (
                        "Units could not be "
                        "converted."
                    ),
                }
            )
            continue

        if not source_servings:
            defined_unmatching_units.append(
                {
                    "source": source_text,
                    "ingredient": best_match[
                        "constant_name"
                    ],
                    "reason": (
                        "Recipe serving count "
                        "is missing."
                    ),
                }
            )
            continue

        serving_multiplier = (
            converted_amount
            / source_servings
            * target_servings
            / serving_quantity["amount"]
        )

        matched.append(
            {
                "source": source_text,
                "item": {
                    "ingredient": best_match[
                        "constant_name"
                    ],
                    "serving": round(
                        serving_multiplier,
                        3,
                    ),
                },
            }
        )

    return {
        "matched": matched,
        "defined_unmatching_units": (
            defined_unmatching_units
        ),
        "undefined": undefined,
    }