import bcrypt
from app.exception.exception import MissingArgumentError

class HashPassword:
    @staticmethod
    def hash_password(password:str = None) -> str:
        if password  ==  None:
            raise ValueError('Password should not be empty')
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def verify_password(password:str = None, hashed_password:str = None) -> bool:
        if password  ==  None:
            raise MissingArgumentError('Password should not be empty')
        if hashed_password  ==  None:
            raise MissingArgumentError('Hashed password should not be empty')
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))



