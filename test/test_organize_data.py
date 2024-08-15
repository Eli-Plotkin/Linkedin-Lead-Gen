from src.organize_data import organizeData
from dotenv import load_dotenv
import os

load_dotenv()

def test_organize_data():
    od = organizeData()
    od.export_organized_data(csvFile='scraped_profiles.csv', 
                             email=os.getenv('MY_LINKEDIN_EMAIL_ADDRESS'), 
                             password=os.getenv('MY_LINKEDIN_PASSWORD'),
                             is_test_data=True)
