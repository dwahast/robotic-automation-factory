from pydantic import BaseModel, Field


class PackageRequest(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    length: int = Field(gt=0)
    weight: int = Field(gt=0)
