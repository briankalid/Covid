from fastapi import status as status_codes
from fastapi.responses import JSONResponse
from typing import Any
from pydantic import BaseModel


class EnvelopeResponse(BaseModel):
    status_code: int | None = None
    data: Any | None = None

    def to_json_response(self):
        response_body = {
            "status_code": self.status_code,
            "data": self.data
        }
        return JSONResponse(content=response_body, status_code=self.status_code)