from src.organize_data import organizeData

def test_organize_data():
    od = organizeData()
    companies_and_positions = od.get_companies_and_positions('data/result(2).csv')
    od.export_data(companies_and_positions)