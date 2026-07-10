import json
import subprocess
import sys

from constants import DAYS
from setters.set_day import set_day
from setters.set_meal import load_meal_plan
from setters.set_grocery_list import update_grocery_list
from calculators.calculate_week import calculate_week


def set_week(plan_name):
    meal_plan = load_meal_plan(plan_name)

    updated = []

    for day in DAYS:
        if day in meal_plan:
            updated.append(set_day(plan_name, day, update_week=False))
            print(f"✅ {day} finished")

    week_totals = calculate_week(plan_name)
    grocery_result = update_grocery_list(plan_name)
    
    return {
        "success": True,
        "plan": plan_name,
        "days_updated": [item["day"] for item in updated],
        "count": len(updated),
        "week_totals": week_totals,
        "grocery_result": grocery_result,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 -m setters.set_week july_13_2026")
        sys.exit(1)

    result = set_week(sys.argv[1])

    pretty = json.dumps(result, indent=2)
    print(pretty)
    subprocess.run(["pbcopy"], input=pretty.encode())
    print("\n✅ Copied to clipboard")