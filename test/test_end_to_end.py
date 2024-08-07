from src.organize_data import organizeData
from src.scrape_profiles import scrape_profiles

def test_end_to_end():
    sp = scrape_profiles()
    sp.sign_in(email="aeplotkin@gmail.com", password="MonkeyMilo1")
    sp.export_data(post_link="https://www.linkedin.com/feed/update/urn:li:activity:7223719016920485889/")
    od = organizeData()
    od.export_organized_data(csvFile='scraped_profiles.csv', 
                             email="aeplotkin@gmail.com", 
                             password="MonkeyMilo1",
                             is_test_data=False)