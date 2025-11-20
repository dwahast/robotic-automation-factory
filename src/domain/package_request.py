from pydantic import BaseModel, Field


class PackageSortRequest(BaseModel):
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    length: int = Field(gt=0)
    mass: int = Field(gt=0)
