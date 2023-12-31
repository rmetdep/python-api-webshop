from fastapi import FastAPI, Query                  # import FastAPI and Query
from random import randint                          # for random number generation
import json                                         # to read and create json files
import sqlite3                                      # sqlite db connector
from pydantic import BaseModel                      # base model for data validation
from fastapi.middleware.cors import CORSMiddleware  # CORS

# post class
class Task(BaseModel):
    title: str = None
    description: str = None
    done: str = False

# init app
app = FastAPI()

# CORS allow all origins
# origins = ["https://rmetdep.github.io", "https://bacbat32.sinners.be"]
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite db setup dict
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def rmv_json(file):
    file = file.replace("}", "").replace("{", "").replace("'", "")
    file = file.split(": ")
    return file[1]

# return link to docs if people are lazy and didn't read the docs
@app.get("/")
def read_root():
    return {"docs": "https://github.com/rmetdep/python-api-basic"}

@app.get("/tasks") # get a list of all tasks
async def get_tasks():
    conn = sqlite3.connect('data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    file = cur.execute("SELECT * FROM task;").fetchall()
    conn.close()
    return file

@app.get("/tasks/{taskid}") # get a task by id
async def get_task_by_id(taskid: str):
    conn = sqlite3.connect('data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    file = cur.execute("SELECT * FROM task WHERE taskId=" + taskid + ";").fetchall()
    conn.close()
    return file

@app.delete("/tasks/{taskid}") # delete a task by id
async def delete_task_by_id(taskid: str):
    conn = sqlite3.connect('data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    file = cur.execute("SELECT * FROM task WHERE taskId=" + taskid + ";").fetchall()
    conn.close()
    if file == []:
        return {"response": "task does not exist"}
    try:
        conn = sqlite3.connect('data.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("DELETE FROM task WHERE taskId=" + taskid + ";")
        conn.commit()
        conn.close()
    except:
        return {"response": "failed to delete task"}
    return {"response": "task deleted"}

@app.post("/tasks") # add a task and return it with an id
async def add_task(task: Task):
    print(task)
    conn = sqlite3.connect('data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    file = cur.execute("SELECT taskTitle FROM task;").fetchall()
    conn.close()
    for x in file:
        if rmv_json(str(x)) == task.title:
            return {"response": "task already exists"}
    conn = sqlite3.connect('data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute("INSERT INTO task (taskTitle, taskDescription, taskDone) VALUES ('" + task.title + "', '" + task.description + "', '" + task.done + "');")
    conn.commit()
    conn.close()
    return {"response": task.title + " added"}