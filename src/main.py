from scrape_profiles import scrapeProfiles
from organize_data import organizeData
from dotenv import load_dotenv
import os

load_dotenv()

sp = scrapeProfiles()
if sp.export_scraped_data(email=os.getenv("MY_LINKEDIN_EMAIL_ADDRESS"), 
                          password=os.getenv("MY_LINKEDIN_PASSWORD"),
                          post_link=os.getenv("MY_POST_LINK")):
    od = organizeData()
    od.export_organized_data(csvFile='scraped_profiles.csv', 
                             email=os.getenv("MY_LINKEDIN_EMAIL_ADDRESS"), 
                             password=os.getenv("MY_LINKEDIN_PASSWORD"),
                             is_test_data=False)