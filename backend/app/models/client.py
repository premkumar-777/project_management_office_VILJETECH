# from sqlalchemy import Column, Integer, String, TIMESTAMP
# from app.database import Base
# from sqlalchemy.sql import func

# class Client(Base):
#     __tablename__ = "clients"

#     id = Column(Integer, primary_key=True)
#     name = Column(String(100))
#     email = Column(String(150), unique=True, index=True)
#     password_hash = Column(String(255))
#     status_id = Column(Integer)
#     created_by = Column(Integer)
#     deleted_by = Column(Integer)
#     created_at = Column(TIMESTAMP, server_default=func.now())
#     updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True)
    password_hash = Column(String(255))
    status_id = Column(Integer)
    created_by = Column(Integer)
    deleted_by = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
