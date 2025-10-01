import  dotenv,os

# loading DOT_ENV
dotenv.load_dotenv()

DB_CONFIG = {
    'conn_string' : {
    'host' : os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user' : os.getenv('DB_USER'),
    'password' : os.getenv('DB_PASS'),
    'database' : os.getenv('DB_NAME')
    },
    'ssl_mode' : os.getenv('DB_SSL'),
    'ca_certificate' : os.getenv('DB_CA')
}

JWT_CONFIG = {
    'secret' : os.getenv('JWT_SECRET') ,
    'algorithm' : os.getenv('JWT_ALGORITHM')
}

EMAIL_CONFIG = {
    'email' : 'teamthreecoders@gmail.com',
    'password' : os.getenv('EMAIL_PASSWORD'),
    'host':os.getenv('EMAIL_HOST'),
    'port':os.getenv('EMAIL_PORT')
}




