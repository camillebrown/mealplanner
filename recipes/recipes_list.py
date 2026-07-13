from ingredients import *

# Breakfasts
COTTAGE_CHEESE_BREAKFAST_TACOS = {
    "title": "Cottage Cheese Breakfast Tacos",
    "category": "breakfast",
    "cuisine": "mexican",
    "source": "tiktok",
    "restaurant": "",
    "recipe_link": "https://www.tiktok.com/t/ZTSC3Uwxk/",
    "image_url": "https://i0.wp.com/foodieholly.com/wp-content/uploads/2024/09/11.png?w=900&ssl=1",
    "prep_time": 10,
    "cook_time": 35,
    "servings": 2,
    "tags": ["high protein"],
    "overview": (
        "Packed with protein from cottage cheese and eggs, these savory breakfast "
        "tacos are not only satisfying but also relatively low in fat, making them "
        "a perfect option for a healthy start."
    ),
    "instructions": [
        "Preheat the oven to 400°F (200°C).",
        "In a bowl, whisk together the low-fat cottage cheese and liquid egg whites until smooth and well combined.",
        "Line a baking sheet with parchment paper. Divide the mixture into two equal circles, spreading each into thin, even layers to form the taco shells. Season with salt, pepper, oregano, and chili flakes if desired.",
        "Bake for 20–35 minutes, or until the taco shells are golden brown and crispy. About halfway through baking, blot away any excess moisture with a paper towel and gently reshape the taco shells with a spatula if needed.",
        "Remove the taco shells from the oven and let them cool for about 10 minutes so they become firm and crisp.",
        "While the taco shells are cooling, cook the turkey bacon until crisp and prepare the whole eggs to your preferred doneness.",
        "Fill each taco shell with the cooked eggs and turkey bacon. Garnish with chopped chives and finish with hot sauce.",
        "Serve immediately while the taco shells are crisp.",
    ],
    "notes": [],
    "items": [
        {"ingredient": LOW_FAT_COTTAGE_CHEESE, "serving": 4},
        {"ingredient": LIQUID_EGG_WHITES, "serving": 0.3},
        {"ingredient": WHOLE_EGG, "serving": 2},
        {"ingredient": TURKEY_BACON, "serving": 3},
        {"ingredient": CHIVES, "serving": 1},
        {"ingredient": HOT_SAUCE, "serving": 1},
    ],
}

BREAKFAST_BAKE = {
    "title": "Breakfast Bake",
    "category": "breakfast",
    "cuisine": "american",
    "source": "tiktok",
    "restaurant": "",
    "recipe_link": "https://www.tiktok.com/t/ZTSVL9o95/",
    "image_url": "https://sallysbakingaddiction.com/wp-content/uploads/2015/09/breakfast-casserole-2.jpg",
    "prep_time": 10,
    "cook_time": 30,
    "servings": 1,
    "tags": ["high protein"],
    "overview": (
        "A hearty, high-protein breakfast bake layered with a crispy hash brown "
        "patty, eggs, turkey bacon, chicken sausage, vegetables, and melted cheddar. "
        "Everything bakes together in one dish for an easy, satisfying breakfast "
        "that's perfect for meal prep."
    ),
    "instructions": [
        "Preheat the oven to 375°F (190°C).",
        "Place the hash brown patty in the bottom of a small oven-safe baking dish.",
        "In a bowl, whisk together the liquid egg whites and whole egg until well combined. Season with salt and pepper if desired.",
        "Pour the egg mixture evenly over the hash brown patty.",
        "Chop the turkey bacon, chicken sausage, spinach, bell pepper, and onion into bite-sized pieces.",
        "Evenly distribute the turkey bacon, chicken sausage, spinach, bell pepper, and onion over the egg mixture.",
        "Sprinkle the low-fat cheddar evenly over the top.",
        "Bake for 30 minutes, or until the eggs are fully set, the turkey bacon and chicken sausage are cooked through, and the cheese is melted and lightly golden.",
        "Allow the breakfast bake to cool for a few minutes before serving.",
    ],
    "notes": [],
    "items": [
        {"ingredient": HASH_BROWN_PATTIES, "serving": 1},
        {"ingredient": LIQUID_EGG_WHITES, "serving": 1.5},
        {"ingredient": WHOLE_EGG, "serving": 1},
        {"ingredient": TURKEY_BACON, "serving": 1},
        {"ingredient": CHICKEN_SAUSAGE, "serving": 1},
        {"ingredient": LOW_FAT_CHEDDAR, "serving": 1},
        {"ingredient": SPINACH, "serving": 1},
        {"ingredient": BELL_PEPPERS, "serving": 0.5},
        {"ingredient": ONIONS, "serving": 1},
    ],
}

