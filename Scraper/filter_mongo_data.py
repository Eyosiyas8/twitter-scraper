import pymongo

# Assuming you have a MongoDB client and a collection object
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["twitter-data"]
collection = db["twitter"]

# Define the filter to target documents with empty or missing "tweets" attribute
filter = {"tweets": {"$exists": True, "$eq": []}}

# Delete documents matching the filter
result = collection.delete_many(filter)

# Output the number of deleted documents
print("Deleted", result.deleted_count, "documents.")