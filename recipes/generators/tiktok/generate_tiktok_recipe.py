import subprocess
import sys

from recipes.generators.build_notion_recipe import (
    build_notion_recipe,
)
from recipes.generators.tiktok.helpers.extract_metadata import (
    read_tiktok_page,
)
from recipes.generators.tiktok.helpers.parse_caption import (
    parse_tiktok_caption,
)

def import_tiktok_recipe(
    url,
    target_servings=1,
):
    """
    Imports a TikTok recipe and returns an editable Python draft.

    Args:
        url: TikTok video URL.
        target_servings: Desired number of servings.

    Returns:
        str: Editable Python recipe draft and review notes.
    """
    page = read_tiktok_page(url)

    video = page["video"]
    caption = video.get("caption", "")
    parsed_recipe = parse_tiktok_caption(caption)

    return build_notion_recipe(
        recipe=parsed_recipe,
        source="tiktok",
        recipe_link=url,
        image_url=video.get("cover", ""),
        target_servings=target_servings,
        notes=[
            (
                f"Creator: {video.get('creator', '')} "
                f"(@{video.get('username', '')})"
            ),
            "Raw TikTok caption:",
            caption,
        ],
    )


if __name__ == "__main__":
    if len(sys.argv) not in {2, 3}:
        print("Usage:")
        print(
            "python3 -m "
            "recipes.generators.tiktok.generate_tiktok_recipe"
            '"https://www.tiktok.com/..."'
        )
        print(
            "python3 -m "
            "recipes.generators.tiktok.generate_tiktok_recipe"
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

    output = import_tiktok_recipe(
        sys.argv[1],
        target_servings=target_servings,
    )

    print(output)

    subprocess.run(
        ["pbcopy"],
        input=output.encode(),
    )

    print(
        "\n✅ Recipe draft and review checklist "
        "copied to clipboard"
    )