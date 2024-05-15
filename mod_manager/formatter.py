def format_record(index: int, storage):
    record = storage.read()[index]
    name = record["name"]
    link = record["link"] 
    return name, link