STEWED_APPLES_AND_YOGURT = {
    "title": "Stewed Apples with Yogurt",
    "category": "breakfast",
    "cuisine": "american",
    "source": "website",
    "restaurant": "",
    "recipe_link": "https://plantyou.com/healthy-stewed-apples/",
    "image_url": "https://cleananddelicious.com/wp-content/uploads/2025/06/stovetop-cinnamon-apples-3.jpg",
    "prep_time": 5,
    "cook_time": 15,
    "servings": 1,
    "tags": ["high protein"],
    "overview": (
        "Tender cinnamon-spiced stewed apples served over protein yogurt for a warm, "
        "high-protein breakfast that's naturally sweet, comforting, and perfect for "
        "meal prep."
    ),
    "instructions": [
        "Core and dice the apple into bite-sized pieces.",
        "Add the apple, sugar-free syrup, vanilla extract, ground cinnamon, and cornstarch to a small saucepan. Stir until the apples are evenly coated.",
        "Cook over medium heat for about 15 minutes, stirring occasionally, until the apples are tender and the sauce has thickened.",
        "Allow the stewed apples to cool for a few minutes.",
        "Serve warm over the protein yogurt.",
    ],
    "notes": [],
    "items": [
        {"ingredient": PROTEIN_YOGURT, "serving": 1},
        {"ingredient": APPLES, "serving": 1},
        {"ingredient": SUGAR_FREE_SYRUP, "serving": 1},
        {"ingredient": VANILLA_EXTRACT, "serving": 2},
        {"ingredient": GROUND_CINNAMON, "serving": 1},
        {"ingredient": CORNSTARCH, "serving": 1.5},
    ],
}

PROTEIN_COFFEE = {
    "title": "Protein Coffee",
    "category": "drink",
    "cuisine": "american",
    "source": "personal",
    "restaurant": "",
    "recipe_link": "",
    "image_url": "https://cleananddelicious.com/wp-content/uploads/2026/05/protein-coffee.jpg",
    "prep_time": 2,
    "cook_time": 0,
    "servings": 1,
    "tags": ["high protein", "quick"],
    "overview": (
        "A quick, high-protein coffee made by blending a ready-to-drink protein "
        "shake with protein coffee powder for an easy breakfast or snack."
    ),
    "instructions": [
        "Pour a small portion of the protein shake into a glass.",
        "Add one scoop of protein coffee powder.",
        "Use a handheld frother to blend the protein powder into the protein shake, starting low in the glass and slowly lifting it as it thickens to create a smooth, super-frothy foam.",
        "Pour remaining protein shake and cooled coffee into the protein mixture with ice, and gently stir.",
        "Serve and enjoy, with a sprinkle of cinnamon on top if you’d like.",
    ],
    "notes": [],
    "items": [
        {"ingredient": PREMIER_PROTEIN_SHAKE, "serving": 1},
        {"ingredient": JAVVY_PROTEIN_COFFEE, "serving": 1},
    ],
}

AVOCADO_TOAST = {
    "title": "Avocado Toast",
    "category": "breakfast",
    "cuisine": "american",
    "source": "personal",
    "restaurant": "",
    "recipe_link": "",
    "image_url": "https://www.kudoskitchenbyrenee.com/wp-content/uploads/2016/05/avocado-toast-with-bacon-and-egg-1.jpg",
    "prep_time": 10,
    "cook_time": 10,
    "servings": 1,
    "tags": ["high protein"],
    "overview": (
        "Creamy avocado toast layered with a savory cottage cheese and blistered "
        "tomato spread, then topped with fluffy eggs for a fresh, satisfying, "
        "high-protein breakfast."
    ),
    "instructions": [
        "Toast the sourdough bread until golden and crisp.",
        "Heat a nonstick skillet over medium heat and lightly coat with cooking spray. Add the cherry tomatoes and garlic, gently mashing the tomatoes as they soften. Cook for about 5 minutes, then remove from the skillet and allow the mixture to cool slightly.",
        "Once the tomato mixture has cooled slightly, stir it together with the cottage cheese until well combined.",
        "Mash the avocado with a fork and season lightly with salt and pepper.",
        "Using the same skillet, add the liquid egg whites and whole egg. Gently stir together and cook to your preferred style, such as soft scrambled.",
        "Spread the cottage cheese and tomato mixture over the toasted sourdough, followed by the mashed avocado and cooked eggs.",
        "Finish with a sprinkle of red pepper flakes and serve immediately.",
    ],
    "notes": [],
    "items": [
        {"ingredient": SOURDOUGH_BREAD, "serving": 2},
        {"ingredient": LOW_FAT_COTTAGE_CHEESE, "serving": 2},
        {"ingredient": CHERRY_TOMATOES, "serving": 1},
        {"ingredient": GARLIC, "serving": 1},
        {"ingredient": AVOCADOS, "serving": 0.5},
        {"ingredient": WHOLE_EGG, "serving": 1},
        {"ingredient": LIQUID_EGG_WHITES, "serving": 1.5},
    ],
}

