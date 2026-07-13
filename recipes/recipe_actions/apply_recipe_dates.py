import importlib
import json
import pkgutil
import subprocess
from collections import defaultdict
from datetime import date, datetime, timedelta

from meal_plans.helpers import recipe_titles
from config import RECIPE_DATABASE_ID
from notion import patch, post

import meal_plans


DAY_OFFSETS = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}


def plan_start_date(plan_name):
    return datetime.strptime(
        plan_name.title(),
        "%B_%d_%Y",
    ).date()



def all_recipe_pages():
    pages = []
    cursor = None

    while True:
        payload = {
            "page_size": 100,
        }

        if cursor:
            payload["start_cursor"] = cursor

        data = post(
            f"/databases/{RECIPE_DATABASE_ID}/query",
            payload,
        )

        if not data or data.get("object") == "error":
            raise Exception(
                f"Failed to query Recipe Database: {data}"
            )

        pages.extend(data.get("results", []))

        if not data.get("has_more"):
            break

        cursor = data.get("next_cursor")

    return pages


def page_title(page):
    title_parts = page["properties"]["Recipe"]["title"]

    return "".join(
        part.get("plain_text", "")
        for part in title_parts
    )


def existing_date(page, property_name):
    value = page["properties"][property_name]["date"]

    if not value:
        return None

    return value.get("start")


def collect_planned_dates():
    planned_dates = defaultdict(list)

    for module_info in pkgutil.iter_modules(meal_plans.__path__):
        plan_name = module_info.name

        if plan_name.startswith("_"):
            continue

        try:
            start_date = plan_start_date(plan_name)
        except ValueError:
            print(
                f"⚠️ Skipping meal plan with unsupported filename: "
                f"{plan_name}.py"
            )
            continue

        module = importlib.import_module(
            f"meal_plans.{plan_name}"
        )

        meal_plan = module.MEAL_PLAN

        for day, meals in meal_plan.items():
            if day not in DAY_OFFSETS:
                continue

            scheduled_date = start_date + timedelta(
                days=DAY_OFFSETS[day]
            )

            for meal in meals.values():
                titles = recipe_titles(meal["items"])

                if not titles:
                    titles = [meal["title"]]
                    print(
                        f"⚠️ No nested recipe found: "
                        f"{plan_name}.py → {day} → {meal['title']}"
                    )

                for title in titles:
                    planned_dates[title].append(scheduled_date)

    return planned_dates


def calculated_dates(dates, today):
    previous_dates = [
        planned_date
        for planned_date in dates
        if planned_date < today
    ]

    upcoming_dates = [
        planned_date
        for planned_date in dates
        if planned_date >= today
    ]

    last_planned = (
        max(previous_dates).isoformat()
        if previous_dates
        else None
    )

    next_planned = (
        min(upcoming_dates).isoformat()
        if upcoming_dates
        else None
    )

    return last_planned, next_planned


def update_recipe_dates():
    today = date.today()
    planned_dates = collect_planned_dates()
    pages = all_recipe_pages()

    updated = []
    unchanged = []
    missing_in_notion = []

    notion_titles = {
        page_title(page)
        for page in pages
        if page_title(page)
    }

    for title in sorted(planned_dates):
        if title not in notion_titles:
            missing_in_notion.append(title)

    for page in pages:
        title = page_title(page)

        if not title:
            continue

        last_planned, next_planned = calculated_dates(
            planned_dates.get(title, []),
            today,
        )

        old_last = existing_date(page, "Last Planned")
        old_next = existing_date(page, "Next Planned")

        if old_last == last_planned and old_next == next_planned:
            unchanged.append(title)
            print(f"✅ Recipe dates unchanged: {title}")
            continue

        result = patch(
            f"/pages/{page['id']}",
            {
                "properties": {
                    "Last Planned": {
                        "date": (
                            {"start": last_planned}
                            if last_planned
                            else None
                        )
                    },
                    "Next Planned": {
                        "date": (
                            {"start": next_planned}
                            if next_planned
                            else None
                        )
                    },
                }
            },
        )

        if not result or result.get("object") == "error":
            raise Exception(
                f"Failed to update recipe dates for "
                f"'{title}': {result}"
            )

        updated.append(title)

        print(f"✅ Recipe dates updated: {title}")

        if old_last != last_planned:
            print(
                f"  • Last Planned: "
                f"{old_last or 'empty'} → "
                f"{last_planned or 'empty'}"
            )

        if old_next != next_planned:
            print(
                f"  • Next Planned: "
                f"{old_next or 'empty'} → "
                f"{next_planned or 'empty'}"
            )

    if missing_in_notion:
        print("\n⚠️ Planned recipes missing from Notion:")

        for title in missing_in_notion:
            print(f"  • {title}")

    return {
        "success": True,
        "updated": updated,
        "unchanged": unchanged,
        "missing_in_notion": missing_in_notion,
        "updated_count": len(updated),
        "unchanged_count": len(unchanged),
    }


if __name__ == "__main__":
    result = update_recipe_dates()

    pretty = json.dumps(result, indent=2)
    print(pretty)

    subprocess.run(
        ["pbcopy"],
        input=pretty.encode(),
    )

    print("\n✅ Copied to clipboard")