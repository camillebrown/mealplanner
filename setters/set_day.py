import json
import subprocess
import sys

from constants import MEALS
from setters.set_meal import clear_meal, load_meal_plan, set_meal
from calculators.calculate_week import calculate_week
from setters.set_grocery_list import update_grocery_list


def set_day(plan_name, day, update_week=True):
    meal_plan = load_meal_plan(plan_name)

    if day not in meal_plan:
        raise Exception(f"No meal plan found for {day}")

    updated = []

    for meal in MEALS:
        if meal in meal_plan[day]:
            updated.append(set_meal(plan_name, day, meal))
        else:
            updated.append(clear_meal(plan_name, day, meal))
            print(f"✅ {day} {meal} cleared")
            
    week_totals = None
    grocery_result = None

    if update_week:
        week_totals = calculate_week(plan_name)
        grocery_result = update_grocery_list(plan_name)
        
    print(f"✅ {day} complete")

    return {
        "success": True,
        "plan": plan_name,
        "day": day,
        "meals_updated": [item["meal"] for item in updated],
        "count": len(updated),
        "week_totals": week_totals,
        "grocery_result": grocery_result,
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 -m setters.set_day july_13_2026 Monday")
        sys.exit(1)

    result = set_day(sys.argv[1], sys.argv[2])

    pretty = json.dumps(result, indent=2)
    print(pretty)
    subprocess.run(["pbcopy"], input=pretty.encode())
    print("\n✅ Copied to clipboard")