from pwdlib import PasswordHash
import os
from dotenv import load_dotenv
from jose import jwt
ALGORITHM = "HS256"
load_dotenv()
from datetime import datetime, timedelta

JWT_SECRET = os.getenv('JWT_SECRET')
password_hash = PasswordHash.recommended()

def create_access_token(user_id : int):
    to_encode = {"user_id": user_id, "exp": datetime.now() + timedelta(minutes=30)}
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return token
