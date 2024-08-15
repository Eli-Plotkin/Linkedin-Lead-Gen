from src.organize_data import organizeData

def test_organize_data():
    od = organizeData()
    od.export_organized_data(csvFile='scraped_profiles.csv', 
                             email="aeplotkin@gmail.com", 
                             password="MonkeyMilo1",
                             is_test_data=True)
