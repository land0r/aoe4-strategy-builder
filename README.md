# Age of Wonders 4 Wiki Scraper

This Python script downloads (scrapes) all articles from the Age of Wonders 4 Wiki (hosted on [paradoxwikis.com](https://aow4.paradoxwikis.com/)), stores them locally as `.txt` files, merges them into a single file, and logs the entire operation. It also skips redirects and provides final statistics about how many articles were processed and how many were skipped.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Example Workflow with ChatGPT](#example-workflow-with-chatgpt)
  - [Example Prompt for ChatGPT](#example-prompt-for-chatgpt)
- [Step-by-Step Instructions](#step-by-step-instructions)

## Features
1. **Full folder cleanup** before scraping (deletes and recreates the `wiki_dump` folder).
2. **Fetches all article titles** from the MediaWiki API.
3. **Skips redirects** (detected by `#redirect` in the content).
4. **Logs** all operations to `scraper.log`.
5. **Combines** all downloaded text files into one (`aoe4-wiki.txt`) and **counts words**.
6. **Uses a custom User-Agent** to reduce the chance of being blocked.

## Prerequisites
- **Python 3.7+** installed.
- A package manager such as **pip**.
- **requests** library (`pip install requests`).
- (Optional) A virtual environment is recommended but not required.

## Usage
1. **Clone or download** this repository.
2. **Install dependencies**:  
   ```bash
   pip install requests
   ```
3. **Run the script**:
   ```bash
   python wiki_scraper.py
   ```
4. **Check the results**:
    - Logs are in `scraper.log`.
    - Individual `.txt` files are in `wiki_dump/`.
    - A combined file named `aoe4-wiki.txt` is also in `wiki_dump/`, containing the merged content of all `.txt` files.

## Example Workflow with ChatGPT
To have ChatGPT analyze the scraped wiki data and generate builds or strategies solely based on that data, consider using **ChatGPT’s Advanced Data Analysis** feature (if you have ChatGPT Plus) or another method of providing these text files to ChatGPT.

### Example Prompt for ChatGPT

Below is a sample prompt you might use within ChatGPT’s **Advanced Data Analysis** (formerly Code Interpreter) session:

```
You are an expert on Age of Wonders 4. You have ONE source of knowledge: a file (or set of files) containing a Wikipedia dump for Age of Wonders 4. This file holds all relevant information about the game’s mechanics, factions, races, abilities, resources, buildings, units, spells, etc.

Your tasks:
1) Analyze ONLY the contents of the uploaded file, without inventing or adding unverified information.
2) If the requested data is not found in the file, explicitly state that the file does not contain such information.
3) Generate in-game development strategies (builds) for Age of Wonders 4, using facts and data from the file.
4) Whenever possible, reference the corresponding sections/fragments in the file (if the wiki dump shows explicit headings or sections).
5) Provide detailed descriptions of the strategies: which factions to choose, which skills or magic tomes to develop, which buildings to construct and in what order, which resources are crucial and why.

Key requirements:
- Do not fabricate facts outside the file.
- If multiple versions of the same info (e.g. various patches) exist, reference the most up-to-date data from the file.
- If a user asks about something that does not appear in the file, say that the information is not present.

Let’s begin with analyzing the database. First, please confirm that you have access to the uploaded file and can extract the necessary Age of Wonders 4 details from it. Then, list the main categories of information you found (for example, about cultures, races, skills, units, buildings, etc.).
```

## Step-by-Step Instructions

1. **Set up the environment**
    - Make sure you have Python 3.7 or higher.
    - (Optional) Create and activate a virtual environment:
      ```bash
      python -m venv venv
      source venv/bin/activate
      ```
    - Install dependencies:
      ```bash
      pip install requests
      ```

2. **Download or copy the scraper script**
    - Place `wiki_scraper.py` in an empty folder (or the folder of your choice).

3. **Run the script**
   ```bash
   python wiki_scraper.py
   ```
    - The script will:
        - Remove and recreate `wiki_dump/`
        - Fetch all article titles from `aow4.paradoxwikis.com`
        - Skip pages that are redirects
        - Save each article as a `.txt` file in `wiki_dump/`
        - Create a `scraper.log` with detailed logs
        - Merge all `.txt` files into `aoe4-wiki.txt`
        - Log the total word count of `aoe4-wiki.txt`

4. **Review the output**
    - Open `scraper.log` to see the logged process:
        - How many pages were found
        - Which pages were processed
        - Which were skipped due to redirects
    - Inspect the `wiki_dump/` folder to see all individual `.txt` files.
    - Check `wiki_dump/aoe4-wiki.txt` for the full merged text of all articles, plus the word count is logged at the end of `scraper.log`.

5. **Use the data with ChatGPT**
    - If using **Advanced Data Analysis**, open that feature in ChatGPT.
    - Click “Upload File” (typically found in the left panel).
    - Upload `aoe4-wiki.txt` (or the entire folder zipped).
    - Provide a prompt (see [Example Prompt for ChatGPT](#example-prompt-for-chatgpt)) instructing ChatGPT to reference only that file.
    - Ask your questions about Age of Wonders 4 builds, referencing your newly obtained data.

6. **Iterate and refine**
    - If you need to update the wiki dump in the future, run `wiki_scraper.py` again.
    - If you want to skip or keep certain pages, adjust the logic in the script.
    - For more advanced usage (like searching or chunking large text), consider additional tools or prompt-engineering.

---

**That’s it!** You now have a functional workflow for scraping the Age of Wonders 4 Wiki and using ChatGPT to answer questions or generate strategies based on **only** that scraped data.