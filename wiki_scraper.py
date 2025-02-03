import requests
import time
import os
import re
import shutil

API_URL = "https://aow4.paradoxwikis.com/api.php"
OUTPUT_FOLDER = "wiki_dump"
LOG_FILE = "scraper.log"
COMBINED_FILENAME = "aoe4-wiki.txt"
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
    return re.sub(r'[^\w\s-]', '_', text).strip()

def clear_output_folder(folder_path, log_file):
    if os.path.exists(folder_path):
        log_file.write(f"Removing existing folder: {folder_path}\n")
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)
    log_file.write(f"Created empty folder: {folder_path}\n")

def fetch_all_page_titles(session, log_file):
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
            log_file.write("Failed to parse JSON for page titles.\n")
            log_file.write(f"Status code: {response.status_code}\n")
            log_file.write(f"Response text (snippet): {response.text[:300]}\n")
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

def fetch_page_content(session, title, log_file):
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
        log_file.write(f"Failed to parse JSON for page: {title}\n")
        log_file.write(f"Status code: {response.status_code}\n")
        log_file.write(f"Response text (snippet): {response.text[:300]}\n")
        return ""

    if "query" not in data or "pages" not in data["query"]:
        return ""

    pages_dict = data["query"]["pages"]
    for page_id, page_info in pages_dict.items():
        if "revisions" in page_info:
            return page_info["revisions"][0]["slots"]["main"].get("*", "")

    return ""

def combine_files_and_count_words(folder_path, combined_filename, log_file):
    combined_path = os.path.join(folder_path, combined_filename)

    with open(combined_path, "w", encoding="utf-8") as combined_file:
        for filename in os.listdir(folder_path):
            # Skip the combined file itself if it already exists
            if filename == combined_filename:
                continue
            full_path = os.path.join(folder_path, filename)
            if os.path.isfile(full_path) and filename.lower().endswith(".txt"):
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                combined_file.write(content + "\n")

    # Count words in the combined file
    with open(combined_path, "r", encoding="utf-8") as cf:
        text = cf.read()
    word_list = re.findall(r"\w+", text)
    word_count = len(word_list)
    log_file.write(f"Combined file: {combined_path}\n")
    log_file.write(f"Word count in combined file: {word_count}\n")

def main():
    with open(LOG_FILE, "w", encoding="utf-8") as log_file:
        clear_output_folder(OUTPUT_FOLDER, log_file)

        with requests.Session() as session:
            all_titles = fetch_all_page_titles(session, log_file)
            log_file.write(f"Found {len(all_titles)} pages in total.\n")
            print(f"Found {len(all_titles)} pages in total.")

            processed_count = 0
            skipped_count = 0

            for index, title in enumerate(all_titles, start=1):
                log_file.write(f"Processing page {index}/{len(all_titles)}: {title}\n")
                print(f"Processing page {index}/{len(all_titles)}: {title}")
                content = fetch_page_content(session, title, log_file)
                content_lower = content.strip().lower()

                if content_lower.startswith("#redirect"):
                    log_file.write(f"Skipping redirect page: {title}\n")
                    print(f"Skipping redirect page: {title}")
                    skipped_count += 1
                    time.sleep(SLEEP_BETWEEN_REQUESTS)
                    continue

                filename = sanitize_filename(title) + ".txt"
                filepath = os.path.join(OUTPUT_FOLDER, filename)

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

                log_file.write(f"Saved: {filepath}\n")
                print(f"Saved: {filepath}")
                processed_count += 1
                time.sleep(SLEEP_BETWEEN_REQUESTS)

            log_file.write(f"Finished. Processed: {processed_count}, Skipped redirects: {skipped_count}\n")
            print(f"\nFinished. Processed: {processed_count}, Skipped redirects: {skipped_count}")

            # Combine all .txt files and count words
            combine_files_and_count_words(OUTPUT_FOLDER, COMBINED_FILENAME, log_file)

if __name__ == "__main__":
    main()
