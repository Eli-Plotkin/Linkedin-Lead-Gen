from src.organize_data import organizeData

def test_organize_data():
    od = organizeData()
    od.export_organized_data(csvFile='input_data/result(2).csv', 
                             email="aeplotkin@gmail.com", 
                             password="MonkeyMilo1",
                             is_test_data=True)
