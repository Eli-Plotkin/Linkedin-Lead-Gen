from scrape_profiles import scrapeProfiles
from organize_data import organizeData


MY_POST_LINK = "https://www.linkedin.com/posts/brighthire_who-owns-interview-planning-the-recruiter-activity-7206335182633672704-FhWe?utm_source=share&utm_medium=member_desktop"
MY_LINKEDIN_LOGIN_EMAIL = "aeplotkin@gmail.com"
MY_LINKEDIN_LOGIN_PASSWORD = "MonkeyMilo1"



sp = scrapeProfiles()
if sp.export_scraped_data(email="aeplotkin@gmail.com", password="MonkeyMilo1",
                        post_link="https://www.linkedin.com/posts/brighthire_who-owns-interview-planning-the-recruiter-activity-7206335182633672704-FhWe?utm_source=share&utm_medium=member_desktop"):
    od = organizeData()
    od.export_organized_data(csvFile='scraped_profiles.csv', 
                             email="aeplotkin@gmail.com", 
                             password="MonkeyMilo1",
                             is_test_data=True)