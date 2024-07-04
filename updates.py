from pymongo import MongoClient

# Define the MongoDB connection URI
mongo_uri = "mongodb://localhost:27017/"

# Connect to the MongoDB server
client = MongoClient(mongo_uri)

# Specify the database and collection
db = client['facebook-data']
collection = db['groupscollections']

def update_documents(osint_id, new_attrib):
    # Define the query to find documents with the specific attribute containing '\n'
    query = {osint_id: {"$regex": "\n"}}  # Replace 'your_attribute' with your specific attribute name

    # Find all documents matching the query
    documents = collection.find(query)

    # Iterate through the documents and update them
    for document in documents:
        # Get the current value of the attribute
        original_string = document.get(osint_id)
        
        if original_string:
            # Remove all occurrences of the '\n' character
            modified_string = original_string.replace("\n", "")

            # Update the document with the modified string
            collection.update_many(
                query,
                {"$set": {osint_id: modified_string}}
            )
        if osint_id != 'osint_user_id':
            collection.update_many(
                {osint_id: {"$exists": True}},
                {"$rename": {osint_id: new_attrib}}
            )
    # print(f"Documents updated successfully: {result.modified_count}")
        

update_documents('osint_user_id', 'osint_user_id')
collection = db['userscollections']
update_documents('osint_user_id', 'osint_user_id')
db = client['telegram-data']
collection = db['channels']
update_documents(' ', 'osint_user_id')
collection = db['groups']
update_documents(' ', 'osint_user_id')
print("Documents updated successfully.")

# Close the MongoDB connection
client.close()