GRAND_SLAM_BREAKFAST = {
    "title": "Grand Slam Breakfast",
    "category": "breakfast",
    "cuisine": "american",
    "source": "personal",
    "restaurant": "",
    "recipe_link": "",
    "image_url": "https://hip2save.com/wp-content/uploads/2020/05/dennys-grand-slam-breakfast-eggs-bacon-sausage-pancakes.jpg?resize=1024%2C538&strip=all",
    "prep_time": 5,
    "cook_time": 15,
    "servings": 1,
    "tags": ["high protein"],
    "overview": (
        "A high-protein take on the classic diner breakfast featuring fluffy protein "
        "scrambled eggs, protein pancakes, crispy turkey bacon, and sugar-free syrup "
        "for a satisfying start to the day."
    ),
    "instructions": [
        "Preheat the oven and cook the protein pancakes according to the package directions.",
        "In a blender, combine the low-fat cottage cheese, liquid egg whites, and whole egg until smooth.",
        "Heat a nonstick skillet over medium heat and lightly coat with cooking spray. Pour in the egg mixture and gently scramble until fully cooked.",
        "Cook the turkey bacon according to your preferred level of crispness.",
        "Plate the protein pancakes, scrambled eggs, and turkey bacon together.",
        "Top the pancakes with sugar-free syrup and serve immediately.",
    ],
    "notes": [],
    "items": [
        {"ingredient": PROTEIN_PANCAKES, "serving": 0.5},
        {"ingredient": LIQUID_EGG_WHITES, "serving": 1},
        {"ingredient": LOW_FAT_COTTAGE_CHEESE, "serving": 1.87},
        {"ingredient": WHOLE_EGG, "serving": 1},
        {"ingredient": TURKEY_BACON, "serving": 2},
        {"ingredient": SUGAR_FREE_SYRUP, "serving": 1},
    ],
}

BREAKFAST_BURRITO = {
    "title": "Breakfast Burrito",
    "category": "breakfast",
    "cuisine": "mexican",
    "source": "personal",
    "restaurant": "",
    "recipe_link": "",
    "image_url": "https://www.allrecipes.com/thmb/BmnDvAZyG_N-R3jhVQxGAF_szG0=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/261844-freeze-and-reheat-breakfast-burritos-ddmfs-3X4-0359-8c6dd90974a545ddab2504633cd43f00.jpg",
    "prep_time": 10,
    "cook_time": 20,
    "servings": 1,
    "tags": ["high protein"],
    "overview": (
        "A hearty, high-protein breakfast burrito packed with fluffy cottage cheese "
        "eggs, crispy turkey bacon, a golden hash brown, and melted cheddar cheese "
        "wrapped in a protein tortilla."
    ),
    "instructions": [
        "Preheat the oven to 400°F (200°C).",
        "Place the hash brown patty on a lightly greased baking sheet and bake for 6 to 7 minutes. Flip and bake for another 6 to 7 minutes, or until golden and crispy. Remove from the oven and set aside.",
        "While the hash brown cooks, blend together the low-fat cottage cheese, liquid egg whites, and whole egg until smooth.",
        "Heat a nonstick skillet over medium heat and lightly coat with cooking spray. Pour in the egg mixture and gently scramble until fully cooked.",
        "Cook the turkey bacon to your preferred level of crispness.",
        "Warm the protein tortilla until pliable.",
        "Layer the scrambled eggs in the center of the tortilla, followed by the shredded low-fat cheddar, turkey bacon, and the hash brown patty.",
        "Fold in the sides of the tortilla and tightly roll it into a burrito.",
        "Place the burrito seam-side down on the baking sheet and bake for 3 to 5 minutes, flipping halfway through, until the tortilla is lightly toasted and the cheese has melted.",
        "Serve immediately.",
    ],
    "notes": [],
    "items": [
        {"ingredient": PROTEIN_TORTILLA, "serving": 1},
        {"ingredient": LIQUID_EGG_WHITES, "serving": 1},
        {"ingredient": WHOLE_EGG, "serving": 1},
        {"ingredient": TURKEY_BACON, "serving": 2},
        {"ingredient": HASH_BROWN_PATTIES, "serving": 1},
        {"ingredient": LOW_FAT_COTTAGE_CHEESE, "serving": 1.87},
        {"ingredient": LOW_FAT_CHEDDAR, "serving": 1},
    ],
}

