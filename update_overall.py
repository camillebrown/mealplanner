import json
import subprocess

from calculators.calculate_overall import calculate_overall


if __name__ == "__main__":
    result = calculate_overall()

    pretty = json.dumps(result, indent=2)
    print(pretty)
    subprocess.run(["pbcopy"], input=pretty.encode())
    print("\n✅ Copied to clipboard")