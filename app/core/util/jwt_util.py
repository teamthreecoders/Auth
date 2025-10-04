import jwt,logging
from jwt import InvalidSignatureError, ExpiredSignatureError

from app.core.config import JWT_CONFIG
from datetime import  timedelta,timezone
import datetime
from app.exception.exception import MissingArgumentError
def decode_token(token) -> dict:
    try:
        payload = jwt.decode(token, JWT_CONFIG['secret'], algorithms=['HS256'])
        return {
            'is_validated': True,
            'message': 'Successfully decoded',
            'payload': payload
        }

    except ExpiredSignatureError:
        return {
            'is_validated': False,
            'message': 'Token has expired',
            'payload': None
        }

    except InvalidSignatureError:
        return {
            'is_validated': False,
            'message': 'Invalid token signature',
            'payload': None
        }

    except Exception as err:
        return {
            'is_validated': False,
            'message': f'Failed to decode token: {str(err)}',
            'payload': None
        }
    
def generate_token(*,payload:dict = None,exp_time:int = 120) -> str:
    if payload is None:
        raise MissingArgumentError('Payload should not empty')
    payload['exp'] = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(seconds=exp_time)
    token = jwt.encode(payload, JWT_CONFIG['secret'], algorithm='HS256')
    return token
