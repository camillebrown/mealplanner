import json

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0 Safari/537.36"
    )
}


def fetch_tiktok_page(url):
    """
    Downloads a TikTok page and returns the response and parsed HTML.
    """
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
        allow_redirects=True,
    )
    response.raise_for_status()

    document = BeautifulSoup(
        response.text,
        "html.parser",
    )

    return response, document

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0 Safari/537.36"
    )
}

def extract_tiktok_item(document):
    """
    Extracts TikTok's embedded itemStruct metadata from the page.

    Returns None when the expected metadata is not found.
    """
    for script in document.find_all("script"):
        raw = script.string or script.get_text()

        if not raw:
            continue

        raw = raw.strip()

        if not raw.startswith("{"):
            continue

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            continue

        default_scope = parsed.get("__DEFAULT_SCOPE__")

        if not default_scope:
            continue

        video_detail = default_scope.get(
            "webapp.video-detail"
        )

        if not video_detail:
            continue

        item_info = video_detail.get("itemInfo")

        if not item_info:
            continue

        item = item_info.get("itemStruct")

        if item:
            return item

    return None


def build_video_metadata(item):
    """
    Converts TikTok's raw itemStruct into the smaller video
    metadata object used by the inspector and generator.
    """
    video = item.get("video", {})
    author = item.get("author", {})

    return {
        "id": item.get("id"),
        "caption": item.get("desc", ""),
        "cover": video.get("cover", ""),
        "origin_cover": video.get(
            "originCover",
            "",
        ),
        "duration": video.get("duration"),
        "creator": author.get(
            "nickname",
            "",
        ),
        "username": author.get(
            "uniqueId",
            "",
        ),
        "hashtags": [
            challenge.get("title", "")
            for challenge in item.get(
                "challenges",
                [],
            )
            if challenge.get("title")
        ],
        "captions": video.get(
            "subtitleInfos",
            [],
        ),
    }


def read_tiktok_page(url):
    """
    Runs the full TikTok page-reading pipeline.

    Returns the response, parsed HTML, raw itemStruct, and
    simplified video metadata.
    """
    response, document = fetch_tiktok_page(url)

    item = extract_tiktok_item(document)

    if item is None:
        raise ValueError(
            "TikTok video metadata was not found in the page."
        )

    video = build_video_metadata(item)

    return {
        "response": response,
        "document": document,
        "item": item,
        "video": video,
    }
    
    