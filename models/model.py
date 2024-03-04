from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class Admin(BaseModel):
    email: str
    password: str

class Loan(BaseModel):
    name: str
    kycId: str
    weight: int
    accNo: int
    ifsc: str
    bank: str
    # ticketId: str

class Status(BaseModel):
    ticketId: str
    status: str

class KYC(BaseModel):
    aadhar: int
    username: str
    phone: int