import json
import subprocess

from notion import get, post

DATABASE_ID = "2e3faf98-d602-83ae-b203-811865326801"


database = get(f"/databases/{DATABASE_ID}")

pages = post(
    f"/databases/{DATABASE_ID}/query",
    {
        "sorts": [
            {"timestamp": "created_time", "direction": "descending"}
        ],
        "page_size": 5,
    },
)

result = {
    "database": database,
    "sample_pages": pages.get("results", []),
}

pretty = json.dumps(result, indent=2)
print(pretty)
subprocess.run(["pbcopy"], input=pretty.encode())
print("\n✅ Copied to clipboard")