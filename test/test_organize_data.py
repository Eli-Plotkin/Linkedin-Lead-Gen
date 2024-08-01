from src.organize_data import organizeData

def test_organize_data():
    od = organizeData()
    companies_and_size_and_positions = od.get_data('data/result(2).csv', email="aeplotkin@gmail.com", password="MonkeyMilo1")
    od.export_data(companies_and_size_and_positions)