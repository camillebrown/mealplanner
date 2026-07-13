import os

from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_VERSION = "2022-06-28"

SUMMARY_DATABASE_ID = "8bf4400d0f694059998a5faf3d4f285b"
RECIPE_DATABASE_ID = "2e3faf98d60283aeb203811865326801"