# Lunches
WILDBIRD_BONELESS_BREAST_MARKET_PLATE = {
    "title": "Wildbird Boneless Breast Market Plate",
    "category": "doordash",
    "cuisine": "american",
    "source": "restaurant",
    "restaurant": "Wildbird",
    "recipe_link": "",
    "image_url": "https://img.cdn4dd.com/p/fit=cover,width=1200,height=1200,format=auto,quality=70/media/photosV2/e2414374-0747-4b3c-a44e-a016ef860765-retina-large.jpg",
    "prep_time": 0,
    "cook_time": 0,
    "servings": 1,
    "tags": ["high protein"],
    "overview": (
        "A high-protein marketplace bowl from Wildbird featuring blackened chicken "
        "served over fresh romaine lettuce. A quick, healthy restaurant option for "
        "lunch or dinner."
    ),
    "instructions": [
        "Order the Boneless Breast Market Plate from Wildbird.",
        "Substitute the base with romaine lettuce.",
        "Add extra blackened chicken.",
        "Enjoy immediately."
    ],
    "notes": [
        "Romaine lettuce",
        "Extra blackened chicken",
    ],
    "items": [
        {"ingredient": WILDBIRD_BONELESS_BREAST_MARKET_PLATE, "serving": 1},
    ],
}

MIXT_COBB_SALAD_MEAL = {
    "title": "Mixt Cobb Salad",
    "category": "doordash",
    "cuisine": "american",
    "source": "restaurant",
    "restaurant": "Mixt",
    "recipe_link": "",
    "image_url": "https://www.erinliveswhole.com/wp-content/uploads/2021/07/chicken-cobb-salad-3.jpg",
    "prep_time": 0,
    "cook_time": 0,
    "servings": 1,
    "tags": ["high protein"],
    "overview": (
        "A customized Cobb salad from Mixt made with butter lettuce, grilled and "
        "blackened chicken, fresh vegetables, feta, and balsamic vinaigrette for a "
        "high-protein, macro-friendly meal."
    ),
    "instructions": [
        "Order the Cobb Salad from Mixt.",
        "Use butter lettuce as the base.",
        "Choose grilled chicken and add extra blackened chicken.",
        "Include egg, tomato, cucumber, green onion, feta, and balsamic vinaigrette.",
        "Remove the avocado, bacon, blue cheese, and champagne vinaigrette.",
        "Enjoy immediately."
    ],
    "notes": [
        "Butter lettuce",
        "Grilled chicken",
        "Extra blackened chicken",
        "Egg",
        "Tomato",
        "Cucumber",
        "Green onion",
        "Feta",
        "Balsamic vinaigrette",
        "No avocado",
        "No bacon",
        "No blue cheese",
        "No champagne vinaigrette",
    ],
    "items": [
        {"ingredient": MIXT_COBB_SALAD, "serving": 1},
    ],
}

TOCAYA_FAJITA_DEL_REY_BOWL_MEAL = {
    "title": "Tocaya Fajita Del Rey Bowl",
    "category": "doordash",
    "cuisine": "mexican",
    "source": "restaurant",
    "restaurant": "Tocaya",
    "recipe_link": "",
    "image_url": "https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1920,format=auto,quality=50,metadata=none,anim=false/https://doordash-static.s3.amazonaws.com/media/photosV2/99083da9-447a-439f-9224-bf190b6f0b3b-retina-large.jpg",
    "prep_time": 0,
    "cook_time": 0,
    "servings": 1,
    "tags": ["high protein"],
    "overview": (
        "A customized Fajita Del Rey Bowl from Tocaya featuring chicken tinga, "
        "cilantro lime rice, black beans, fajita vegetables, fresh pico de gallo, "
        "and queso fresco for a balanced, high-protein meal."
    ),
    "instructions": [
        "Order the Fajita Del Rey Bowl from Tocaya.",
        "Choose chicken tinga as the protein.",
        "Include cilantro lime rice, black beans, pico de gallo, and queso fresco.",
        "Add fajita vegetables.",
        "Remove the guacamole and vegan chipotle crema.",
        "Enjoy immediately."
    ],
    "notes": [
        "Chicken tinga",
        "Queso fresco",
        "Cilantro lime rice",
        "Black beans",
        "Pico de gallo",
        "Add fajita veggies",
        "No guacamole",
        "No vegan chipotle crema",
    ],
    "items": [
        {"ingredient": TOCAYA_FAJITA_DEL_REY_BOWL, "serving": 1},
    ],
}

