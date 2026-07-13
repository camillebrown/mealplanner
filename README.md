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

### 1. Create a blank meal-plan page in Notion

Open the Meal Plans database and use the blue **New** button to create a page from the configured meal-plan template.

Leave the page's title, Start date, and End date empty. The initialization script fills those values automatically.

---

### 2. Create the weekly meal-plan file

Create a new file inside:

```text
meal_plans/
```

The filename identifies the first day of the week.

Example:

```text
meal_plans/july_20_2026.py
```

To reuse an existing plan as a starting point:

```bash
cp meal_plans/july_13_2026.py meal_plans/july_20_2026.py
```

Edit the copied file as needed before populating Notion.

Each day may include:

- Breakfast
- Lunch
- Dinner
- Snack

Recipes can be referenced directly:

```python
"Saturday": {
    "Breakfast": BREAKFAST_BURRITO,
    "Lunch": TURKEY_LETTUCE_WRAPS,
    "Dinner": BBQ_CHICKEN_FLATBREAD_PIZZA,
    "Snack": SPICY_ASIAN_CUCUMBER_TUNA_SALAD,
},
```

Recipes and individual ingredients can also be combined:

```python
"Tuesday": {
    "Breakfast": {
        "title": "Breakfast Bake & Apples",
        "items": [
            BREAKFAST_BAKE,
            {"ingredient": APPLES, "serving": 0.75},
        ],
    },
},
```

Multiple recipes can be combined into one meal:

```python
"Wednesday": {
    "Breakfast": {
        "title": "Stewed Apples with Ratio Yogurt + Protein Coffee",
        "items": [
            STEWED_APPLES_AND_YOGURT,
            PROTEIN_COFFEE,
        ],
    },
},
```

---

### 3. Initialize the blank Notion page

Run:

```bash
python3 initialize_new_page.py july_20_2026
```

The argument must match the meal-plan filename without `.py`.

For example:

```text
meal_plans/july_20_2026.py
```

uses:

```bash
python3 initialize_new_page.py july_20_2026
```

The script automatically:

- Verifies that the meal-plan file exists.
- Finds the newest blank page in the Meal Plans database.
- Derives the start date from the meal-plan name.
- Calculates the remaining six days of the week.
- Sets the page title.
- Sets the Start and End dates.

---

### 4. Choose how much of the plan to populate

#### Populate one meal

Use this while creating or changing one meal:

```bash
python3 -m setters.set_meal july_20_2026 Monday Breakfast
```

This updates:

- Meal heading
- Recipe-page link
- Ingredients
- Meal totals
- Daily totals

---

#### Populate one day

Use this after completing all meals for one day:

```bash
python3 -m setters.set_day july_20_2026 Monday
```

This updates:

- Every meal for the selected day
- Daily totals
- Weekly totals and averages
- Grocery list

An omitted meal, such as Snack, keeps its section and table in Notion. The script clears unused ingredient rows and resets that meal's total.

---

#### Populate the full week

Use this after the entire weekly plan is ready:

```bash
python3 -m setters.set_week july_20_2026
```

This updates:

- Every meal
- Every day
- Recipe-page links
- Daily totals
- Weekly totals and averages
- Grocery list
- Recipe Last Planned and Next Planned dates

---

### Initialize and populate the full week in one command

Once the meal-plan file is complete and a blank Notion page exists, run:

```bash
python3 initialize_and_fill_week.py july_20_2026
```

This is equivalent to running:

```bash
python3 initialize_new_page.py july_20_2026
python3 -m setters.set_week july_20_2026
```

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

### Apply Recipe Dates

Recalculates the **Last Planned** and **Next Planned** properties in the Recipe Database from every file in `meal_plans/`.

```bash
python3 -m recipes.recipe_actions.apply_recipe_dates
```

This normally runs automatically at the end of `set_week`, but it can also be run independently after renaming, copying, or editing meal-plan files.

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