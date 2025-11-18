GFG Puzzle Scraper → Notion Automation

This script scrapes all puzzle links from the GeeksforGeeks page
“Top 100 Puzzles Asked in Interviews”
and automatically adds them into a Notion database via the Notion API.

Features

Scrapes puzzle titles and URLs from GFG.

Cleans and removes duplicate entries.

Creates a Notion database page for each puzzle with:

Puzzle Title (Title property)

URL (URL property)

Done (Checkbox)

Includes logging and error handling.

Uses .env for secure API credentials.

Requirements
Python Packages

Install dependencies:

pip install requests beautifulsoup4 python-dotenv notion-client

Environment Variables

Create a .env file:

NOTION_API_KEY=your-secret-api-key
NOTION_DATABASE_ID=your-database-id

Notion Database Setup

Your Notion database must contain these properties:

Property Name	Type
Puzzle Title	Title
URL	URL
Done	Checkbox
How It Works
1. Scrapes the GFG Puzzle Page

The script fetches:

https://www.geeksforgeeks.org/aptitude/top-100-puzzles-asked-in-interviews/


Then extracts puzzle titles and URLs from all tables inside <div class="text">.

2. Removes Duplicate Links

URLs are used as unique keys.

3. Pushes Each Puzzle to Notion

Each puzzle is added as a page in your database with a 1-second delay to avoid hitting Notion’s rate limits.

Running the Script
python main.py


You will see logs such as:

INFO - Fetching puzzles...
INFO - Found 95 unique puzzles
INFO - Adding puzzle to Notion: Example Puzzle

File Structure
project/
│
├── main.py
├── .env
└── README.md

Logging

The script uses Python's logging module for progress updates and error reporting.

Troubleshooting
1. Incorrect Property Names

If you see:

Error: A property in your script does not match your Notion database.


Verify that Notion contains exactly:

Puzzle Title (Title)

URL (URL)

Done (Checkbox)

2. Notion credentials not found

Ensure .env exists and keys are correct.
