import csv
import sqlite3

csvfile = "mitigations.csv"
db = "db.db3"

connection = sqlite3.Connection(db)

def insert(table:str, data:dict[str, str]):
    cursor = sqlite3.Cursor(connection)
    print(f"inserting into table: {table} values: {data}")
    statement = f"insert into {table} ({','.join(data.keys())}) values ({','.join(['?' for _ in range(len(data.keys()))])})"
    cursor.execute(statement, list(data.values()))

with open(csvfile, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        insert("mitigations", {
        "type":row["type"],
        "tags":row["tag"],
        "title":row["title"],
		"description":row["description"]
    })
    


connection.commit()