import pymongo

# Assuming you have a MongoDB client and a collection object
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["twitter-data"]
collection = db["twitter"]

# Define the filter to target documents with empty or missing "tweets" attribute
filter = {"tweets": {"$exists": True, "$eq": []}}
filter1 = {"UserName": {"$exists": True, "$in": ["@MapEthiopia", "@BarackObama", "@addisstandard", "@DanielBekele", "@Heyab_raya", "@MichelleObama", "@belfort_andrew", "@JoeBiden", "@taylorswift13", ""]}}

# Delete documents matching the filter
result = collection.delete_many(filter1)

# Output the number of deleted documents
print("Deleted", result.deleted_count, "documents.")