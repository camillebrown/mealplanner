import re
from fractions import Fraction

from recipes.generators.helpers.formatters import (
    normalize_quantity_text,
    normalize_unit,
    unit_variants,
)
from recipes.generators.constants import (
    KNOWN_EXPLICIT_UNITS,
    UNIT_TO_BASE,
)

def parse_amount(value):
    """
    Converts a whole number, fraction, or mixed fraction to a float.

    Args:
        value: Numeric text such as "2", "1/2", or "1 1/2".

    Returns:
        float: Parsed numeric amount.
    """
    value = value.strip()

    if " " in value and "/" in value:
        whole, fraction = value.split(" ", 1)

        return (
            float(whole)
            + float(Fraction(fraction))
        )

    if "/" in value:
        return float(Fraction(value))

    return float(value)


def parse_amount_and_unit(text):
    """
    Extracts an amount and unit from the beginning of text.

    Args:
        text: Quantity text such as "30 g" or "1 cup".

    Returns:
        dict | None: Parsed amount and normalized unit, or None when
        the text does not begin with both an amount and unit.
    """
    normalized = normalize_quantity_text(text)

    match = re.match(
        (
            r"^(?P<amount>"
            r"\d+(?:\.\d+)?"
            r"|\d+/\d+"
            r"|\d+\s+\d+/\d+"
            r")"
            r"\s*"
            r"(?P<unit>[a-z]+)\b"
        ),
        normalized,
    )

    if not match:
        return None

    return {
        "amount": parse_amount(
            match.group("amount")
        ),
        "unit": normalize_unit(
            match.group("unit")
        ),
    }


def convert_amount(
    amount,
    from_unit,
    to_unit,
):
    """
    Converts an amount between compatible measurement units.

    Args:
        amount: Numeric amount to convert.
        from_unit: Current normalized unit.
        to_unit: Desired normalized unit.

    Returns:
        float | None: Converted amount, or None when the units are
        unknown or belong to incompatible measurement groups.
    """
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


def parse_source_quantity(
    source_text,
    ingredient_serving_size,
):
    """
    Extracts a quantity from an imported ingredient line.

    The ingredient's defined serving unit is preferred when that unit
    appears anywhere in the source line. Otherwise, the function reads
    an explicit measurement unit directly following the amount.

    Args:
        source_text: Imported ingredient line.
        ingredient_serving_size: Serving size from the matched
            ingredient definition.

    Returns:
        dict | None: Parsed amount and unit, or None when the amount or
        ingredient serving size cannot be parsed.
    """
    source = normalize_quantity_text(
        source_text
    )

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

    for variant in unit_variants(
        serving_unit
    ):
        if re.search(
            (
                rf"(?:^|\s)"
                rf"{re.escape(variant)}"
                rf"(?:\s|$)"
            ),
            source,
        ):
            return {
                "amount": amount,
                "unit": serving_unit,
            }

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

    return {
        "amount": amount,
        "unit": (
            explicit_unit
            if explicit_unit
            in KNOWN_EXPLICIT_UNITS
            else None
        ),
    }