UMAMI_EXPRESS_CHICKEN_RICE_AND_CABBAGE_BOWL = {
    "title": "Umami Express Chicken Rice & Cabbage Bowl",
    "category": "doordash",
    "cuisine": "asian",
    "source": "restaurant",
    "restaurant": "Umami Express",
    "recipe_link": "",
    "image_url": "https://images.squarespace-cdn.com/content/v1/5fa716a9ec3d205d12252d14/07ee45f2-f4ea-4697-ba20-4d93d37200b8/umami-express-pork-shoulder-rice-and-cabbage-bowl.jpg",
    "prep_time": 0,
    "cook_time": 0,
    "servings": 1,
    "tags": ["high protein"],
    "overview": (
        "A customized Chicken Rice & Cabbage Bowl from Umami Express featuring "
        "extra chicken, fresh cucumber, and lemon garlic soy sauce for a simple, "
        "balanced, high-protein meal."
    ),
    "instructions": [
        "Order the Chicken Rice & Cabbage Bowl from Umami Express.",
        "Add extra chicken.",
        "Add cucumber.",
        "Choose the lemon garlic soy sauce.",
        "Enjoy immediately.",
    ],
    "notes": [
        "Extra chicken",
        "Cucumber",
        "Lemon garlic soy",
    ],
    "items": [
        {"ingredient": UMAMI_CHICKEN_RICE_CABBAGE_BOWL, "serving": 1},
    ],
}

BLACK_ANGUS_GRILLED_SALMON_AND_BROCCOLI = {
    "title": "Black Angus Grilled Salmon & Broccoli",
    "category": "doordash",
    "cuisine": "american",
    "source": "restaurant",
    "restaurant": "Black Angus",
    "recipe_link": "",
    "image_url": "https://wholeandheavenlyoven.com/wp-content/uploads/2025/07/BBQ-Salmon-and-Broccoli-Featured-Image.jpg",
    "prep_time": 0,
    "cook_time": 0,
    "servings": 1,
    "tags": ["high protein"],
    "overview": (
        "A simple, protein-packed meal from Black Angus featuring grilled salmon "
        "paired with a side of fresh broccoli for a balanced and nutritious lunch "
        "or dinner."
    ),
    "instructions": [
        "Order the Grilled Salmon from Black Angus.",
        "Choose fresh broccoli as the side.",
        "Enjoy immediately.",
    ],
    "notes": [],
    "items": [
        {"ingredient": BLACK_ANGUS_GRILLED_SALMON, "serving": 1},
        {"ingredient": BLACK_ANGUS_FRESH_BROCCOLI, "serving": 1},
    ],
}

TURKEY_LETTUCE_WRAPS = {
    "title": "Turkey Lettuce Wraps",
    "category": "lunch",
    "cuisine": "asian",
    "source": "website",
    "restaurant": "",
    "recipe_link": "https://www.eatyourselfskinny.com/healthy-turkey-lettuce-wraps/",
    "image_url": "https://www.eatyourselfskinny.com/wp-content/uploads/2023/01/lettuce-wraps-1-scaled.jpg",
    "prep_time": 10,
    "cook_time": 15,
    "servings": 1,
    "tags": ["high protein"],
    "overview": (
        "Lean ground turkey is tossed in a sweet and savory gochujang sauce with "
        "fresh vegetables, then wrapped in crisp butter lettuce for a light yet "
        "satisfying high-protein lunch."
    ),
    "instructions": [
        "In a small bowl, whisk together the low-sodium soy sauce, rice vinegar, gochujang, and honey until smooth.",
        "Heat a large nonstick skillet over medium-high heat and add the ground turkey. Cook, breaking it apart into crumbles until nearly browned.",
        "Add the garlic, ginger, and diced bell peppers. Cook for another 3 to 5 minutes until fragrant and the peppers begin to soften.",
        "Pour the sauce into the skillet and stir until the turkey is evenly coated. Simmer for 1 to 2 minutes until the sauce slightly thickens.",
        "Remove the skillet from the heat and stir in the sliced green onions.",
        "Spoon the turkey mixture into the butter lettuce leaves.",
        "Garnish with sesame seeds and serve immediately.",
    ],
    "notes": [],
    "items": [
        {"ingredient": GROUND_TURKEY, "serving": 1},
        {"ingredient": BUTTER_LETTUCE, "serving": 2},
        {"ingredient": GARLIC, "serving": 2},
        {"ingredient": GINGER, "serving": 1},
        {"ingredient": GREEN_ONIONS, "serving": 1},
        {"ingredient": BELL_PEPPERS, "serving": 0.5},
        {"ingredient": LOW_SODIUM_SOY_SAUCE, "serving": 1},
        {"ingredient": RICE_VINEGAR, "serving": 1},
        {"ingredient": GOCHUJANG, "serving": 1},
        {"ingredient": HONEY, "serving": 0.33},
        {"ingredient": SESAME_SEEDS, "serving": 1},
    ],
}

