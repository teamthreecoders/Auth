import logging
import random
import uuid
from app.core.util.jwt_util import generate_token,decode_token
from app.core.util.hasing import HashPassword
from app.crud.otp_crud import OTPCrud
from app.db.database import DB_CONN
from app.services.email_service import send_email
from jinja2 import Template
from app.template.html.email_template import EmailTemplate
from app.exception.exception import InvalidOTPService,EmailSendError,MissingArgumentError
from app.core.util.logger import get_logger

_logger = get_logger(__name__)   

class OTPService:
    def __init__(self, dbConn:DB_CONN = None):
        if dbConn is None:
            _logger.error(" dbConn not provided ")
            raise InvalidOTPService("DB Connection not provided")
        self._dbconn = dbConn

    def send_otp_over_email(self,to_email,/,user_name:str = None, purpose:str = None):
        if purpose is None:
            _logger.error(" purpose agrs not provided ")
            raise MissingArgumentError(" purpose should not be empty ")
        
        OTP = str(random.randint(100000, 999999))
        hash_otp = HashPassword.hash_password(OTP)
        
        if purpose == 'login':
            txn_id = 'txn' + str(uuid.uuid4()) + 'auth_login'
            body = Template(EmailTemplate.LOGIN_OTP_TEMPLATE).render(otp_code = OTP,expiry_minutes = '2')
            subject = Template(EmailTemplate.LOGIN_OTP_TEMPLATE_SUBJECT).render(otp_code = OTP)

        elif purpose == 'signup':
            txn_id = 'txn' + str(uuid.uuid4()) + 'auth_signup'
            body = Template(EmailTemplate.SIGNUP_OTP_TEMPLATE).render(otp_code = OTP,expiry_minutes = '2')
            subject = EmailTemplate.SIGNUP_OTP_TEMPLATE_SUBJECT

        elif purpose == '2fa':
            txn_id = 'txn' + str(uuid.uuid4()) + 'auth_2fa'
            body = Template(EmailTemplate.TWO_FA_OTP_TEMPLATE).render(otp_code = OTP,expiry_minutes = '2')
            subject = EmailTemplate.TWO_FA_OTP_TEMPLATE_SUBJECT
        
        is_successful = send_email(to_email,subject = subject,body=body,body_type='html')
        if is_successful:
            if not OTPCrud.create_otp(self._dbconn,txn_id=txn_id,email=to_email,hashed_otp=hash_otp,purpose=purpose):
                raise EmailSendError(" OTP Send failed to {to_email} ")
            else:
                return generate_token(payload={'txn_id': txn_id,'email':to_email},exp_time= 180)
        else:
            raise EmailSendError(f" OTP Send failed to {to_email}")
        

        
    def verify_otp(self,*,token,otp,purpose) -> dict:
        try:
            payload = decode_token(token)
            if payload['is_validated']:
                txn_id = payload.get('payload',{}).get('txn_id',None)
                email = payload.get('payload',{}).get('email',None)
            else:
                return {'is_verified' : False, 'message': 'Invalid OTP' ,'token' : None}
            
            otp_obj = OTPCrud.fetch_otp(self._dbconn,txn_id=txn_id,email = email,purpose = purpose)
            print('This is ::',otp_obj)
            if otp_obj is None:
                return {'is_verified' : False, 'message': 'Invalid OTP' ,'token' : None}
            else:
                hashed_otp = otp_obj.get('hashed_otp','null')
                if HashPassword.verify_password(otp,hashed_otp):
                    OTPCrud.update_is_verify(self._dbconn,txn_id=txn_id)
                    return {'is_verified' : True, 'message': 'OTP verified' ,'token' : generate_token(payload=payload.get('payload',{}),exp_time= 180)}
                else:
                    return {'is_verified' : False, 'message': 'Invalid OTP' ,'token' : None}
        except Exception as e:
            raise e
        

    def send_otp_over_sms(self,to_number):
        pass

    def senf_otp_over_whatsapp(self):
        pass
