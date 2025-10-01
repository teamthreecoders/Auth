from pydantic import BaseModel
from typing import Optional

class CreateUser(BaseModel) :
    token:str
    name : str
    password : str
    phone : str
    is_active : bool = False
    role : str = 'user'


class LoginUser(BaseModel):
    user_id : str
    password : str

class SignUpEmail(BaseModel):
    email : str

class OTPVerification(BaseModel):
    token: str
    otp: str

class SignUpPhone(BaseModel):
    phone : str

class SignUpWhatsapp(BaseModel):
    phone : str