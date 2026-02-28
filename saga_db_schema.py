from sqlalchemy import Column, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from enum import Enum

Base = declarative_base()

class SagaStatus(str, Enum):
    UNFINISHED = "unfinished"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class SagaOrder(Base):
    __tablename__ = 'order_sagas'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), nullable=False)

    order_id = Column(UUID(as_uuid=True))

    order_cancelled = Column(Boolean, default=False, nullable=False)

    payment_id = Column(UUID(as_uuid=True))

    payment_cancelled = Column(Boolean, default=False, nullable=False)

    reservation_id = Column(UUID(as_uuid=True))

    reservation_cancelled = Column(Boolean, default=False, nullable=False)

    delivery_id = Column(UUID(as_uuid=True))

    delivery_cancelled = Column(Boolean, default=False, nullable=False)

    status = Column(SQLEnum(SagaStatus), nullable=False, default=SagaStatus.UNFINISHED)
    # Метка времени, чтобы отделять зависшие саги от идущих здесь и сейчас в потенциальном "разгребателе" 
    last_updated = Column(DateTime, nullable=False, default=datetime.utcnow())

