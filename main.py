import os
import logging
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from notion_client import Client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

notion = Client(auth=NOTION_API_KEY)


def get_gfg_puzzles():

    GFG_URL = "https://www.geeksforgeeks.org/aptitude/top-100-puzzles-asked-in-interviews/"
    
    logging.info(f"Fetching puzzles from {GFG_URL}...")
    puzzles_list = []
    
    try:
        page = requests.get(GFG_URL, headers={"User-Agent": "Mozilla/5.0"})
        page.raise_for_status() 
        
        soup = BeautifulSoup(page.content, "html.parser")

        all_text_divs = soup.find_all("div", class_="text") 
        
        for text_div in all_text_divs:

            all_tables = text_div.find_all("table") 
            
            if not all_tables:
                logging.info("A 'text' div was found, but it contained no tables. Skipping.")
                continue # Skip to the next 'text' div

            
            for table in all_tables:
                table_rows = table.find_all("tr")
                
                for row in table_rows:
                    
                    link_tag = row.find("a") 
                    
                    if link_tag and link_tag.has_attr('href'):
                        title = link_tag.get_text().strip() 
                        url = link_tag['href']
                        
                        if not url.startswith("http"):
                            url = f"https://www.geeksforgeeks.org{url}"
                            
                        puzzles_list.append({
                            "title": title,
                            "url": url
                        })

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching GFG page: {e}")
        return []
    
   #removing duplicate puzzles
    unique_puzzles = list({p['url']: p for p in puzzles_list}.values())
    
    logging.info(f"Found {len(unique_puzzles)} unique puzzles across all tables.")
    return unique_puzzles


def add_puzzle_to_notion(title, url):
    
    logging.info(f"Adding puzzle to Notion: {title}")
    
    new_page_properties = {
        "Puzzle Title": {
            "title": [{"text": {"content": title}}]
        },
        "URL": {
            "url": url
        },
        "Done": {
            "checkbox": False 
        }
    }
    
    try:
        notion.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties=new_page_properties
        )
    except Exception as e:
        if "not found" in str(e) or "does not exist" in str(e):
             logging.error(f"Error: A property in your script does not match your Notion database.")
             logging.error(f"Check Notion for: 'Puzzle Title', 'URL', and 'Done' (Checkbox)")
        else:
            logging.error(f"Error adding page to Notion: {e}")


if __name__ == "__main__":
    logging.info("Starting GFG to Notion scraper...")
    
    if not NOTION_API_KEY or not NOTION_DATABASE_ID:
        logging.error("Notion API Key or Database ID not found in .env file. Exiting.")
    else:
        all_puzzles = get_gfg_puzzles()
        
        if not all_puzzles:
            logging.warning("No puzzles found. Check scraper function or GFG page.")
        else:
            logging.info(f"Starting to add {len(all_puzzles)} puzzles to Notion...")
            
            for puzzle in all_puzzles:
                add_puzzle_to_notion(puzzle["title"], puzzle["url"])
                
                time.sleep(1) 
                
            logging.info("Successfully added all puzzles. Script complete.")