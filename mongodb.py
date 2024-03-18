def mongodb(func):
    from pymongo import MongoClient

    def wrapper(**kwargs):
        host = kwargs['host']
        port = int(kwargs['port'])
        database_name = kwargs['database_name']
        collection_name = kwargs['collection_name']

        client = MongoClient(host=host, port=port)
        db = client[database_name]
        collection = db[collection_name]
        result = func(collection, **kwargs)
        return result
    return wrapper

@mongodb
def upload_to_mongo(collection, **kwargs):
    import json
    input_file_path = kwargs['input_file_path']

    documents = []
    with open(input_file_path, 'r') as json_file:
        for json_line in json_file.readlines():
            documents.append(json.loads(json_line))
    collection.insert_many(documents)

    return