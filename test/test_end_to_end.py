from src.organize_data import organizeData
from src.scrape_profiles import scrapeProfiles

def test_end_to_end():
    sp = scrapeProfiles()
    if sp.export_scraped_data(email="aeplotkin@gmail.com", 
                    password="MonkeyMilo1",
                    post_link="https://www.linkedin.com/posts/brighthire_who-owns-interview-planning-the-recruiter-activity-7206335182633672704-FhWe?utm_source=share&utm_medium=member_desktop"):
        od = organizeData()
        od.export_organized_data(csvFile='scraped_profiles.csv', 
                             email="aeplotkin@gmail.com", 
                             password="MonkeyMilo1",
                             is_test_data=True)