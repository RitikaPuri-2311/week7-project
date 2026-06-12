from app.mongodb import activity_collection

result = activity_collection.insert_one({
    "event": "test"
})

print(result.inserted_id)