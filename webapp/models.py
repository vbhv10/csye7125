from sqlalchemy import Column, Integer, String, Boolean, DateTime, UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class HttpCheck(Base):
    __tablename__ = "http_checks"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    uri = Column(String, nullable=False)
    is_paused = Column(Boolean, default=False)
    num_retries = Column(Integer, nullable=False)
    uptime_sla = Column(Integer, nullable=False)
    response_time_sla = Column(Integer, nullable=False)
    use_ssl = Column(Boolean, default=True)
    response_status_code = Column(Integer, nullable=False)
    check_interval_in_seconds = Column(Integer, nullable=False)
    check_created = Column(DateTime, default=datetime.utcnow)
    check_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "uri": self.uri,
            "is_paused": self.is_paused,
            "num_retries": self.num_retries,
            "uptime_sla": self.uptime_sla,
            "response_time_sla": self.response_time_sla,
            "use_ssl": self.use_ssl,
            "response_status_code": self.response_status_code,
            "check_interval_in_seconds": self.check_interval_in_seconds,
            "check_created": self.check_created,
            "check_updated": self.check_updated
        }
    