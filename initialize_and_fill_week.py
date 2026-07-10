import json
import subprocess
import sys

from initialize_new_page import main as create_page_main
from setters.set_week import set_week


def run(start_date, plan_name):
    create_page_main(start_date)
    week_result = set_week(plan_name)

    return {
        "success": True,
        "start_date": start_date,
        "plan": plan_name,
        "week_result": week_result,
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 run.py 2026-07-13 july_13_2026")
        sys.exit(1)

    result = run(sys.argv[1], sys.argv[2])

    pretty = json.dumps(result, indent=2)
    print(pretty)
    subprocess.run(["pbcopy"], input=pretty.encode())
    print("\n✅ Copied to clipboard")