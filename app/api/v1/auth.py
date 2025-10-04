import logging

import app.core.util.jwt_util
from app.exception.exception import InvalidOTPService, EmailSendError, MissingArgumentError, InvalidAuthService
from app.services.auth_service import AuthServices
from app.services.otp_service import OTPService
from fastapi import  FastAPI,routing,HTTPException,APIRouter,Header
from app.db.database import DB_CONN
from fastapi import Depends
from app.models.user import CreateUser,SignUpEmail,OTPVerification,Current_session
from app.core.util.logger import get_logger
from app.core.util.validation import validate_email,validate_password

def get_db():
    conn = None
    try:
        conn = DB_CONN()
        yield conn  # pass it to the route

    # except pymysql.DatabaseError as err:
    #     logging.error(f"DBCONN ERRPR")
    #     raise err

    except Exception as err:
        logging.error(f"Error in get_db: {err.args}", exc_info=True)
        # re-raise so FastAPI can handle the exception properly
        raise err

    finally:
        if isinstance(conn,DB_CONN):
            logging.info(":: Requesting for close DB connection :: ")
            conn.close()

def get_current_user(authorization:str = Header(...),dbConn = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    schema,token = authorization.split()
    if schema != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    try:
        auth_service = AuthServices(dbConn)
        user = auth_service.get_current_user(token=token)
        if user:
            return user
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except InvalidAuthService as err:
        raise HTTPException(status_code=500, detail="Error Auth Service")
    except Exception as err:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# router for authentication
router = routing.APIRouter(prefix="/auth/v1", tags=["auth"])

@router.get("/")
def read_root():
    return {"TEXT": "WELCOME TO AUTHENTICATION V1"}

@router.get('/me')
def current_session(session_payload:Current_session = Depends (get_current_user)):
    return session_payload

@router.post('/log-in-or-create-account')
def signup(userEmail: SignUpEmail, dbConn: DB_CONN = Depends(get_db)):
    try:
        auth_service = AuthServices(dbConn)
        is_user_exist = auth_service.user_exist(user_id=userEmail.email)
        otp_service = OTPService(dbConn)
        if is_user_exist:
            logging.info(f"User already exist")
            verification_token = otp_service.send_otp_over_email(userEmail.email,purpose='login')
            payload = {
                "msg":"User already exist",
                "token": verification_token
            }

            raise HTTPException(status_code=400, detail=payload)
        # otp_service = OTPService(dbConn)
        token = otp_service.send_otp_over_email(userEmail.email,purpose='login')
        return {"txn_token": token}

    except MissingArgumentError as err:
        raise HTTPException(status_code=400, detail={err.args[1]})

    except EmailSendError as err:
        raise HTTPException(status_code=400, detail="Can not send OTP")

    except InvalidOTPService as err:
        raise HTTPException(status_code=401, detail="Can not send OTP")

    except HTTPException as e:
        raise e

    except Exception as err:
        logging.error(f"Unexpected error: {err}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post('/signup/verify_otp')
def signup_verify_otp(submitted_otp:OTPVerification,dbConn:DB_CONN = Depends(get_db)):
    try:
        otp_service = OTPService(dbConn)
        is_valid = otp_service.verify_otp(token = submitted_otp.token,otp=submitted_otp.otp)
        if is_valid:
            return is_valid
        else:
            raise HTTPException(status_code=401, detail="Invalid OTP")

    except InvalidOTPService as err:
        raise HTTPException(status_code=401, detail="Can not send OTP")

    except Exception as err:
        raise HTTPException(status_code=400, detail="Server not found")


@router.post('/signup')
def signup_create_account(user:CreateUser,dbConn:DB_CONN = Depends(get_db)):
    auth_service = AuthServices(dbConn)
    try:
        auth_service.register_user(token=user.token,name = user.name,password=user.password,phone=user.phone,role= user.role)
        return {"message":"user created successfully"}
    except Exception as err:
        print(err)
        raise  HTTPException(status_code=400, detail="Not created user")

@router.get('/login')
def login(user_id:str = None,password:str = None, dbConn:DB_CONN = Depends(get_db)):
    try:
        auth_service = AuthServices(dbConn)
        token = auth_service.authenticate_user(user_id = user_id,password=password)
        if not token:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        is_2fa_enabled = auth_service.is_2fa_enabled(user_id=user_id)
        if not is_2fa_enabled:
            return {"is_2fa_enabled":False,"access_token": token, "token_type": "bearer"}
        else:
            otp_service = OTPService(dbConn)
            token = otp_service.send_otp_over_email(to_email=user_id)
            return {"is_2fa_enabled":True,"token": token}

    except InvalidAuthService as err:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    except InvalidOTPService as err:
        raise HTTPException(status_code=401, detail="Can not send OTP")

    except ValueError as e:
        logging.error(e)
        raise HTTPException(status_code=401, detail="Invalid credentials")

    except Exception as err:
        logging.error(f"Unexpected error: {err}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/login/verify-2fa")
def verify_2fa(submitted_otp:OTPVerification,dbConn:DB_CONN = Depends(get_db)):
    try:
        otp_service = OTPService(dbConn)
        is_valid = otp_service.verify_otp(token = submitted_otp.token,otp=submitted_otp.otp)
        print("is_validate",is_valid)
        print(submitted_otp)
        if is_valid:
            auth_service = AuthServices(dbConn)
            if user_details := auth_service.get_current_user(token = submitted_otp.token):
                payload  = {
                    "message ": "2FA verified",
                    "data" : user_details
                }
                generate_token = app.core.util.jwt.generate_token(payload=payload,exp_time=1000)
                return {"access_token": generate_token, "token_type": "bearer"}
            else:
                return {"message":"2FA not Verified successfully",}
        else:
            raise HTTPException(status_code=401, detail="Invalid OTP")

    except InvalidOTPService as err:
        raise HTTPException(status_code=401, detail="Can not send OTP")
    except Exception as err:
        logging.error("::2FA:: ",err)
        raise HTTPException(status_code=400, detail="Server not found")




