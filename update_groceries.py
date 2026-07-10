import json
import subprocess
import sys

from setters.set_grocery_list import update_grocery_list


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 update_groceries.py july_13_2026")
        sys.exit(1)

    result = update_grocery_list(sys.argv[1])

    pretty = json.dumps(result, indent=2)
    print(pretty)
    subprocess.run(["pbcopy"], input=pretty.encode())
    print("\n✅ Copied to clipboard")