# Dinners
STICKY_SWEET_CHILI_BEEF_BOWL = {
    "title": "Sticky Sweet Chili Beef Bowl",
    "category": "dinner",
    "cuisine": "asian",
    "source": "tiktok",
    "restaurant": "",
    "recipe_link": "https://www.tiktok.com/t/ZTSCcuoPK/",
    "image_url": "https://www.recipetineats.com/uploads/2024/12/Thai-sweet-chilli-beef-bowls_0.jpg",
    "prep_time": 10,
    "cook_time": 15,
    "servings": 1,
    "tags": ["high protein"],
    "overview": (
        "A quick, high-protein beef bowl with lean ground beef, jasmine rice, "
        "crisp vegetables, and a sticky sweet chili gochujang sauce. It is an "
        "easy, flavorful dinner that comes together in one skillet."
    ),
    "instructions": [
        "Prepare the jasmine rice according to the package directions.",
        "In a small bowl, whisk together the gochujang, honey, rice vinegar, and low-sodium soy sauce until smooth.",
        "In a separate small bowl, stir the cornstarch with a small amount of hot water until fully dissolved to make a slurry.",
        "Heat a nonstick skillet over medium heat. Season the ground beef with salt and pepper, then cook, breaking it into small crumbles, until browned and fully cooked.",
        "Add the minced garlic and grated ginger to the skillet. Cook for about 2 minutes until fragrant.",
        "Add the diced bell pepper and season lightly with salt and pepper. Cook for another 3 to 5 minutes until slightly softened.",
        "Pour the prepared sauce and cornstarch slurry into the skillet. Stir until the beef and vegetables are evenly coated.",
        "Bring the sauce to a gentle boil, then reduce the heat and simmer for 1 to 2 minutes, stirring frequently, until thick and glossy.",
        "Add the jasmine rice to a bowl and top with the sticky sweet chili beef mixture.",
        "Finish with the grated carrot and sliced green onions, then serve immediately.",
    ],
    "notes": [],
    "items": [
        {"ingredient": GROUND_BEEF, "serving": 1},
        {"ingredient": JASMINE_RICE, "serving": 1},
        {"ingredient": BELL_PEPPERS, "serving": 0.5},
        {"ingredient": CARROTS, "serving": 0.5},
        {"ingredient": GARLIC, "serving": 1},
        {"ingredient": GINGER, "serving": 1},
        {"ingredient": GOCHUJANG, "serving": 2},
        {"ingredient": HONEY, "serving": 0.5},
        {"ingredient": RICE_VINEGAR, "serving": 2},
        {"ingredient": LOW_SODIUM_SOY_SAUCE, "serving": 1},
        {"ingredient": CORNSTARCH, "serving": 2},
        {"ingredient": GREEN_ONIONS, "serving": 1},
    ],
}

SPRING_CITRUS_COD = {
    "title": "Spring Citrus Cod",
    "category": "dinner",
    "cuisine": "american",
    "source": "tiktok",
    "restaurant": "",
    "recipe_link": "https://www.tiktok.com/t/ZTSCo3MoR/",
    "image_url": "https://www.sipandfeast.com/wp-content/uploads/2026/03/baked-cod-lemon-potatoes-snippet-2-600x600.jpg",
    "prep_time": 15,
    "cook_time": 35,
    "servings": 1,
    "tags": ["high protein"],
    "overview": (
        "Tender citrus-roasted cod served with crispy roasted baby potatoes and "
        "charred broccoli. Bright lemon, garlic, and fresh herbs make this an easy, "
        "high-protein dinner with minimal cleanup."
    ),
    "instructions": [
        "Preheat the oven to 380°F (193°C).",
        "Halve the baby potatoes and toss with olive oil, salt, black pepper, garlic powder, and paprika. Spread them in a single layer on a baking sheet and roast for 30 to 35 minutes, flipping halfway through, until golden brown and fork tender.",
        "Line the bottom of a baking dish with fresh orange and lemon slices.",
        "Place the cod on top of the citrus slices.",
        "In a small bowl, combine olive oil, paprika, chopped chives, chopped dill, grated garlic, vinegar, lemon juice, salt, and black pepper.",
        "Top the cod with a few small pieces of cold butter.",
        "Bake for 15 to 18 minutes, or until the cod flakes easily with a fork.",
        "While the cod finishes cooking, heat a nonstick skillet over medium-high heat. Add the broccoli and sauté until lightly charred and tender-crisp. Season to taste with salt, pepper, and garlic powder.",
        "Serve the cod alongside the roasted baby potatoes and sautéed broccoli. Finish with an extra squeeze of fresh lemon before serving.",
    ],
    "notes": [],
    "items": [
        {"ingredient": COD, "serving": 1},
        {"ingredient": BABY_POTATOES, "serving": 1},
        {"ingredient": BROCCOLI, "serving": 1},
        {"ingredient": GARLIC, "serving": 2},
    ],
}

