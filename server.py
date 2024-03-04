from fastapi import FastAPI, HTTPException, status
import uvicorn
from models.model import User, Admin, Loan, Status, KYC
from fastapi.middleware.cors import CORSMiddleware
# from db.db import insert
from db.db import userColl, adminColl, loanColl
import uuid


app = FastAPI()

# connection()

app.add_middleware(
    CORSMiddleware,
    allow_methods = ['*'],
    allow_credentials = True,
    allow_headers = ['*'],
    allow_origins = ['*']
)


@app.get('/')
def home():
    return "🙌"

@app.post('/admin')
def admin(payload: Admin):
    data = payload.model_dump()
    print(data)
    if(adminColl.find_one(data)):
        raise HTTPException(status_code= status.HTTP_200_OK)
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)


@app.post('/login')
def login(payload: User):
    print(payload)
    data = payload.model_dump()
    print(data['username'])
    if(userColl.find_one(data)):
        print("Found")
        res = userColl.find_one(data)
        print(res['_id'])
        return {'id': str(res['_id'])}
    else:
        print("Nop")
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)

@app.post('/register')
def register(payload: User):
    data = payload.model_dump()
    if(userColl.find_one(data)):
        print("already registered")
        raise HTTPException(status_code= status.HTTP_409_CONFLICT)
    else:
        res = userColl.insert_one(data)
        if(res.inserted_id):
            print(res.inserted_id)
            raise HTTPException(status_code= status.HTTP_201_CREATED)

@app.post('/loanDetails')
def loanDetails(payload: Loan):
    data = payload.model_dump()
    ticketId = uuid.uuid4()
    data['ticketId'] = str(ticketId)
    data['status'] = 'pending'
    loanColl.insert_one(data)
    return {'ticketId': ticketId}

@app.get('/status/{ticketId}')
def get(ticketId: str):
    res = loanColl.find_one({'ticketId': ticketId})
    # print(res['status'])
    return {'status': res['status']}

@app.get('/details')
def detials():
    res = loanColl.find({'status': 'Pending'},{'_id':0})
    data = [i for i in res]
    return data

@app.patch('/loanDetails')
def patch(payload: Status):
    data = payload.model_dump()
    id = {'ticketId': data['ticketId']}
    update = {"$set": {'status': data['status']}}
    loanColl.update_one(id,update)
    # res = loanColl.find_one(data['ticketId'])

@app.post('/kyc')
def kyc(payload: KYC):    
    data = payload.model_dump()
    username = {'username': data['username']}
    print(username)
    update = {"$set": {'aadhar': data['aadhar'], 'phone': data['phone']}}
    res = userColl.update_one(username,update)
    if(res.matched_count == 1):
        out = userColl.find_one({'username': data['username']})
        return {'id': str(out['_id'])}
    

if __name__ == '__main__':
    uvicorn.run('server:app', reload=True)