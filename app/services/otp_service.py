import random
from app.core.util.jwt import generate_token,decode_token
from app.core.util.hasing import HashPassword
import uuid
from app.crud.otp_crud import OTPCrud
from app.db.database import DB_CONN
from app.services.email_service import send_email
from jinja2 import Template
from app.template.html.email_template import EmailTemplate


class OTPService:
    def __init__(self, dbConn:DB_CONN = None):
        if dbConn is None:
            raise Exception("No database connection provided")
        self._dbconn =dbConn

    def send_otp_over_email(self,to_email):
        OTP = str(random.randint(100000, 999999))
        hash_otp = HashPassword.hash_password(OTP)
        txn_id = 'txn' + str(uuid.uuid4())
        subject = "OTP Confirmation"
        body = Template(EmailTemplate.OTP_SEND).render(otp=OTP)
        is_successful = send_email(to_email,subject = subject,body=body,body_type='html')
        if is_successful:
            if not OTPCrud.create_otp(self._dbconn,txn_id=txn_id,email=to_email,hashed_otp=hash_otp):
                raise Exception("Failed to create OTP")
            else:
                return generate_token(payload={'txn_id': txn_id,'email':to_email},exp_time= 180)
        else:
            raise Exception("Failed to send email")


    def verify_otp(self,*,token,otp):
        try:
            payload = decode_token(token)
            txn_id = payload['txn_id']
            otp_obj = OTPCrud.fetch_otp(self._dbconn,txn_id=txn_id)
            print(payload)
            if otp_obj is None:
                raise Exception("Invalid token")
            else:
                hashed_otp = otp_obj['hashed_otp']
                if HashPassword.verify_password(otp,hashed_otp):
                    OTPCrud.update_is_verify(self._dbconn,txn_id=txn_id)
                    return {'otp_verify' : True,'token' : generate_token(payload=payload,exp_time= 180)}
                else:
                    raise Exception("Invalid OTP")
        except Exception as e:
            raise Exception(e)

    def send_otp_over_sms(self,to_number):
        pass

    def senf_otp_over_whatsapp(self):
        pass
