from src.organize_data import organizeData
from src.scrape_profiles import scrape_profiles

def test_end_to_end():
    sp = scrape_profiles()
    sp.export_data(email="aeplotkin@gmail.com", 
                    password="MonkeyMilo1",
                    post_link="https://www.linkedin.com/posts/brighthire_2019-2024-happy-5th-activity-7217181041768243200-OcfH?utm_source=share&utm_medium=member_desktop")
    od = organizeData()
    od.export_organized_data(csvFile='scraped_profiles.csv', 
                             email="aeplotkin@gmail.com", 
                             password="MonkeyMilo1",
                             is_test_data=False)