from src.scrape_profiles import scrape_profiles

def test_scrape_profiles():
    sp = scrape_profiles()
    sp.export_data(email="aeplotkin@gmail.com", 
                    password="MonkeyMilo1",
                    post_link="https://www.linkedin.com/posts/brighthire_who-owns-interview-planning-the-recruiter-activity-7206335182633672704-FhWe?utm_source=share&utm_medium=member_desktop")
