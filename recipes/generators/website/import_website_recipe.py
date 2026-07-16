import subprocess
import sys

import requests
from bs4 import BeautifulSoup

from recipes.generators.import_report import (
    classify_ingredient_names,
    empty_import_report,
    render_import_report,
)
from recipes.generators.website.extract_custom_recipe_card import (
    extract_custom_recipe_card,
)
from recipes.generators.website.inspect_website_recipe import (
    HEADERS,
    detect_recipe_source,
)


def import_website_recipe(
    url,
    target_servings=1,
):
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

    if detected_source["type"] != "custom_recipe_card":
        raise ValueError(
            "This website recipe source is not supported yet."
        )

    extracted = extract_custom_recipe_card(
        document,
        detected_source["selector"],
    )

    source_servings = extracted["servings"]

    report = empty_import_report()

    report["recipe"].update(
        {
            "title": extracted["title"],
            "source": "website",
            "recipe_link": url,
            "image_url": extracted["image_url"],
            "prep_time": extracted["prep_time"],
            "cook_time": extracted["cook_time"],
            "servings": target_servings,
            "overview": extracted["overview"],
            "instructions": extracted["instructions"],
            "notes": [],
        }
    )

    report["ingredients"] = classify_ingredient_names(
        extracted["ingredients"],
        source_servings,
        target_servings,
    )

    return report


if __name__ == "__main__":
    if len(sys.argv) not in {2, 3}:
        print("Usage:")
        print(
            "python3 -m "
            "recipes.recipe_actions.website.import_website_recipe "
            '"https://example.com/recipe"'
        )
        print(
            "python3 -m "
            "recipes.recipe_actions.website.import_website_recipe "
            '"https://example.com/recipe" 4'
        )
        sys.exit(1)

    target_servings = (
        int(sys.argv[2])
        if len(sys.argv) == 3
        else 1
    )

    if target_servings < 1:
        raise ValueError(
            "Target servings must be at least 1."
        )

    result = import_website_recipe(
        sys.argv[1],
        target_servings=target_servings,
    )

    output = render_import_report(result)

    print(output)

    subprocess.run(
        ["pbcopy"],
        input=output.encode(),
    )

    print(
        "\n✅ Website recipe draft and review checklist "
        "copied to clipboard"
    )