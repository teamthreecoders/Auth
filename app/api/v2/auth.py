import logging
from app.exception.exception import InvalidOTPService, EmailSendError, MissingArgumentError, InvalidAuthService,EmailFormatError
from app.services.auth_service import AuthServices
from app.services.otp_service import OTPService
from fastapi import  FastAPI,routing,HTTPException,APIRouter,Header
from app.db.database import DB_CONN
from fastapi import Depends
from app.models.user import CreateUser,SignUpEmail,OTPVerification,Current_session,LoginUser,LoginUser2fa
from app.template.payload import response
from app.core.util.validation import validate_email,validate_password
from app.services.auth_service_2 import AuthServices as AuthServices2
def get_db():
    conn = None
    try:
        conn = DB_CONN()
        yield conn  # pass it to the route

    except Exception as err:
        logging.error(f"Error in get_db: {err.args}", exc_info=True)

        raise err

    finally:
        if isinstance(conn,DB_CONN):
            logging.info(":: Requesting for close DB connection :: ")
            conn.close()


def get_current_user(authorization:str = Header(...)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    schema,token = authorization.split()
    if schema != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    try:
        user_details = AuthServices.get_token_decode(token=token)
        if user_details:
            details = response.payload(True,200," Auth Token Validated " , user_details)
            return details
        else:
            details = response.payload(False,400, " Invalid Auth Token ", errors = [{"request_header" : authorization}])
            raise HTTPException(400, detail=details)
        
    except Exception as err:
            details = response.payload(False,400, " Invalid Auth Token ", errors = [{"request_header" : authorization}])
            raise HTTPException(400, detail=details)
        

# router for authentication

router = routing.APIRouter(tags=["auth2"])



@router.get("/")
def read_root():
    return {"TEXT": "WELCOME TO AUTHENTICATION V1"}

@router.get('/me')
def current_session(session_payload:Current_session = Depends (get_current_user)):
    return session_payload

@router.post('/start-auth')
def start_auth(credential:SignUpEmail,dbConn:DB_CONN = Depends(get_db)):
    details:dict = None 
    user_email = credential.email
    try:
        validate_email(user_email)

        auth_service  = AuthServices(dbConn=dbConn)
        if is_user_exist := auth_service.user_exist(user_id = user_email):
            details:dict = response.payload(True,200," User Already Registered ")
            return details
        otp_service = OTPService(dbConn=dbConn)
        auth_token = otp_service.send_otp_over_email(user_email,purpose='signup')
        details = response.payload(True,200," New User Regitration ",data={'auth_token':auth_token})
        return details

    except EmailSendError as err:
        details = response.payload(False, 500, " OTP can not send ")
        raise HTTPException(status_code=500,detail=details)
    
    except InvalidOTPService as err:
        
        details = response.payload(False, 500, " Internal server error ")
        raise HTTPException(status_code=500,detail=details)
    
    except EmailFormatError as err:
        details:dict = response.payload(True,400,err.args[-1], errors = [{"request_payload":{"body" : {'email' : user_email }}}])
        raise HTTPException(status_code=400 , detail = details)
    
    except InvalidAuthService as err:
        details = response.payload(False, 500, " Internal server error ")
        raise HTTPException(status_code=500,detail=details)
    
    except Exception as err:
        logging.critical(err.args)
        details = response.payload(False, 503, " Service Unavailable")
        raise HTTPException(status_code=503,detail=details)
    
@router.post('/verify-2fa')
def verify_2fa(submitted_otp:OTPVerification,dbConn:DB_CONN = Depends(get_db)):
    try:
        auth_service = AuthServices2(dbConn)
        is_otp_verified = auth_service.verify_auth_2fa(token = submitted_otp.token,otp=submitted_otp.otp)
        return is_otp_verified
    except MissingArgumentError as err:
        details = response.payload(False,400,err.args[-1], errors = [{"request_payload":{"body" : {'token' : submitted_otp.token,'otp': submitted_otp.otp }}}])
        raise HTTPException(400,details)
    except InvalidAuthService as err:
        details = response.payload(False,500," Two factor authentication failed ", errors= err.args)
        raise HTTPException(500,details)
    
@router.post('/login/verify-2fa')
def login_verify_2fa(submitted_otp:OTPVerification,dbConn:DB_CONN = Depends(get_db)):
    details:dict = None
    try:
        otp_service = OTPService(dbConn)
        is_otp_verified = otp_service.verify_otp(token = submitted_otp.token,otp=submitted_otp.otp,purpose='login')

        if is_otp_verified.get('is_verified', False):
            auth_2fa_token = is_otp_verified.get('token', '')
            auth_service = AuthServices(dbConn=dbConn)
            auth_token = auth_service.create_session_token(payload=auth_service.get_current_user(token=auth_2fa_token))
            details = response.payload(True,200,' Two factor authentication successful', {'auth_token':auth_token})
            return details
        
    except MissingArgumentError as err:
        details = response.payload(False,400,err.args[-1], errors = [{"request_payload":{"body" : {'token' : submitted_otp.token,'otp': submitted_otp.otp }}}])
        raise HTTPException(400,details)
        
    except Exception as err:
        details = response.payload(False,500," Two factor authentication failed ", errors= err.args)
        raise HTTPException(500,details)
        

@router.post('/signup')
def signup(credentials:CreateUser,dbConn: DB_CONN = Depends(get_db)):
    try:
        auth_service = AuthServices2(dbConn)
        return auth_service.signup(email_verified_token=credentials.email_verified_token,
                            name = credentials.name,
                            phone=credentials.phone,
                            password=credentials.password,
                            role=credentials.role
                            )
    
    
    except InvalidAuthService as err:
        logging(err.args)
        raise HTTPException(500, 'Internal Server Error')
    
    except MissingArgumentError as err:
        logging(err.args)
        raise HTTPException(400, err.args[-1])
    
    

    # except Exception as err:
    #     logging.info(err)
    #     raise HTTPException(500, 'Internal Server Error')

@router.post('/login')
def login(credential:LoginUser,dbConn: DB_CONN = Depends(get_db)):
    try:
        auth_service = AuthServices2(dbConn)
        response_payload  = auth_service.login(user_id=credential.user_id,password=credential.password)
        return response_payload
    except InvalidAuthService as err:
        logging(err.args)
        raise HTTPException(500, 'Internal Server Error')
    
    # except Exception as err:
    #     logging.info(err)
    #     raise HTTPException(500, 'Internal Server Error')


@router.post('/login/2fa')
def login_2fa( credential:LoginUser2fa,dbConn: DB_CONN = Depends(get_db)):
    auth_service = AuthServices2(dbConn)
    return auth_service.verify_login_2fa(token=credential.auth_2fa_token,otp=credential.otp)
    