TURKEY_PROTEIN_PASTA = {
    "title": "Turkey Protein Pasta",
    "category": "dinner",
    "cuisine": "italian",
    "source": "personal",
    "restaurant": "",
    "recipe_link": "",
    "image_url": "https://fitfoodiefinds.com/wp-content/uploads/2022/02/Ground-Turkey-Shells-3.jpg",
    "prep_time": 10,
    "cook_time": 20,
    "servings": 1,
    "tags": ["high protein"],
    "overview": (
        "A simple, high-protein pasta made with lean ground turkey, sautéed "
        "vegetables, marinara sauce, and protein pasta. It's an easy weeknight "
        "dinner that's hearty, flavorful, and perfect for hitting your protein goals."
    ),
    "instructions": [
        "Bring a large pot of salted water to a boil and cook the protein pasta according to the package directions until al dente. Reserve a small amount of pasta water before draining.",
        "While the pasta cooks, heat a large nonstick skillet over medium heat and lightly coat with cooking spray or olive oil.",
        "Add the diced onion and bell pepper and sauté for 4 to 5 minutes until they begin to soften.",
        "Stir in the minced garlic and cook for about 30 seconds until fragrant.",
        "Add the ground turkey and cook, breaking it into small crumbles, until fully browned and cooked through.",
        "Pour in the marinara sauce and stir to combine. Simmer for 3 to 5 minutes until heated through. If the sauce becomes too thick, stir in a splash of the reserved pasta water.",
        "Add the cooked pasta to the skillet and toss until evenly coated in the sauce.",
        "Serve immediately.",
    ],
    "notes": [],
    "items": [
        {"ingredient": GROUND_TURKEY, "serving": 1},
        {"ingredient": PROTEIN_PASTA, "serving": 1},
        {"ingredient": MARINARA_SAUCE, "serving": 1},
        {"ingredient": ONIONS, "serving": 1},
        {"ingredient": BELL_PEPPERS, "serving": 0.5},
        {"ingredient": GARLIC, "serving": 2},
    ],
}

LOADED_CHIPOTLE_STEAK_SWEET_POTATO = {
    "title": "Loaded Chipotle Steak Sweet Potato",
    "category": "dinner",
    "cuisine": "american",
    "source": "tiktok",
    "restaurant": "",
    "recipe_link": "https://www.tiktok.com/t/ZTSXeoune/",
    "image_url": "https://www.delishdlites.com/wp-content/uploads/2015/01/DSC_02211.jpg",
    "prep_time": 15,
    "cook_time": 100,
    "servings": 1,
    "tags": ["high protein"],
    "overview": (
        "A roasted sweet potato loaded with juicy sirloin steak, fresh tomato salsa, "
        "and a smoky chipotle yogurt sauce. This hearty, high-protein dinner balances "
        "sweet, savory, and tangy flavors in every bite."
    ),
    "instructions": [
        "Preheat the oven to 350°F.",
        "Pierce the sweet potato several times with a fork. Rub it with the olive oil and season generously with salt and black pepper. Bake for 70 minutes, then carefully flip and bake for another 30 minutes, or until the potato is very soft and the skin is lightly caramelized.",
        "While the potato bakes, prepare the chipotle yogurt by mixing together the protein yogurt, chipotle in adobo sauce, a squeeze of fresh lime juice, salt, and pepper.",
        "Prepare the salsa by combining the diced tomato, diced red onion, the remaining lime juice, red wine vinegar, salt, and pepper. Stir well and set aside while the steak cooks.",
        "Season the sirloin steak generously with salt, black pepper, and garlic powder. Cook in a hot skillet over medium-high heat until it reaches your preferred doneness. During the last minute of cooking, add the minced garlic to the pan and spoon the garlic over the steak.",
        "Remove the steak from the skillet and allow it to rest for 5 minutes before slicing into thin strips.",
        "Slice the baked sweet potato open and gently fluff the inside with a fork.",
        "Top the sweet potato with the sliced steak, fresh salsa, and a generous drizzle of the chipotle yogurt sauce.",
        "Serve immediately with an extra squeeze of fresh lime if desired.",
    ],
    "notes": [],
    "items": [
        {"ingredient": SIRLOIN_STEAK, "serving": 1},
        {"ingredient": SWEET_POTATOES, "serving": 1},
        {"ingredient": PROTEIN_YOGURT, "serving": 0.75},
        {"ingredient": CHIPOTLE_IN_ADOBO, "serving": 1},
        {"ingredient": GARLIC, "serving": 0.5},
        {"ingredient": OLIVE_OIL, "serving": 0.5},
        {"ingredient": RED_WINE_VINEGAR, "serving": 1},
        {"ingredient": RED_ONION, "serving": 0.25},
        {"ingredient": TOMATOES, "serving": 1},
        {"ingredient": LIMES, "serving": 1},
    ],
}

