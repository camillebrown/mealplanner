import re


INSTRUCTION_STARTERS = (
    "add",
    "bake",
    "blend",
    "bring",
    "chop",
    "combine",
    "cook",
    "dry",
    "fry",
    "heat",
    "julienne",
    "microwave",
    "mix",
    "place",
    "pour",
    "put",
    "serve",
    "simmer",
    "slice",
    "stir",
    "top",
    "whisk",
)


NON_INGREDIENT_UNITS = {
    "minute",
    "minutes",
    "min",
    "hour",
    "hours",
    "hr",
    "hrs",
    "calorie",
    "calories",
    "kcal",
    "kcals",
    "protein",
    "fat",
    "carb",
    "carbs",
}


QUANTITY_PATTERN = re.compile(
    r"""^
    (
        \d+\s+\d+/\d+
        |
        \d+/\d+
        |
        \d+(?:\.\d+)?
        |
        pinch\b
        |
        dash\b
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)


def normalize_caption(caption):
    """
    Converts caption line separators into standard newlines.
    """
    return re.sub(
        r"[\u2028\u2029\u0085\r\n]+",
        "\n",
        caption or "",
    )


def caption_lines(caption):
    """
    Returns the non-empty lines from a normalized caption.
    """
    normalized = normalize_caption(caption)

    return [
        line.strip()
        for line in normalized.split("\n")
        if line.strip()
    ]


def suggested_title(caption):
    """
    Extracts a suggested recipe title from the caption.
    """
    lines = caption_lines(caption)

    if not lines:
        return ""

    first_line = lines[0]

    first_line = re.sub(
        r"^\d+\s*MINUTE\s+",
        "",
        first_line,
        flags=re.IGNORECASE,
    )

    return first_line.title()


def suggested_cook_time(caption):
    """
    Extracts a cook time stated before the recipe sections.
    """
    intro = re.split(
        r"\b(?:serves|ingredients|method)\b",
        caption or "",
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]

    match = re.search(
        r"\b(\d+)\s*(?:minute|minutes|min)\b",
        intro,
        re.IGNORECASE,
    )

    return int(match.group(1)) if match else None


def suggested_servings(caption):
    """
    Extracts the source recipe serving count.
    """
    match = re.search(
        r"\b(?:serves|servings|yield|yields)"
        r"\s*:?\s*(\d+(?:\.\d+)?)\b",
        caption or "",
        re.IGNORECASE,
    )

    if not match:
        return None

    value = float(match.group(1))

    return int(value) if value.is_integer() else value


def extract_ingredient_lines(caption):
    """
    Extracts likely ingredient lines from a TikTok caption.
    """
    normalized = normalize_caption(caption)

    # Remove an explicitly labeled method section.
    normalized = re.split(
        r"\bmethod\s*:",
        normalized,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]

    # Separate headings followed by hyphen bullets.
    normalized = re.sub(
        r"\s+([A-Za-z][A-Za-z\s]{2,40}:)\s*-(?=\S)",
        r"\n\1\n",
        normalized,
    )

    # Convert hyphen bullets into separate lines.
    normalized = re.sub(
        r"\s+-\s*(?=\S)",
        "\n",
        normalized,
    )

    lines = [
        line.strip()
        for line in normalized.split("\n")
        if line.strip()
    ]

    ingredient_lines = []
    collecting = False

    for line in lines:
        lower = line.lower()

        if (
            collecting
            and lower.startswith(INSTRUCTION_STARTERS)
        ):
            break

        if line.endswith(":"):
            continue

        quantity_match = QUANTITY_PATTERN.match(line)

        if quantity_match:
            remainder = line[
                quantity_match.end():
            ].strip()

            next_word_match = re.match(
                r"^([A-Za-z]+)",
                remainder,
            )

            next_word = (
                next_word_match.group(1).lower()
                if next_word_match
                else ""
            )

            if next_word in NON_INGREDIENT_UNITS:
                continue

            collecting = True
            ingredient_lines.append(line)
            continue

        if collecting:
            ingredient_lines.append(line)

    return ingredient_lines


def extract_numbered_instructions(method_text):
    """
    Extracts numbered instructions from a Method section.
    """
    steps = re.split(
        r"\s+(?=\d+\.\s)",
        method_text.strip(),
    )

    instructions = []

    for step in steps:
        step = re.sub(
            r"^\d+\.\s*",
            "",
            step.strip(),
        )

        step = re.sub(
            r"\s+#\w.*$",
            "",
            step,
        ).strip()

        if step:
            instructions.append(step)

    return instructions


def extract_line_instructions(caption):
    """
    Extracts instructions written as separate caption lines.
    """
    lines = caption_lines(caption)

    instructions = []
    collecting = False

    for line in lines:
        lower = line.lower()

        if not collecting:
            if lower.startswith(INSTRUCTION_STARTERS):
                collecting = True
            else:
                continue

        line = re.sub(
            r"\s+#\w.*$",
            "",
            line,
        ).strip()

        if line:
            instructions.append(line)

    return instructions


def extract_instructions(caption):
    """
    Extracts numbered or line-separated recipe instructions.
    """
    normalized = normalize_caption(caption)

    method_parts = re.split(
        r"\bmethod\s*:",
        normalized,
        maxsplit=1,
        flags=re.IGNORECASE,
    )

    if len(method_parts) == 2:
        return extract_numbered_instructions(
            method_parts[1]
        )

    return extract_line_instructions(normalized)


def parse_tiktok_caption(caption):
    """
    Converts a TikTok caption into standardized recipe fields.
    """
    return {
        "title": suggested_title(caption),
        "overview": "",
        "prep_time": None,
        "cook_time": suggested_cook_time(caption),
        "servings": suggested_servings(caption),
        "ingredients": extract_ingredient_lines(caption),
        "instructions": extract_instructions(caption),
    }