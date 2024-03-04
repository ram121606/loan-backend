from pymongo import MongoClient
import os


client = MongoClient(os.environ.get('DB_URL'))

db = client['Gold-loan']
userColl = db['users']
adminColl = db['admin']
loanColl = db['loan-details']
# statusColl = db['status']
# def insert(payload):
#     print(payload)
#     res = coll.insert_one(payload)
#     print(res.inserted_id)
#     if(res.inserted_id):
#         return True
#     else:
#         return False