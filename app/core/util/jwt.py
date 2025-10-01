import jwt,logging
from app.core.config import JWT_CONFIG
from datetime import  timedelta,timezone
import datetime
def decode_token(token) -> dict:
    try:
        payload = jwt.decode(token, JWT_CONFIG['secret'] , algorithms=['HS256'])
        return payload
    except Exception as e:
        logging.error('Verify_token',e)
        return {"payload":""}

def generate_token(*,payload:dict = None,exp_time:int = 120) -> str:
    if payload is None:
        raise ValueError('Payload should not empty')
    payload['exp'] = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(seconds=exp_time)
    token = jwt.encode(payload, JWT_CONFIG['secret'], algorithm='HS256')
    return token