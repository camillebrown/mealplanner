from recipes.recipes_list import *

MEAL_PLAN = {
    "Monday": {
        "Breakfast": {
            "title": "Cottage Cheese Breakfast Tacos",
            "recipe_link": COTTAGE_CHEESE_BREAKFAST_TACOS["recipe_link"],
            "items": [
                *COTTAGE_CHEESE_BREAKFAST_TACOS["items"],
                {"ingredient": MIXED_BERRIES, "serving": 1},
            ],
        },
        "Lunch": WILDBIRD_BONELESS_BREAST_MARKET_PLATE,
        "Dinner": STICKY_SWEET_CHILI_BEEF_BOWL,
        "Snack": RATIO_YOGURT_PARFAIT,
    },

    "Tuesday": {
        "Breakfast": {
            "title": "Breakfast Bake & Apples",
            "items": [
                BREAKFAST_BAKE,
                {"ingredient": APPLES, "serving": 0.75},
            ],
        },
        "Lunch": MIXT_COBB_SALAD_MEAL,
        "Dinner": SPRING_CITRUS_COD,
    },

    "Wednesday": {
        "Breakfast": {
            "title": "Stewed Apples with Ratio Yogurt + Protein Coffee",
            "recipe_link": STEWED_APPLES_AND_YOGURT["recipe_link"],
            "items": [
                STEWED_APPLES_AND_YOGURT,
                PROTEIN_COFFEE,
            ],
        },
        "Lunch": TOCAYA_FAJITA_DEL_REY_BOWL_MEAL,
        "Dinner": TURKEY_PROTEIN_PASTA,
    },

    "Thursday": {
        "Breakfast": AVOCADO_TOAST,
        "Lunch": UMAMI_EXPRESS_CHICKEN_RICE_AND_CABBAGE_BOWL,
        "Dinner": LOADED_CHIPOTLE_STEAK_SWEET_POTATO,
    },

    "Friday": {
        "Breakfast": GRAND_SLAM_BREAKFAST,
        "Lunch": BLACK_ANGUS_GRILLED_SALMON_AND_BROCCOLI,
        "Dinner": TERIYAKI_SHRIMP_BOWL,
    },

    "Saturday": {
        "Breakfast": BREAKFAST_BURRITO,
        "Lunch": TURKEY_LETTUCE_WRAPS,
        "Dinner": BBQ_CHICKEN_FLATBREAD_PIZZA,
        "Snack": SPICY_ASIAN_CUCUMBER_TUNA_SALAD,
    },
}