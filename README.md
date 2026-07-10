# Meal Planner

## Objective

Automatically create and update weekly meal plans in Notion. This project includes the following:

- Weekly meal plan configuration
- Master List of Ingredients (including macros)
- Day, Week, and Overall Calculators
- Automated Grocery List compilation with totals
- Setters for individual meals, full days and full weeks

Plan out what you want to eat throughout the week and this project will make tracking your goals quick and easy.

## Project Structure

```
mealplanner/
│
├── calculators/
│   ├── calculate_day.py
│   ├── calculate_week.py
│   └── calculate_overall.py
│
├── setters/
│   ├── set_meal.py
│   ├── set_day.py
│   ├── set_week.py
│   └── set_grocery_list.py
│
├── recipes/
│   ├── __init__.py
│   └── recipes.py
│
├── recipe_actions/
│   ├── __init__.py
│   ├── import_recipe.py
│   ├── export_recipes.py
│   ├── validate_recipes.py
│   └── inspect_recipe.py
│
├── meals/
│   ├── __init__.py
│   └── july_13_2026.py
│
├── ingredients.py
├── constants.py
├── notion.py
├── config.py
│
├── initialize_new_page.py
├── initialize_and_fill_week.py
├── recalculate_totals.py
├── update_groceries.py
└── update_overall.py
```

## New Meal Plan Workflow

### 1. Create a new empty page in Notion

Use the blue "New" button in the Notion UI to create a new meal plan page that will automatically be added to the Summary Database.

---

### 2. Create a new meal plan page

Create a new file inside:

```
meal_plans/
```

Example:

```
meal_plans/july_13_2026.py
```

Each day should include Breakfast, Lunch, and Dinner with an optional Snack.

Each meal supports the following properties:

| Property | Required | Description | Example |
|----------|----------|-------------|---------|
| `title` | ✅ Yes | Display name shown in Notion. | `"Sticky Sweet Chili Beef Bowl"` |
| `recipe_link` | ❌ No | URL linked from the meal title in Notion. | `"https://..."` |
| `items` | ✅ Yes | List of ingredients and servings used in the meal. | `[{"ingredient": GROUND_BEEF, "serving": 1}]` |

Each item within `items` supports:

| Property | Required | Description | Example |
|----------|----------|-------------|---------|
| `ingredient` | ✅ Yes | Ingredient object imported from `ingredients.py`. | `GROUND_BEEF` |
| `serving` | ✅ Yes | Multiplier applied to the ingredient's serving size and macros. Can be a whole number or decimal. | `1`, `0.5`, `2` |

Example structure:

```python
"Monday": {
    "Breakfast": {
        "title": "Cottage Cheese Breakfast Tacos",
        "recipe_link": "https://www.tiktok.com/t/ZTSC3Uwxk/",
        "items": [
            {"ingredient": LOW_FAT_COTTAGE_CHEESE, "serving": 4},
            {"ingredient": LIQUID_EGG_WHITES, "serving": 0.3},
            ...
        ],
    },

    "Lunch": {
        "title": "Wildbird Boneless Breast Marketplace",
        "items": [
            {"ingredient": WILDBIRD_BONELESS_BREAST_MARKET_PLATE, "serving": 1},
        ],
    },

    "Dinner": {
        "title": "Sticky Sweet Chili Beef Bowl",
        "recipe_link": "https://www.tiktok.com/t/ZTSCcuoPK/",
        "items": [
            {"ingredient": GROUND_BEEF, "serving": 1},
            {"ingredient": JASMINE_RICE, "serving": 1},
            ...
        ],
    },
    "Snack": {
        "title": "Ratio Yogurt Parfait",
        "items": [
            {"ingredient": PROTEIN_YOGURT, "serving": 1},
            {"ingredient": KIWIS, "serving": 1},
            ...
        ],
    },
},
```

---

### 3. Initialize the new Notion meal plan page

```bash
python3 initialize_new_page.py 2026-07-13
```

> 💡 **NOTE**:
> The date passed to `initialize_new_page.py` **must be the first day of the meal plan week** (typically Monday).
>
> The script automatically:
> - Calculates the remaining 6 days of the week.
> - Names the Notion page (e.g. **July 13–19, 2026**).
> - Sets the page's **Start** and **End** dates.
> - Creates the page in the Summary database from the configured Notion template.

---

### 4. Choose your population strategy

Depending on how you're planning your meals, you can populate a single meal, an entire day, or the entire week.

#### Option 1 — Populate a Single Meal

Use this while actively planning or tweaking an individual meal.

```bash
python3 -m setters.set_meal july_13_2026 Monday Breakfast
```

Automatically updates:

- Meal heading and recipe link
- Meal ingredients
- Meal totals
- Daily totals

---

#### Option 2 — Populate a Single Day

Use this after finishing all meals for a day.

```bash
python3 -m setters.set_day july_13_2026 Monday
```

Automatically updates:

- All meals for the day
- Daily totals
- Weekly totals and averages
- Grocery list

Meals omitted from the meal plan (such as an optional Snack), automatically clean up that meal's table in the Notion page.

---

#### Option 3 — Populate the Entire Week

Use this after completing the full meal plan.

```bash
python3 -m setters.set_week july_13_2026
```

Automatically updates:

- Every meal
- Every day
- Weekly totals and averages
- Grocery list

---

## Useful Helpers

The following scripts can be run independently to update or verify specific parts of the meal plan without repopulating meals.

---

### Create + Populate a New Week

