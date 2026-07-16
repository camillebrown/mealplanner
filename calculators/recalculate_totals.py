import json
import subprocess
import sys

from calculators.calculate_day import calculate_day
from calculators.calculate_week import calculate_week
from constants import DAYS
from setters.set_meal import load_meal_plan


def recalculate(plan_name):
    meal_plan = load_meal_plan(plan_name)

    days = []
    for day in DAYS:
        if day in meal_plan:
            result = calculate_day(plan_name, day)
            days.append(result)
            print(f"✅ {day} totals recalculated")

    week = calculate_week(plan_name)
    print("✅ Weekly averages recalculated")

    return {
        "success": True,
        "plan": plan_name,
        "days_recalculated": [d["day"] for d in days],
        "week_totals": week,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 recalculate.py july_13_2026")
        sys.exit(1)

    result = recalculate(sys.argv[1])

    pretty = json.dumps(result, indent=2)
    print(pretty)
    subprocess.run(["pbcopy"], input=pretty.encode())
    print("\n✅ Copied to clipboard")