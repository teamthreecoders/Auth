import logging

from app.services.auth_service import AuthServices
from app.services.otp_service import OTPService
from fastapi import  FastAPI,routing,HTTPException,APIRouter
from app.db.database import DB_CONN

from fastapi import Depends

from app.models.user import CreateUser,SignUpEmail,OTPVerification
from app.core.util.jwt import decode_token
def get_db():
    conn = None
    try:
        conn = DB_CONN()
        yield conn  # pass it to the route
    except Exception as err:
        logging.error(f"Error in get_db: {err}", exc_info=True)
        # re-raise so FastAPI can handle the exception properly
        raise err
    finally:
        if isinstance(conn, DB_CONN):
            conn.close()

router = APIRouter(prefix="/auth/v1", tags=["auth"])
@router.get("/")
def read_root():
    return {"TEXT": "WELCOME TO AUTHENTICATION V1"}
@router.post('/log-in-or-create-account')
def signup(userEmail: SignUpEmail, dbConn: DB_CONN = Depends(get_db)):
    try:
        auth_service = AuthServices(dbConn)
        is_user_exist = auth_service.user_exist(user_id=userEmail.email)

        if is_user_exist:
            raise HTTPException(status_code=400, detail="User already exist")

        otp_service = OTPService(dbConn)
        token = otp_service.send_otp_over_email(to_email=userEmail.email)
        return {"txn_token": token}

    except HTTPException as http_exc:
        # Re-raise so FastAPI can return correct status code and detail
        raise http_exc
    except Exception as err:
        logging.error(f"Unexpected error: {err}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post('/signup/verify_otp')
def signup_verify_otp(submitted_otp:OTPVerification,dbConn:DB_CONN = Depends(get_db)):
    otp_service = OTPService(dbConn)
    try:

        is_valid = otp_service.verify_otp(token = submitted_otp.token,otp=submitted_otp.otp)
        if is_valid:
            return is_valid
        else:
            raise HTTPException(status_code=401, detail="Invalid OTP")
    except Exception as err:
        print(err)
        raise HTTPException(status_code=400, detail="no daa")

@router.post('/signup/create_account')
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
    auth_service = AuthServices(dbConn)
    try:
        token = auth_service.authenticate_user(user_id = user_id,password=password)

        if not token:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"access_token": token, "token_type": "bearer"}

    except ValueError as e:
        logging.error(e)
        raise HTTPException(status_code=401, detail="Invalid credentials")