If starting from scratch, this convenience script creates the new Notion page and immediately populates it using the specified meal plan.

```bash
python3 initialize_and_fill_week.py 2026-07-13 july_13_2026
```

Equivalent to running:

1. `initialize_new_page.py`
2. `set_week.py`

---

### Recalculate Totals

Use this after changing nutritional information in `ingredients.py`.

This recalculates all daily and weekly totals without modifying any meal contents.

```bash
python3 recalculate_totals.py july_13_2026
```

Updates:

- Daily totals
- Weekly averages
- Difference tables

---

### Update Grocery List

Use this after:

- Adding or removing meals from the meal plan.
- Changing ingredient serving quantities.
- Adding, removing, or renaming ingredients.
- Changing an ingredient's grocery category.

```bash
python3 update_groceries.py july_13_2026
```

Only the grocery list is updated.

---

### Update Overall Historical Averages

Use this once a week's meal plan is considered complete and should contribute to long-term statistics.

```bash
python3 update_overall.py
```

This updates the **📊 Overall Average vs. Goal** table on the parent Meal Plans page.

> 💡 **NOTE**:
>
> This script is intentionally **manual**. Partially planned weeks (vacations, eating out, incomplete meal plans, etc.) should not influence long-term averages until they accurately represent a typical week.

---

## Ingredients

All ingredients are defined in:

```
ingredients.py
```

The ingredient list serves as the single source of truth for the entire project.

Every meal is built from ingredients, and every calculation throughout the application is derived from the nutritional information defined here. Updating an ingredient automatically affects any meal that uses it the next time the meal or totals are recalculated.

Each ingredient contains:

```python
{
    "name": "...",
    "category": "...",
    "serving_size": "...",
    "calories": ...,
    "protein": ...,
    "fat": ...,
    "carbs": ...,
    "fiber": ...,
}
```

### How Ingredients Are Used

Each ingredient property is used throughout the project:

**Nutritional calculations**: Meal totals, daily totals, weekly averages, and overall historical averages.

| Property | Purpose |
|----------|---------|
| `name` | Displayed in meal tables and the grocery list. |
| `category` | Determines which grocery list section the ingredient belongs to. |
| `serving_size` | Used to calculate and display the total quantity needed based on the serving multiplier defined in a meal plan. |
| `calories` | Used in all nutritional calculations. |
| `protein` | Used in all nutritional calculations. |
| `fat` | Used in all nutritional calculations. |
| `carbs` | Used in all nutritional calculations. |
| `fiber` | Used in all nutritional calculations. |

For example, if an ingredient has a serving size of **30 g** and is used with a serving multiplier of **2**, the meal will display **60 g**, the grocery list will accumulate **60 g**, and all nutritional values will be doubled automatically.

> 💡 **IMPORTANT**:
>
> Changes to an ingredient do **not** immediately update existing Notion pages. After modifying nutritional information, run the appropriate setter or helper scripts to recalculate the affected meals, days, or weeks.

---

## Recipes

Reusable recipes are defined in:

```text
recipes/recipes.py
```

Recipes are reusable building blocks for meal plans. Each recipe follows the same structure as a meal within a weekly meal plan and contains its own title, optional recipe link, and list of ingredients.

For example:

```python
STICKY_SWEET_CHILI_BEEF_BOWL = {
    "title": "Sticky Sweet Chili Beef Bowl",
    "recipe_link": "https://www.tiktok.com/t/ZTSCcuoPK/",
    "items": [
        {"ingredient": GROUND_BEEF, "serving": 1},
        {"ingredient": JASMINE_RICE, "serving": 1},
        {"ingredient": BELL_PEPPERS, "serving": 0.5},
        ...
    ],
}
```

Recipes can then be reused directly throughout any weekly meal plan.

```python
"Dinner": STICKY_SWEET_CHILI_BEEF_BOWL
```

Meal plans can also customize or extend a recipe without modifying the original recipe definition.

For example:

```python
"Breakfast": {
    "title": "Cottage Cheese Breakfast Tacos with Berries",
    "recipe_link": COTTAGE_CHEESE_BREAKFAST_TACOS["recipe_link"],
    "items": [
        *COTTAGE_CHEESE_BREAKFAST_TACOS["items"],
        {"ingredient": MIXED_BERRIES, "serving": 1},
    ],
}
```

This approach keeps commonly used meals defined in a single place while still allowing each week's meal plan to make adjustments as needed.

Recipes inherit all nutritional information from the ingredients they reference. As a result, updating an ingredient automatically affects every recipe that uses it the next time meal totals or weekly totals are recalculated.

---

### Grocery Categories

Each ingredient belongs to a grocery category.

Current categories are:

- proteins
- dairy
- frozen products
- grains & starches
- produce
- pantry, canned goods & condiments

The grocery list is generated automatically from the current meal plan.

For every ingredient used throughout the week, the script:

1. Groups ingredients by their `category`.
2. Combines duplicate ingredients across all meals and days.
3. Calculates the total quantity required using the ingredient's `serving_size` and meal plan serving multiplier.
4. Populates the matching grocery table in the Notion page.

For example:

- Monday Breakfast: Cottage Cheese × 30 g
- Thursday Lunch: Cottage Cheese × 45 g

becomes:

- **Low-Fat Cottage Cheese — 75 g**

> 💡 **NOTE**: 
>
> If an ingredient references a category that does not exist in the Notion template, the script reports the missing category instead of silently skipping the ingredient. This makes it easy to identify new grocery sections that need to be added to the Notion template.

---