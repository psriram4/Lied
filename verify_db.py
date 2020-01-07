import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

def verifyDatabaseCreation():
    db_list = client.list_database_names()
    if "bridge_db" in db_list:
        print("bridge_db exists")
    
    bridge_db = client["bridge_db"]
    if "artist_col" in bridge_db.list_collection_names():
        print("artist similarity data exists")
    if "tracks_col" in bridge_db.list_collection_names():
        print("track data exists")
    

def getArtistData():
    bridge_db = client["bridge_db"]
    artist_col = bridge_db["artist_col"]
    print(artist_col.find_one()) 

# verifyDatabaseCreation()
getArtistData()