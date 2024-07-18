from src.organize_data import organizeData

def test_organize_data():
    od = organizeData()
    od.signIn(email="aeplotkin@gmail.com", password="MonkeyMilo1")