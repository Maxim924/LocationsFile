from sqlalchemy import Column, UUID, String, DateTime, Integer, Float
from database import Base
from datetime import datetime
import uuid

class WalletRecord(Base):
    __tablename__ = "wallet_requests"

    uuid = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    address = Column(String, index=True)
    balance = Column(Float, index=True)
    bandwidth = Column(Integer)
    energy = Column(Integer)
    date_created = Column(DateTime, default=datetime.utcnow)
