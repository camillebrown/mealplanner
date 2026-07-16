import re

from bs4 import BeautifulSoup


def clean_text(value):
    if value is None:
        return ""

    text = BeautifulSoup(
        str(value),
        "html.parser",
    ).get_text(" ")

    return re.sub(
        r"\s+",
        " ",
        text,
    ).strip()


def extract_number(value):
    match = re.search(
        r"\d+(?:\.\d+)?",
        value or "",
    )

    if not match:
        return None

    number = float(match.group())

    return int(number) if number.is_integer() else number


def extract_custom_recipe_card(
    document,
    selector="#recipe-card",
):
    card = document.select_one(selector)

    if card is None:
        raise ValueError(
            f"Could not find recipe card using '{selector}'."
        )

    title = ""

    for heading in card.find_all(
        ["h1", "h2", "h3", "h4"],
    ):
        text = clean_text(
            heading.get_text(" ")
        )

        if not text:
            continue

        if text.lower() in {
            "ingredients",
            "instructions",
        }:
            continue

        title = text
        break

    image_url = ""

    image = card.find("img")

    if image:
        image_url = (
            image.get("data-src")
            or image.get("data-lazy-src")
            or image.get("src")
            or ""
        )

    overview = ""

    for paragraph in card.find_all("p"):
        text = clean_text(
            paragraph.get_text(" ")
        )

        if not text:
            continue

        if text.lower() in {
            "print recipe",
            "pin recipe",
        }:
            continue

        overview = text
        break

    card_text = clean_text(
        card.get_text(" ")
    )

    prep_time = None
    cook_time = None
    total_time = None
    servings = None

    prep_match = re.search(
        r"Prep Time:\s*(.+?)"
        r"(?=Cook Time:|Total Time:|Yields:|Ingredients)",
        card_text,
        re.IGNORECASE,
    )

    if prep_match:
        prep_time = extract_number(
            prep_match.group(1)
        )

    cook_match = re.search(
        r"Cook Time:\s*(.+?)"
        r"(?=Total Time:|Yields:|Ingredients)",
        card_text,
        re.IGNORECASE,
    )

    if cook_match:
        cook_time = extract_number(
            cook_match.group(1)
        )

    total_match = re.search(
        r"Total Time:\s*(.+?)"
        r"(?=Yields:|Ingredients)",
        card_text,
        re.IGNORECASE,
    )

    if total_match:
        total_time = extract_number(
            total_match.group(1)
        )

    servings_match = re.search(
        r"Yields:\s*(.+?)"
        r"(?=Ingredients)",
        card_text,
        re.IGNORECASE,
    )

    if servings_match:
        servings = extract_number(
            servings_match.group(1)
        )

    ingredients = []
    instructions = []

    current_section = None

    for element in card.find_all(
        ["h1", "h2", "h3", "h4", "li"],
    ):
        if element.name in {
            "h1",
            "h2",
            "h3",
            "h4",
        }:
            heading = clean_text(
                element.get_text(" ")
            ).lower()

            if heading == "ingredients":
                current_section = "ingredients"

            elif heading == "instructions":
                current_section = "instructions"

            continue

        text = clean_text(
            element.get_text(" ")
        )

        if not text:
            continue

        if current_section == "ingredients":
            ingredients.append(text)

        elif current_section == "instructions":
            instructions.append(text)

    page_title = document.find("h1")

    if page_title:
        title = clean_text(
            page_title.get_text(" ")
        )
    
    return {
        "title": title,
        "image_url": image_url,
        "overview": overview,
        "prep_time": prep_time,
        "cook_time": cook_time,
        "total_time": total_time,
        "servings": servings,
        "ingredients": ingredients,
        "instructions": instructions,
    }