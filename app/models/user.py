
from pydantic import BaseModel
from typing import Optional

class CreateUser(BaseModel) :
    email_verified_token:str
    name : str
    password : str
    phone : str
    is_2fa_enebled:bool = False
    is_active : bool = False
    role : str = 'user'


class LoginUser(BaseModel):
    user_id : str
    password : str

class LoginUser2fa(BaseModel):
    auth_2fa_token:str
    otp:str
    
class SignUpEmail(BaseModel):
    email : str

class OTPVerification(BaseModel):
    token: str
    otp: str

class SignUpPhone(BaseModel):
    phone : str

class SignUpWhatsapp(BaseModel):
    phone : str


class Current_session(BaseModel):
    token: str

