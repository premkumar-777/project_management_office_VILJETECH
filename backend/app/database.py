

# import os
# import urllib.parse
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from dotenv import load_dotenv

# load_dotenv()

# # Load environment variables 

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



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib.parse

# -----------------------------
# Local DB credentials
# -----------------------------
DB_USER = "root"
DB_PASSWORD = "@#Qwerty123#@"
DB_HOST = "localhost"
DB_NAME = "pmo_db"
DB_PORT = "3306"

# Encode password (because it has special characters)
password = urllib.parse.quote_plus(DB_PASSWORD)

# MySQL connection string
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine FIRST
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Then create SessionLocal
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base model
Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Email: superadmin@pmo.com
#Password: Admin@123        