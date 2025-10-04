import logging
from app.crud.user_crud import UserCRUD
from app.core.util.hasing import HashPassword
from app.core.util.jwt_util import generate_token,decode_token
from app.db.database import DB_CONN
from app.services.email_service import send_email
from jinja2 import Template
from app.template.html.email_template import EmailTemplate
from app.exception.exception import InvalidAuthService,MissingArgumentError, EmailFormatError, PasswordFormatError
from app.core.util.validation import validate_email,validate_password
from typing import Tuple,Dict,List
from app.template.payload import response
from app.services.otp_service import OTPService
from fastapi import HTTPException
from app.crud.user_crud import UserCRUD
from app.crud.otp_crud import OTPCrud
from app.exception import exception

class AuthServices:
    # Configure root logger once (usually done at app entry-point)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Private class-level logger instance
    __logger = logging.getLogger('AuthServices')
    _current_user_details = None

    def __init__(self, dbConn:DB_CONN = None):
        if dbConn is None:
            self.__logger.critical(" DB Connection not provided ")
            raise InvalidAuthService(" dbConn :: DB connection provided")
        self._dbconn = dbConn
        

    def _getUser(self,*,user_id:str = None):
        if user_id is None or user_id == '':
            self.__logger.info(" MissingArgumentError :: User id is empty ")
            raise MissingArgumentError('User id is empty')
        
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
        
        if user_details is None:
            raise exception.UserNotFoundError("user_id not found")
        return user_details

    def __create_session_token(self,*,user_id,exp_time: int = 9000):

        try:
            user_details = self._getUser(user_id=user_id)
            print(user_details)
            user_details.pop('email')
            user_details.pop('hashed_password')
            return {'is_session_created':True, 'auth_session_token': generate_token(payload=user_details,exp_time=exp_time)}
        except Exception as err:
            return {'is_session_created':False, 'auth_session_token': None }
        
    
        # if payload is not None or payload != {}:
        #     session_token = generate_token(payload=payload,exp_time=exp_time)
        #     return session_token

    # def __get_current_user(self,*,token:str):
    #     if token is None:
    #         raise MissingArgumentError("Token must be provided")
        
    #     payload = decode_token(token)
    #     user_id = payload.get('email')
    #     try:
    #         if user_id is None:
    #             raise Exception("User id not found")
    #         user_details = self._getUser(user_id=user_id)
    #         if user_details is None:
    #             raise Exception("User not found")
    #     except  Exception as e:
    #         raise exception( " User Not Found ")
    #     del user_details['hashed_password']
    #     return user_details
    

    def login(self,*,user_id:str,password:str):
        try:
            if user_id is None or password is None or user_id == "" or password == "":
                raise exception.UserNotFoundError( " user_id and password are should not empty " )
            
            user_details = self._getUser(user_id=user_id)

            user_email = user_details['email']
            hashed_password = user_details['hashed_password']
            is_password_matched = HashPassword.verify_password(password=password,hashed_password=hashed_password)
           
            if not is_password_matched:
                raise exception.UserNotFoundError(" Password not matched ")

            if user_details['is_2fa_enabled']:
                otp_service = OTPService(self._dbconn)
                txn_2fa_token = otp_service.send_otp_over_email(user_email,purpose='2fa')
                payload = response.payload(True,200," Required 2FA ", data={'user_id':user_details.get('ID'),'is_2fa_enabled':True, 'txn_2fa_token':txn_2fa_token})
                return payload

            user_details.pop('hashed_password')
            user_details.pop('phone')

            auth_session_token = self.__create_session_token(user_id=user_id,exp_time=3600)
            print(auth_session_token)
            if auth_session_token['is_session_created']:
                payload = response.payload(True,200,"login successful", data = {'user_id':user_details.get('ID'),'is_2fa_enabled':False, 'auth_session_token':auth_session_token})
                return payload
            payload = response.payload(True,400,"login failed", errors = {'error':'session token cration failed'})
            return payload

        except exception.UserNotFoundError as err:
            self.__logger.error(err.args)
            print(err.args)
            payload = response.payload(False,401, "login failed", errors = {'message':err.args[0]})
            raise HTTPException(401,payload)

        except KeyError as err:
            self.__logger.error(err.args)
            payload = response.payload(False,500, "login failed", errors=  {'message':err.args[0]})
            raise HTTPException(500,payload)

    

    def signup(self,email_verified_token,name,phone,password,role = 'user'):
        try:
            token_payload = decode_token(token=email_verified_token)
            if not token_payload['is_validated']:
                payload = response.payload(False,400,token_payload['message'],errors={'email_verified_token':email_verified_token})
                raise HTTPException(400,payload)            
            
            txn_id = token_payload.get('payload',{}).get('txn_id','')
            user_email = token_payload.get('payload',{}).get('email','')
            
            is_otp_validated = OTPCrud.is_otp_validated(self._dbconn,txn_id = txn_id,email=user_email,purpose='signup')
            if not is_otp_validated:
                payload = response.payload(False,401, 'Unauthorized Entry' ,errors={'email_verified_token':email_verified_token})
                raise HTTPException(401,payload)   

            validate_email(user_email)
            validate_password(password=password)

            # phone check
            if UserCRUD.get_user_by_phone(self._dbconn, phone=str(phone)):
                payload = response.payload(
                    False, 400, "Phone number already exists",
                    errors={'phone': phone}
                )
                raise HTTPException(status_code=400, detail=payload)

            # email check
            if UserCRUD.get_user_by_email(self._dbconn, email=user_email):
                payload = response.payload(
                    False, 400, "Email already exists",
                    errors={'email': user_email}
                )
                raise HTTPException(status_code=400, detail=payload)


            hashed_password = HashPassword(password)
            from random import randint
            USER_ID = name[:3].upper() + str(randint(1000,9999)) + str(phone[-4:])
            payload = {
                "user_id": USER_ID,
                "email":user_email,
                "role":role
            }
            
            auth_token = generate_token(payload=payload,exp_time=3600)

            if not auth_token:
                payload = response.payload(False,500,'Registration failed', errors={'error': 'Auth token creation unsuccessful'})
                raise HTTPException(500,payload)
            
            rowCnt = OTPCrud.update_is_used(self._dbconn,txn_id = txn_id)
            if not rowCnt:
                payload = response.payload(False,501, 'Registration failed' , errors={'message' : 'OTP Already used'})
                raise HTTPException(501,payload) 
                
            rowCnt = UserCRUD.create_user(self._dbconn,id = USER_ID,email=user_email,phone=phone,hashed_password=hashed_password,role=role)
            if not rowCnt:
                payload = response.payload(False,501, 'Registration failed' , errors={'message' : 'User creation failed'})
                raise HTTPException(501,payload) 

            body = Template(EmailTemplate.WELCOME_ONBOARD).render()
            subject = 'Greetings !!! Successfully Onboard'
            send_email(to_email=user_email,subject=subject,body_type='html',body = body)
            return response.payload(True,200,'Registration successful',{'user_id':USER_ID,'auth_session_token':auth_token})

        except EmailFormatError as err:
            payload = response.payload(
                success=False,
                status_code=422,
                message='Registration failed',
                errors={'email': str(err)}
            )
            raise HTTPException(422, payload)

        except PasswordFormatError as err:
            payload = response.payload(
                success=False,
                status_code=422,
                message='Registration failed',
                errors={'password': str(err)}
            )
            raise HTTPException(422, payload)

    
    def verify_login_2fa(self,*,token,otp):
        try:
            token_payload = decode_token(token=token)
            if not token_payload['is_validated']:
                payload = response.payload(False,400,token_payload['message'],errors={'2fa_token':token})
                raise HTTPException(400,payload) 
             
            otp_service = OTPService(self._dbconn)
            payload = otp_service.verify_otp(token=token,otp=otp,purpose='2fa')
            if not payload.get('is_verified'):
                response_payload = response.payload(False,400,payload.get('message'),errors = {'request_payload': {'2fa_token':token,'otp':otp} })
                raise HTTPException(400,response_payload)
            
            
            user_email = token_payload.get('payload',{}).get('email','')
            auth_session_token = self.__create_session_token(user_id = user_email  ,exp_time=9000)
            if auth_session_token['is_session_created'] is None:
                response_payload = response.payload(False,400,'login failed',errors={'message':'Someting went wrong'})
                raise HTTPException(400,response_payload)
            
            response_payload = response.payload(True,200,'login successful',data={'user_id':user_email,'is_2fa_enabled':True,'auth_session_token' : auth_session_token["auth_session_token"] })
            return response_payload
        except Exception as err:
            raise err
    
    def verify_auth_2fa(self,*,token,otp):
        token_payload = decode_token(token)
        if not token_payload['is_validated']:
            response_payload = response.payload(False,400,token_payload['message'],errors={'2fa_token':token})
            raise HTTPException(400,response_payload)
        otp_service = OTPService(self._dbconn)
        payload = otp_service.verify_otp(token=token,otp=otp,purpose='signup')
        if not payload.get('is_verified'):
            response_payload = response.payload(False,400,payload.get('message'),errors = {'request_payload': {'2fa_token':token,'otp':otp} })
            raise HTTPException(400,response_payload)
        auth_2fa_token = payload.get('token','')
        response_payload = response.payload(True,200,' Two factor authentication successful', {'auth_2fa_token':auth_2fa_token})
        return response_payload
    
    
