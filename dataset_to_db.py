import csv
import os
import sys
import sqlite3
import random

dataset = sys.argv[sys.argv.index("--dataset")+1]

infofile = sys.argv[sys.argv.index("--info")+1]

db = sys.argv[sys.argv.index("--database")+1]

connection = sqlite3.Connection(db)

id_offset = 100

with open(infofile) as file:
    qs = [(line.split("\t", 1)[0][1:], line.split("\t", 1)[1]) for line in file.read().split("\n") if len(line) > 0 and line[0] == "Q"]
    for index, q in qs:
        cursor = sqlite3.Cursor(connection)
        query = f"insert or replace into questions (id, type, question) values (?, ?, ?)"
        cursor.execute(query, [id_offset+int(index), 0, q])
        connection.commit()

print("Inserted questions at an id offset of {qid_offset}")


with open(dataset, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    header = []
    qcount = None
    jid = id_offset
    for user_count, row in enumerate(reader):
        if not header:
            header = row
            qcount = len([col for col in header if col[0] == "Q" and col[-1] == "A"])
            print(f"There are {qcount} questions")
        else:
            cursor = sqlite3.Cursor(connection)
            query = f"insert into users (username, password, state) values (?, ?, ?)"
            print(f"creating user: user{user_count}")
            cursor.execute(query, [f'user{user_count}', "123", 1])
            for _ in range(3):
                jid += 1
                query = f"insert into journals (id, userId) values (?, ?)"
                cursor.execute(query, [jid, user_count])
                for qid in [random.randint(1, qcount) for _ in range(8)]:
                    answer = row[header.index(f"Q{qid}A")]
                    query = f"insert into answers (answer, journalId, questionId) values (?, ?, ?)"
                    cursor.execute(query, [answer, jid, qid])
            connection.commit()
