import requests
import time
import os
import re
import shutil

API_URL = "https://aow4.paradoxwikis.com/api.php"
OUTPUT_FOLDER = "wiki_dump"
SLEEP_BETWEEN_REQUESTS = 0.2
PAGE_LIMIT = 500

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/88.0.4324.96 Safari/537.36"
    )
}

def sanitize_filename(text):
    # Replaces any character that is not alphanumeric, space, underscore, or dash
    # with an underscore
    return re.sub(r'[^\w\s-]', '_', text).strip()

def clear_output_folder(folder_path):
    # Completely remove the folder and re-create it
    if os.path.exists(folder_path):
        print(f"Removing existing folder: {folder_path}")
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)
    print(f"Created empty folder: {folder_path}")

def fetch_all_page_titles(session):
    titles = []
    apcontinue_value = None

    while True:
        params = {
            "action": "query",
            "list": "allpages",
            "aplimit": PAGE_LIMIT,
            "format": "json"
        }
        if apcontinue_value:
            params["apcontinue"] = apcontinue_value

        response = session.get(API_URL, params=params, headers=HEADERS)
        try:
            data = response.json()
        except Exception as e:
            print("Failed to parse JSON for page titles.")
            print("Status code:", response.status_code)
            print("Response text (snippet):", response.text[:300])
            raise e

        if "query" not in data or "allpages" not in data["query"]:
            break

        pages = data["query"]["allpages"]
        for p in pages:
            titles.append(p["title"])

        if "continue" in data:
            apcontinue_value = data["continue"]["apcontinue"]
            time.sleep(SLEEP_BETWEEN_REQUESTS)
        else:
            break

    return titles

def fetch_page_content(session, title):
    params = {
        "action": "query",
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "main",
        "titles": title,
        "format": "json"
    }
    response = session.get(API_URL, params=params, headers=HEADERS)
    try:
        data = response.json()
    except Exception as e:
        print(f"Failed to parse JSON for page: {title}")
        print("Status code:", response.status_code)
        print("Response text (snippet):", response.text[:300])
        return ""

    if "query" not in data or "pages" not in data["query"]:
        return ""

    pages_dict = data["query"]["pages"]
    for page_id, page_info in pages_dict.items():
        if "revisions" in page_info:
            return page_info["revisions"][0]["slots"]["main"].get("*", "")

    return ""

def main():
    # Clear (re-create) output folder
    clear_output_folder(OUTPUT_FOLDER)

    with requests.Session() as session:
        all_titles = fetch_all_page_titles(session)
        print(f"Found {len(all_titles)} pages in total.")

        processed_count = 0
        skipped_count = 0

        for index, title in enumerate(all_titles, start=1):
            print(f"Processing page {index}/{len(all_titles)}: {title}")
            content = fetch_page_content(session, title)
            content_lower = content.strip().lower()

            # Skip redirect pages
            # MediaWiki redirects often start with "#REDIRECT [[Some page]]"
            if content_lower.startswith("#redirect"):
                print(f"Skipping redirect page: {title}")
                skipped_count += 1
                time.sleep(SLEEP_BETWEEN_REQUESTS)
                continue

            filename = sanitize_filename(title) + ".txt"
            filepath = os.path.join(OUTPUT_FOLDER, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"Saved: {filepath}")
            processed_count += 1
            time.sleep(SLEEP_BETWEEN_REQUESTS)

        print(f"\nFinished. Processed: {processed_count}, Skipped redirects: {skipped_count}")

if __name__ == "__main__":
    main()
