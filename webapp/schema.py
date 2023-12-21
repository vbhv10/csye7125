from pydantic import BaseModel, HttpUrl, Field
from fastapi import status

class CustomException(Exception):
    def __init__(self, status_code, msg):
        self.status_code = status_code
        self.msg = msg

class HttpCheck(BaseModel):

    def __init__(self, **data):
        for key, value in data.items():
            
            if key in ["num_retries", "uptime_sla", "response_time_sla", "response_status_code", "check_interval_in_seconds"] and (isinstance(value, str) or isinstance(value, float)):
                raise CustomException(status.HTTP_400_BAD_REQUEST, {key: "The value should be Integer"})
        super().__init__(**data)

    name: str
    uri: HttpUrl
    is_paused: bool
    num_retries: int = Field(ge=1, le=5)
    uptime_sla: int = Field(ge=0, le=100)
    response_time_sla: int = Field(ge=0, le=100)
    use_ssl: bool
    response_status_code: int = 200
    check_interval_in_seconds: int = Field(ge=1, le=86400)