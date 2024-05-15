import csv
import sys
import sqlite3
import random
from typing import Any
import math
from subprocess import check_output
import os
import datetime
import time

# DIR_OF_SCRIPT
script_dir="/".join(sys.argv[0].split("/")[:-1])

# ARGUMENT PARSING

arg_help:dict[str, dict[str, Any]] = {}

def getArg(args:list[str], dtype:type, default):
    arg_help[args[0]] = {
        "aliases":args[1:],
        "default":default
    }


    if dtype == bool:
        return any([arg in sys.argv for arg in args])

    for arg in args:
        if arg in sys.argv:
            return dtype(sys.argv[sys.argv.index(arg)+1])
    return dtype(default)

csvfile =     getArg(["--file", "-f"], str, "data.csv")
db =          getArg(["--database", "-d"], str, "db.db3")
codebook =    getArg(["--codebook", "-c"], str, "codebook.txt")
help_enable = getArg(["--help", "-h", "-?"], bool, False)
mitigations = getArg(["--mitigations", "-m"], str, "mitigations.csv")
tables =      getArg(["--tables", "-t"], str, "all").split(",")
now = time.time()

if help_enable:
    print(sys.argv[0])
    for key, data in arg_help.items():
        print(f'{key}\r\t\t\t{data["aliases"]}\r\t\t\t\t\t\t{data["default"]}')
    exit(0)

connection = sqlite3.Connection(db)

# compile...
os.system(f"g++ {script_dir}/hash.cpp -o /tmp/hash.out")

print_enable = False

def insert(table:str, data:dict[str, str]):
    if not table in tables and not tables[0] == "all":
        return
    global print_enable
    cursor = sqlite3.Cursor(connection)
    if print_enable: print(f"inserting into table: {table} values: {data}")
    statement = f"insert into {table} ({','.join(data.keys())}) values ({','.join(['?' for _ in range(len(data.keys()))])})"
    cursor.execute(statement, list(data.values()))


with open(codebook, "r") as file:
    data = file.read().split("\n")
    questions = {line.split("\t")[0][1:]:line.split("\t")[-1] for line in data if len(line) > 0 and line[0] == "Q"}
    default_questions = {line.split("\t")[0]:{
        "question":line.split("\t")[-1].split(", ")[0][1:-1],
        "args":{
            arg.split("=")[0]:arg.split("=")[1]
        for arg in line.split("\t")[-1].split(", ")[1:] if "=" in arg}
        # stupid table in a txt file of nonstandard format :pepedrool:
    } for line in data[119:132] if line.split("\t")[0] in [
        "education", 
        "urban", 
        "gender", 
        "religion", 
        "orientation", 
        "race", 
        "married"
    ]}

for key, value in default_questions.items():
    insert("questions", {
        "type":"valued",
        "question":value["question"], # we need to extend this to also store descriptions for args
        "tags":"default"
    })

for key, value in questions.items():
    insert("questions", {
        "id":int(key)+100,
        "type":"valued",
        "question":value
    })

with open(csvfile, "r") as file:
    reader = csv.reader(file, delimiter='\t', quotechar='|')
    header = None
    jid = 100
    for i, row in enumerate(reader):
        uid = i+100
        print_enable = not (uid%100)
        if not header:
            header = row
            continue
        insert("users", {
            "id":uid,
            "username":f"user{uid}",
            "state":"1",
            "password":check_output(["/tmp/hash.out", f"user{uid}", "123"]).decode()
        })
        age = int(row[header.index("age")])
        lower = int(math.floor(age/10)*10)
        upper = int(math.ceil((age+1)/10)*10)-1
        insert("userdata", {
            "userId":uid,
            "agegroup":f"{lower}-{upper}",
            "major":row[header.index("major")]
        })
        for i in range(3):
            jid+=1
            insert("journals", {
                "id":jid,
                "timestamp":now-(86400*i),
                "userId":uid,
            })
            picks = []
            answercount = 0
            while answercount < 8:
                qid = random.randint(1, len(questions.keys()))
                if qid in picks:
                    continue
                picks.append(qid)
                answercount+=1
                answer = row[header.index(f"Q{qid}A")]
                insert("answers", {
                    "value":answer,
                    "rating":random.randint(0,100)/100,
                    "questionId":qid,
                    "journalId":jid
                })

print_enable = True
with open(mitigations, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        insert("mitigations", {
        "type":row["type"],
        "tags":row["tag"],
        "title":row["title"],
		"description":row["description"]
    })

connection.commit()