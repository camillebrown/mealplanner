import json
import re
import subprocess
import sys

from recipes.generators.build_notion_recipe import (
    classify_ingredient_names,
    empty_extracted_recipe_output,
    render_import_report
)
from recipes.generators.tiktok.helpers.parse_caption import (
    parse_tiktok_caption,
)
from recipes.generators.tiktok.helpers.extract_metadata import (
    read_tiktok_page,
)

def import_tiktok_recipe(
    url,
    target_servings=1,
):
    page = read_tiktok_page(url)

    video = page["video"]
    caption = video.get("caption", "")
    parsed_recipe = parse_tiktok_caption(caption)

    report = empty_extracted_recipe_output()

    report["recipe"].update(
        {
            "title": parsed_recipe["title"],
            "source": "tiktok",
            "recipe_link": url,
            "image_url": video.get("cover", ""),
            "overview": parsed_recipe["overview"],
            "prep_time": parsed_recipe["prep_time"],
            "cook_time": parsed_recipe["cook_time"],
            "servings": target_servings,
            "instructions": parsed_recipe["instructions"],
            "notes": [
                (
                    f"Creator: {video.get('creator', '')} "
                    f"(@{video.get('username', '')})"
                ),
                "Raw TikTok caption:",
                caption,
            ],
        }
    )

    report["ingredients"] = classify_ingredient_names(
        parsed_recipe["ingredients"],
        parsed_recipe["servings"],
        target_servings,
    )

    return report


if __name__ == "__main__":
    if len(sys.argv) not in {2, 3}:
        print("Usage:")
        print(
            "python3 -m "
            "recipes.recipe_actions.tiktok.import_tiktok_recipe "
            '"https://www.tiktok.com/..."'
        )
        print(
            "python3 -m "
            "recipes.recipe_actions.tiktok.import_tiktok_recipe "
            '"https://www.tiktok.com/..." 4'
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

    result = import_tiktok_recipe(
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
        "\n✅ Recipe draft and review checklist "
        "copied to clipboard"
    )