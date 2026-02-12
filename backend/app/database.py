# # app/database.py
# import os
# import urllib.parse
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Encode password for special characters
# password = urllib.parse.quote_plus(os.getenv("DB_PASSWORD"))

# # Database URL
# DATABASE_URL = (
#     f"mysql+pymysql://{os.getenv('DB_USER')}:{password}"
#     f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
# )

# # Create engine
# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"ssl": {"ssl_disabled": False}}  # Azure requires SSL
# )

# # SessionLocal for ORM usage
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base class for ORM models
# Base = declarative_base()

# # Optional: helper for raw queries
# def get_connection():
#     return engine.connect()



import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Local DB credentials
DB_USER = "root"
DB_PASSWORD = "Ponnadas#123"
DB_HOST = "localhost"
DB_NAME = "pmo_test_db"
DB_PORT = "3306"
# ------------------------------
# DB dependency
# ------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Encode password safely
password = urllib.parse.quote_plus(DB_PASSWORD)

# Connection URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # avoids "MySQL server has gone away"
)

# Session and Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
