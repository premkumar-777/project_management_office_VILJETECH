import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -----------------------------
# Local DB credentials
# -----------------------------
DB_USER = "root"
DB_PASSWORD = "Ponnadas#123"
DB_HOST = "localhost"
DB_NAME = "pmo_test_db"
DB_PORT = "3306"

# Encode password for special characters
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

# FastAPI dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# import os
# import urllib.parse
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST")
# DB_NAME = os.getenv("DB_NAME")
# DB_PORT = os.getenv("DB_PORT", "3306")  # default MySQL port

# # Encode password safely
# password = urllib.parse.quote_plus(DB_PASSWORD)

# # Azure connection URL
# DATABASE_URL = f"mysql+pymysql://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# # Create engine with SSL
# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"ssl": {"ssl_disabled": False}},  # required by Azure
#     pool_pre_ping=True
# )

# # Session and Base
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # FastAPI dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
