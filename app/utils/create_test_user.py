from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from database import SessionLocal, engine, Base
from models import User


def create_test_user():
    db: Session = SessionLocal()
    try:
        Base.metadata.create_all(bind=engine)
        is_user = db.query(User).filter_by(username="test").first()
        if is_user:
            print("Пользователь уже существует")
        else:
            pasword_hash = generate_password_hash('test')
            test_user = User(username="test", password_hash=pasword_hash)
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            print(f"Создан пользователь с ID: {test_user.id}")
    except Exception as e:
        print(f"Ошибка: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_test_user()
