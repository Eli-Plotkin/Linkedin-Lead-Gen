from src.scrape_profiles import scrapeProfiles
from dotenv import load_dotenv
import os

load_dotenv()

def test_scrape_profiles():
    sp = scrapeProfiles()
    sp.export_scraped_data(email=os.getenv('MY_LINKEDIN_EMAIL_ADDRESS'), 
                    password=os.getenv('MY_LINKEDIN_PASSWORD'),
                    post_link=os.getenv('MY_POST_LINK'))