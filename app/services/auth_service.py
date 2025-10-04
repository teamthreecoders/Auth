from app.crud.user_crud import UserCRUD
from app.crud.otp_crud import OTPCrud
from app.core.util.hasing import HashPassword
from app.core.util.jwt_util import generate_token,decode_token
from app.db.database import DB_CONN
from app.services.email_service import send_email
from jinja2 import Template
from app.template.html.email_template import EmailTemplate
from app.exception.exception import InvalidAuthService,MissingArgumentError, EmailFormatError, PasswordFormatError
from app.core.util.validation import validate_email,validate_password
from typing import Tuple,Dict,List
class AuthServices:
    _current_user_details = None
    def __init__(self, dbConn:DB_CONN = None):
        if dbConn is None:
            raise InvalidAuthService("No database connection provided")
        self._dbconn = dbConn

    def _getUser(self,*,user_id:str = None):
        if user_id is None:
            raise MissingArgumentError('User id  must be provided ')
        valid_tlds = [
            "com", "org", "net", "edu", "gov", "mil", "int",
            "in", "us", "uk", "ca", "au", "de", "fr", "ru", "cn", "jp",
            "io", "ai", "dev", "app", "tech", "xyz", "me", "info", "biz", "co", "online", "shop", "cloud"
        ]
        # if client give email
        if '@' in user_id and user_id.split('@')[-1].split('.')[-1] in valid_tlds:

            user_details = UserCRUD.get_user_by_email(self._dbconn, email=user_id)

        # if client give phone no
        elif user_id.isdigit():
            user_details = UserCRUD.get_user_by_phone(self._dbconn, phone=str(user_id))
        # if client give any other
        else:
            user_details = UserCRUD.get_user_by_id(self._dbconn, user_id= str(user_id))
        return user_details

    def get_current_user(self,*,token:str):
        if token is None:
            raise MissingArgumentError("Token must be provided")
        
        payload = decode_token(token)
        user_id = payload.get('email')
        try:
            if user_id is None:
                raise Exception("User id not found")
            user_details = self._getUser(user_id=user_id)
            if user_details is None:
                raise Exception("User not found")
        except  Exception as e:
            raise e

        del user_details['hashed_password']
        return user_details


    def authenticate_user(self,*,user_id:str,password:str) -> Tuple[bool,str, str]:
        if user_id is None or password is None:
            raise MissingArgumentError("User id and password must be provided")

        try:
            user_details = self._getUser(user_id=user_id)
            if user_details is None:
                raise Exception("User not found")
            
        except  Exception as e:
            raise e

        DB_STORED_PASSWORD = user_details['hashed_password']
        try:
           result = HashPassword.verify_password(password=password,hashed_password=DB_STORED_PASSWORD)
           if result:
               payload = {
                   "user_id":user_details['ID'],
                   "email":user_details['email'],
                   "is_verified" :  user_details['is_verified'],
                   "role":user_details['role']
               }
               auth_token = generate_token(payload=payload,exp_time=180)
               return user_details['is_2fa_enabled'],user_details['email'],auth_token
           else:
               raise ValueError("Incorrect password")
        except Exception as e:
            raise ValueError(" Something went wrong :: {}",e)
        


    def register_user(self, *, token:str , name:str,phone:str,password:str,role:str = 'user' ):

        if token is None:
            raise MissingArgumentError(" Token can not be empty ")

        from random import randint
        payload = decode_token(token)
        txn_id,email = payload['txn_id'],payload['email']

        is_otp_validated = OTPCrud.is_otp_validated(self._dbconn,txn_id = txn_id,email=email,purpose='signup')

        if not is_otp_validated:
            raise Exception(' OTP VALIDATION FAILED ')

        USER_ID = name[:3].upper() + str(randint(1000,9999)) + str(phone[-4:])

        isPhoneExist = UserCRUD.get_user_by_phone(self._dbconn,phone = str(phone))
        isEmailExist = UserCRUD.get_user_by_email(self._dbconn,email=email)

        if isPhoneExist:
            raise ValueError('Phone number already exist')

        if isEmailExist:
            raise ValueError('Email already exist')

        rowCnt = UserCRUD.create_user(self._dbconn,  id = USER_ID ,email= email,
                                            phone= phone,
                                            hashed_password= HashPassword.hash_password(password=password),role=role)

        if rowCnt:
            OTPCrud.update_is_used(self._dbconn,txn_id = txn_id)
            body = Template(EmailTemplate.WELCOME_ONBOARD).render()
            subject = 'Greetings !!! Successfully Onboard'
            send_email(to_email=email,subject=subject,body_type='html',body = body)
            payload = {
                "user_id": USER_ID,
                "email":email,
                "role":role
            }
            auth_token = self.create_session_token(payload=payload)
            return rowCnt,auth_token
        return  rowCnt,None

    def user_exist(self,*,user_id:str) -> bool:
        if user_id is None:
            raise MissingArgumentError("User is must be provided")
        user_details = self._getUser(user_id=user_id)
        if user_details:
            return True
        else:
            return False

    def is_2fa_enabled(self,*,user_id:str) -> bool:
        if user_id is None:
            raise MissingArgumentError("User is must be provided")
        user_details = self._getUser(user_id=user_id)
        if user_details:
            return user_details['is_2fa_enabled']
        else:
            return False


    def create_session_token(self,*,payload: Dict,exp_time: int = 9000):
        if payload is not None or payload != {}:
            session_token = generate_token(payload=payload,exp_time=exp_time)
            return session_token
        return None
    
    @staticmethod
    def get_token_decode(*,token):
        return decode_token(token=token)
    