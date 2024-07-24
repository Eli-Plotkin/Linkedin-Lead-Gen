from src.organize_data import organizeData

def test_organize_data():
    od = organizeData()
    od.get_company_and_position('data/result(2).csv')