from pydantic import BaseModel, validator, root_validator

from core.settings import settings

class FileFilterSchema(BaseModel):
    
    bucket: str | None = None
    country: str | None = None
    all : bool | None = None

    @validator("all")
    def validate_all_filter(cls, value, values):
        if not values.get("bucket") and not values.get("country"):
            return True
        return False
    
    @root_validator(pre=True)
    def fields_validator(cls, values):
        if values.get("all"):
            values["bucket"] = None
            values["country"] = None

        if values.get("country"):
            if values.get("country") in settings.COUNTRIES:
                values["bucket"] = f"{values.get("country").lower()}-bucket-covidkalid"
            else:
                raise ValueError("Country not valid.")

        return values