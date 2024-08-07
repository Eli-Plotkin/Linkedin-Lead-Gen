from src.scrape_profiles import scrape_profiles

def test_scrape_profiles():
    sp = scrape_profiles()
    sp.sign_in(email="aeplotkin@gmail.com", password="MonkeyMilo1")
    sp.export_data(post_link="https://www.linkedin.com/feed/update/urn:li:activity:7223719016920485889/")
