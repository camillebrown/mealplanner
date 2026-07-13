import json
import subprocess
import sys

from initialize_new_page import main as initialize_page
from setters.set_week import set_week


def run(plan_name):
    page_result = initialize_page(plan_name)
    week_result = set_week(plan_name)

    return {
        "success": True,
        "plan": plan_name,
        "page_result": page_result,
        "week_result": week_result,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 initialize_and_fill_week.py july_20_2026")
        sys.exit(1)

    result = run(sys.argv[1])

    pretty = json.dumps(result, indent=2)
    print(pretty)
    subprocess.run(["pbcopy"], input=pretty.encode())
    print("\n✅ Copied to clipboard")