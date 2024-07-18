from src.organize_data import organizeData

def test_organize_data():
    od = organizeData()
    od.findBigPlayers('data/result(2).csv')