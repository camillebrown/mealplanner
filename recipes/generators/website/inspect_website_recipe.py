import json
import re
import subprocess
import sys
from html import unescape

import requests
from bs4 import BeautifulSoup

from recipes.generators.website.extract_custom_recipe_card import (
    extract_custom_recipe_card,
)


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0 Safari/537.36"
    )
}


def clean_text(value):
    if value is None:
        return ""

    value = BeautifulSoup(
        str(value),
        "html.parser",
    ).get_text(" ")

    value = unescape(value)

    return re.sub(
        r"\s+",
        " ",
        value,
    ).strip()


def detect_recipe_source(document):
    if document.select_one("#recipe-card"):
        return {
            "type": "custom_recipe_card",
            "selector": "#recipe-card",
        }

    if document.select_one(".wprm-recipe-container"):
        return {
            "type": "wprm",
            "selector": ".wprm-recipe-container",
        }

    if document.select_one(".tasty-recipes"):
        return {
            "type": "tasty_recipes",
            "selector": ".tasty-recipes",
        }

    if document.select_one(".mv-create-card"):
        return {
            "type": "mv_create",
            "selector": ".mv-create-card",
        }

    return {
        "type": "unknown",
        "selector": None,
    }


def inspect_website_recipe(url):
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    document = BeautifulSoup(
        response.text,
        "html.parser",
    )

    detected_source = detect_recipe_source(
        document
    )
    
    recipe = None

    if detected_source["type"] == "custom_recipe_card":
        recipe = extract_custom_recipe_card(
            document,
            detected_source["selector"],
        )
    
    card = document.select_one("#recipe-card")

    if card:
        with open(
            "recipe_card.html",
            "w",
            encoding="utf-8",
        ) as file:
            file.write(card.prettify())

    json_ld_blocks = []

    for index, script in enumerate(
        document.find_all(
            "script",
            attrs={"type": "application/ld+json"},
        ),
        start=1,
    ):
        raw = script.string or script.get_text()

        if not raw or not raw.strip():
            continue

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {
                "parse_error": True,
                "preview": raw[:500],
            }

        json_ld_blocks.append(
            {
                "index": index,
                "data": parsed,
            }
        )

    candidate_selectors = [
        "#recipe-card",
        ".wprm-recipe-container",
        ".wprm-recipe",
        "[id^='wprm-recipe-container']",
        ".tasty-recipes",
        ".mv-create-card",
        "[itemtype*='Recipe']",
    ]

    selector_matches = {}

    for selector in candidate_selectors:
        matches = document.select(selector)

        selector_matches[selector] = {
            "count": len(matches),
            "preview": (
                clean_text(
                    matches[0].get_text(" ")
                )[:1000]
                if matches
                else ""
            ),
        }

    headings = []

    for tag in document.find_all(
        ["h1", "h2", "h3", "h4"],
    ):
        text = clean_text(
            tag.get_text(" ")
        )

        if text:
            headings.append(
                {
                    "tag": tag.name,
                    "text": text,
                    "id": tag.get("id"),
                    "class": tag.get(
                        "class",
                        [],
                    ),
                }
            )

    result = {
        "request": {
            "requested_url": url,
            "final_url": response.url,
            "status": response.status_code,
            "content_type": response.headers.get(
                "content-type"
            ),
            "html_length": len(response.text),
        },
        "page": {
            "title": (
                clean_text(
                    document.title.get_text(" ")
                )
                if document.title
                else ""
            ),
            "meta_description": "",
            "canonical_url": "",
        },
        "detected_source": detected_source,
        "json_ld": json_ld_blocks,
        "candidate_selectors": selector_matches,
        "headings": headings,
        "recipe": recipe,
    }

    description = document.find(
        "meta",
        attrs={"name": "description"},
    )

    if description:
        result["page"]["meta_description"] = (
            description.get("content", "")
        )

    canonical = document.find(
        "link",
        attrs={"rel": "canonical"},
    )

    if canonical:
        result["page"]["canonical_url"] = (
            canonical.get("href", "")
        )

    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python3 -m "
            "recipes.recipe_actions.website."
            "inspect_website_recipe "
            '"https://example.com/recipe"'
        )
        sys.exit(1)

    result = inspect_website_recipe(
        sys.argv[1]
    )

    pretty = json.dumps(
        result,
        indent=2,
        ensure_ascii=False,
    )

    print(pretty)

    subprocess.run(
        ["pbcopy"],
        input=pretty.encode(),
    )

    print(
        "\n✅ Website inspection copied "
        "to clipboard"
    )