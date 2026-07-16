import re

from recipes.generators.constants import (
    UNICODE_FRACTIONS,
    UNIT_ALIASES
)

def normalize_fractions(value):
    """
    Converts Unicode fraction characters into ASCII fractions.

    Args:
        value: Text or value that may contain Unicode fractions.

    Returns:
        str: Text containing ASCII fraction representations.
    """
    text = str(value)

    for symbol, fraction in UNICODE_FRACTIONS.items():
        text = text.replace(symbol, fraction)

    return text


def normalize_quantity_text(value):
    """
    Normalizes text used for parsing ingredient quantities.

    Unicode fractions are converted, text is lowercased, underscores
    are replaced with spaces, and unsupported characters are removed.

    Args:
        value: Ingredient quantity or serving-size text.

    Returns:
        str: Normalized quantity text.
    """
    text = normalize_fractions(value)
    text = text.lower()
    text = text.replace("_", " ")
    text = re.sub(
        r"[^a-z0-9/\.\s]+",
        " ",
        text,
    )

    return re.sub(
        r"\s+",
        " ",
        text,
    ).strip()


def normalize_name(value):
    """
    Normalizes an ingredient name for comparison.

    Args:
        value: Ingredient name, constant name, or source text.

    Returns:
        str: Lowercase, space-separated ingredient name.
    """
    text = str(value).lower()
    text = text.replace("_", " ")
    text = re.sub(
        r"[^a-z0-9]+",
        " ",
        text,
    )

    return re.sub(
        r"\s+",
        " ",
        text,
    ).strip()


def name_variants(value):
    """
    Produces basic singular and plural variants of a name.

    Args:
        value: Ingredient name to normalize and vary.

    Returns:
        set[str]: Normalized singular and plural name variants.
    """
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
    elif (
        last_word.endswith("s")
        and not last_word.endswith("ss")
    ):
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


def normalize_unit(unit):
    """
    Converts a unit name into its canonical abbreviated form.

    Args:
        unit: Unit name or abbreviation.

    Returns:
        str: Normalized unit abbreviation or original normalized unit.
    """
    normalized = normalize_name(unit)

    return UNIT_ALIASES.get(
        normalized,
        normalized,
    )


def unit_variants(unit):
    """
    Produces singular and plural variants of a unit.

    Args:
        unit: Unit name or abbreviation.

    Returns:
        set[str]: Normalized unit variants.
    """
    normalized = normalize_unit(unit)
    variants = {normalized}

    if normalized.endswith("s"):
        variants.add(normalized[:-1])
    else:
        variants.add(f"{normalized}s")

    return variants