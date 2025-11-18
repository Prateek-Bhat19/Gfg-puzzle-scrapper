Here is a clean **README.md** file in Markdown format.

---

# GFG Puzzle Scraper to Notion

This project automatically scrapes puzzle links from the GeeksforGeeks page **“Top 100 Puzzles Asked in Interviews”** and saves them into a Notion database using the Notion API.

---

## Features

* Scrapes puzzle titles and URLs from GFG.
* Removes duplicate entries.
* Inserts each puzzle into a Notion database.
* Uses a 1-second delay to avoid Notion rate limits.
* Includes clear logging and error handling.
* Uses `.env` for secure configuration.

---

## Technologies Used

* Python
* Requests
* BeautifulSoup4
* Notion API (`notion-client`)
* python-dotenv
* Logging

---

## Setup Instructions

### 1. Clone the project

```bash
git clone <your_repo_url>
cd <project_folder>
```

### 2. Install dependencies

```bash
pip install requests beautifulsoup4 python-dotenv notion-client
```

### 3. Create a `.env` file

```
NOTION_API_KEY=your_notion_secret_key
NOTION_DATABASE_ID=your_database_id
```

### 4. Configure your Notion database

Your Notion database must contain these properties:

| Property Name | Type     |
| ------------- | -------- |
| Puzzle Title  | Title    |
| URL           | URL      |
| Done          | Checkbox |

Make sure names match exactly.

---

## How the Script Works

### 1. Scrape puzzles

The script fetches:

```
https://www.geeksforgeeks.org/aptitude/top-100-puzzles-asked-in-interviews/
```

It extracts puzzle titles + URLs from tables inside `<div class="text">`.

### 2. Deduplicate

Removes repeated links based on URL.

### 3. Add puzzles to Notion

Each puzzle is added as a page with:

* Title → Puzzle Title
* URL → URL property
* Done → set to false
* Parent → Your database ID

### 4. Rate limiting

A `time.sleep(1)` prevents hitting Notion API limits.

---

## Running the Script

```bash
python main.py
```

Example log output:

```
INFO - Fetching puzzles...
INFO - Found 93 unique puzzles.
INFO - Adding puzzle to Notion: Ages Puzzle
INFO - Successfully added all puzzles. Script complete.
```

---

## Project Structure

```
/
├── main.py
├── README.md
└── .env
```

---

## Error Handling

### Missing Notion properties

If database property names don’t match:

```
Error: A property in your script does not match your Notion database.
```

Fix the property names in Notion.

### Missing environment variables

If `.env` is not set:

```
Notion API Key or Database ID not found in .env file.
```

Ensure `.env` is correctly created.

---