TERIYAKI_SHRIMP_BOWL = {
    "title": "Teriyaki Shrimp Bowl",
    "category": "dinner",
    "cuisine": "asian",
    "source": "personal",
    "restaurant": "",
    "recipe_link": "",
    "image_url": "https://mariefoodtips.com/wp-content/uploads/2024/04/teriyaki-shrimp-3-1.jpg",
    "prep_time": 10,
    "cook_time": 20,
    "servings": 1,
    "tags": ["high protein"],
    "overview": (
        "Juicy shrimp and sautéed vegetables are tossed in a homemade teriyaki "
        "sauce and served over jasmine rice for a quick, high-protein dinner that's "
        "sweet, savory, and packed with flavor."
    ),
    "instructions": [
        "Prepare the jasmine rice according to the package directions.",
        "In a small bowl, whisk together the low-sodium soy sauce, honey, rice vinegar, and cornstarch until smooth. Set aside.",
        "Season the shrimp lightly with salt and black pepper.",
        "Heat a large nonstick skillet over medium-high heat. Add the shrimp and cook for 1 to 2 minutes per side, or until pink and cooked through. Remove from the skillet and set aside.",
        "In the same skillet, add the diced onion and bell pepper. Cook for 4 to 5 minutes until they begin to soften.",
        "Add the minced garlic and grated ginger and cook for about 30 seconds until fragrant.",
        "Pour the prepared teriyaki sauce into the skillet and stir continuously until it begins to thicken.",
        "Return the shrimp to the skillet and toss until the shrimp and vegetables are evenly coated in the sauce.",
        "Serve over the cooked jasmine rice and garnish with sliced green onions and sesame seeds.",
    ],
    "notes": [],
    "items": [
        {"ingredient": SHRIMP, "serving": 1},
        {"ingredient": JASMINE_RICE, "serving": 1},
        {"ingredient": BELL_PEPPERS, "serving": 1},
        {"ingredient": ONIONS, "serving": 1},
        {"ingredient": GARLIC, "serving": 2},
        {"ingredient": GINGER, "serving": 2},
        {"ingredient": LOW_SODIUM_SOY_SAUCE, "serving": 2},
        {"ingredient": HONEY, "serving": 0.5},
        {"ingredient": RICE_VINEGAR, "serving": 2},
        {"ingredient": CORNSTARCH, "serving": 2},
        {"ingredient": SESAME_SEEDS, "serving": 1},
        {"ingredient": GREEN_ONIONS, "serving": 1},
    ],
}

BBQ_CHICKEN_FLATBREAD_PIZZA = {
    "title": "BBQ Chicken Flatbread Pizza",
    "category": "dinner",
    "cuisine": "american",
    "source": "website",
    "restaurant": "",
    "recipe_link": "https://xoxobella.com/bacon-onion-and-bbq-chicken-flatbread-pizza/",
    "image_url": "https://xoxobella.com/wp-content/uploads/2021/04/BBQ_Chicken_Flatbread_Pizzas.jpg",
    "prep_time": 10,
    "cook_time": 20,
    "servings": 1,
    "tags": ["high protein"],
    "overview": (
        "A crispy whole wheat pita topped with BBQ chicken, melted mozzarella, "
        "red onion, and fresh cilantro. This quick, high-protein flatbread pizza "
        "delivers classic barbecue pizza flavors in a lighter, weeknight-friendly meal."
    ),
    "instructions": [
        "Preheat the oven to 400°F (200°C).",
        "Season the chicken breast with salt, black pepper, garlic powder, and smoked paprika.",
        "Heat a skillet over medium heat and cook the chicken until golden on the outside and cooked through, about 5 to 7 minutes per side depending on thickness. Let it rest for 5 minutes, then slice or shred into bite-sized pieces.",
        "Place the whole wheat pita on a baking sheet or pizza pan.",
        "Spread the BBQ sauce evenly over the pita, leaving a small border around the edge.",
        "Top with the cooked chicken, followed by the low-fat mozzarella and thinly sliced red onion.",
        "Bake for 8 to 10 minutes, or until the cheese is melted and bubbly and the edges of the pita are lightly crisp.",
        "Remove from the oven and garnish with fresh cilantro before serving.",
    ],
    "notes": [],
    "items": [
        {"ingredient": WHOLE_WHEAT_PITA, "serving": 1},
        {"ingredient": CHICKEN_BREAST, "serving": 1},
        {"ingredient": LOW_FAT_MOZZARELLA, "serving": 1},
        {"ingredient": BBQ_SAUCE, "serving": 1},
        {"ingredient": RED_ONION, "serving": 0.1},
        {"ingredient": CILANTRO, "serving": 1},
    ],
}

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
        {"ingredient": LOW_SODIUM_SOY_SAUCE, "serving": 0.33},
        {"ingredient": RICE_VINEGAR, "serving": 0.33},
        {"ingredient": GOCHUJANG, "serving": 0.33},
        {"ingredient": GREEN_ONIONS, "serving": 1},
        {"ingredient": SESAME_SEEDS, "serving": 0.5},
    ],
}