from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
import os

from database import get_db
from models import User

auth = HTTPBasicAuth()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORE_DIR = os.path.join(BASE_DIR, '..', 'store')


@auth.verify_password
def verify_password(username, password):
    db = next(get_db())
    user = db.query(User).filter(User.username == username).first()
    if user and check_password_hash(user.password_hash, password):
        return username
    return None


def get_file_path(file_hash, file_extension=""):
    return os.path.join(STORE_DIR, file_hash[:2], file_hash + file_extension)


def find_file_by_hash(file_hash):
    dir_path = os.path.dirname(get_file_path(file_hash))
    for filename in os.listdir(dir_path):
        if os.path.splitext(filename)[0] == file_hash:
            return os.path.join(dir_path, filename)
    return None
