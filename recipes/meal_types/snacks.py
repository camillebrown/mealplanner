from recipes.ingredients.index import *

# Snacks
RATIO_YOGURT_PARFAIT = {
    "title": "Ratio Yogurt Parfait",
    "category": "snack",
    "cuisine": "american",
    "source": "personal",
    "restaurant": "",
    "recipe_link": "",
    "image_url": "https://www.katiescucina.com/wp-content/uploads/2022/08/Yogurt-with-Granola.jpg",
    "prep_time": 5,
    "cook_time": 0,
    "servings": 1,
    "tags": ["high protein", "quick"],
    "overview": (
        "A refreshing, high-protein yogurt parfait topped with fresh kiwi, "
        "strawberries, and pineapple. It's a quick, nutritious snack that's "
        "naturally sweet and packed with protein."
    ),
    "instructions": [
        "Wash and prepare the fruit by peeling the kiwi and cutting the kiwi, strawberries, and pineapple into bite-sized pieces.",
        "Spoon the protein yogurt into a serving bowl.",
        "Top evenly with the prepared fruit.",
        "Serve immediately.",
    ],
    "notes": [],
    "items": [
        {"ingredient": PROTEIN_YOGURT, "serving": 1},
        {"ingredient": KIWIS, "serving": 1},
        {"ingredient": STRAWBERRIES, "serving": 1},
        {"ingredient": PINEAPPLE, "serving": 1},
    ],
}

SPICY_ASIAN_CUCUMBER_TUNA_SALAD = {
    "title": "Spicy Asian Cucumber Tuna Salad",
    "category": "snack",
    "cuisine": "asian",
    "source": "personal",
    "restaurant": "",
    "recipe_link": "",
    "image_url": "https://i1.wp.com/safecatch.com/wp-content/uploads/3-ingredient-korean-bbq-tuna-cucumber-salad.jpg",
    "prep_time": 10,
    "cook_time": 0,
    "servings": 1,
    "tags": ["high protein", "quick"],
    "overview": (
        "A refreshing, high-protein tuna salad made with crisp cucumber, green onions, "
        "and a spicy, tangy Asian-inspired dressing. It's a light, flavorful snack that "
        "comes together in just a few minutes."
    ),
    "instructions": [
        "Thinly slice the cucumbers and green onions and add them to a mixing bowl.",
        "Drain the canned tuna well, then add it to the bowl. Gently break it into bite-sized flakes with a fork.",
        "Add the low-sodium soy sauce, rice vinegar, and gochujang. Mix until everything is evenly coated.",
        "Taste and season with salt and black pepper if desired.",
        "Transfer to a serving bowl and garnish with sesame seeds before serving.",
    ],
    "notes": [],
    "items": [
        {"ingredient": CANNED_TUNA, "serving": 1},
        {"ingredient": CUCUMBERS, "serving": 2},
        {"ingredient": SOY_SAUCE, "serving": 0.33},
        {"ingredient": RICE_VINEGAR, "serving": 0.33},
        {"ingredient": GOCHUJANG, "serving": 0.33},
        {"ingredient": GREEN_ONIONS, "serving": 1},
        {"ingredient": SESAME_SEEDS, "serving": 0.5},
    ],
}