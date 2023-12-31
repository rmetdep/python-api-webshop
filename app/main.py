from fastapi import FastAPI, Query                  # import FastAPI and Query
from random import randint                          # for random number generation
import json                                         # to read and create json files
import sqlite3                                      # sqlite db connector
from pydantic import BaseModel                      # base model for data validation
from fastapi.middleware.cors import CORSMiddleware  # CORS

# put class
class Item(BaseModel):
    name: str = None

# post class
class Order(BaseModel):
    itemid: str = None
    userid: str = None
    amount: str = None

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
    return {"docs": "https://github.com/rmetdep/python-api-webshop"}

# ----------------------
#         ITEMS
# ----------------------

@app.get("/items") # get a list of all items
async def get_items():
    conn = sqlite3.connect('data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    file = cur.execute("SELECT * FROM item;").fetchall()
    conn.close()
    return file

@app.get("/items/{itemid}") # get an item by id
async def get_item_by_id(itemid: str):
    conn = sqlite3.connect('data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    file = cur.execute("SELECT * FROM item WHERE itemId=" + itemid + ";").fetchall()
    conn.close()
    return file

@app.put("/items") # add an item and return it with an id
async def add_item(item: Item):
    print(item)
    conn = sqlite3.connect('data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    file = cur.execute("SELECT itemName FROM item;").fetchall()
    conn.close()
    for x in file:
        if rmv_json(str(x)) == item.name:
            return {"response": "item already exists"}
    conn = sqlite3.connect('data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute("INSERT INTO item (itemName) VALUES ('" + item.name + "');")
    conn.commit()
    conn.close()
    return {"response": item.name + " added"}

@app.delete("/items/{itemid}") # delete an item by id
async def delete_item_by_id(itemid: str):
    conn = sqlite3.connect('data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    file = cur.execute("SELECT * FROM item WHERE itemId=" + itemid + ";").fetchall()
    conn.close()
    if file == []:
        return {"response": "item does not exist"}
    try:
        conn = sqlite3.connect('data.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("DELETE FROM item WHERE itemId=" + itemid + ";")
        conn.commit()
        conn.close()
    except:
        return {"response": "failed to delete item"}
    return {"response": "item deleted"}

# ----------------------
#        ORDERS
# ----------------------

@app.get("/orders") # get a list of all items
async def get_orders():
    conn = sqlite3.connect('data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    file = cur.execute("SELECT * FROM orders;").fetchall()
    conn.close()
    return file

@app.get("/orders/{orderid}") # get an item by id
async def get_order_by_id(orderid: str):
    conn = sqlite3.connect('data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    file = cur.execute("SELECT * FROM orders WHERE orderId=" + orderid + ";").fetchall()
    conn.close()
    return file

@app.post("/orders") # add an order and return it with an id
async def add_order(order: Order):
    print(order)
    conn = sqlite3.connect('data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (itemId, userId, amount) VALUES ('" + order.itemid + "', '" + order.userid + "', '" + order.amount + "');")
    conn.commit()
    conn.close()
    return {"response": order.itemid + " * " + order.amount + " added"}

@app.delete("/orders/{orderid}") # delete an order by id
async def delete_order_by_id(orderid: str):
    conn = sqlite3.connect('data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    file = cur.execute("SELECT * FROM orders WHERE orderId=" + orderid + ";").fetchall()
    conn.close()
    if file == []:
        return {"response": "order does not exist"}
    try:
        conn = sqlite3.connect('data.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute("DELETE FROM orders WHERE orderId=" + orderid + ";")
        conn.commit()
        conn.close()
    except:
        return {"response": "failed to delete order"}
    return {"response": "order deleted"}

# ----------------------
#         USERS
# ----------------------

@app.get("/users") # get a list of all items
async def get_users():
    conn = sqlite3.connect('data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    file = cur.execute("SELECT * FROM user;").fetchall()
    conn.close()
    return file

@app.get("/users/{userid}") # get an item by id
async def get_user_by_id(userid: str):
    conn = sqlite3.connect('data.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    file = cur.execute("SELECT * FROM user WHERE userId=" + userid + ";").fetchall()
    conn.close()
    return file