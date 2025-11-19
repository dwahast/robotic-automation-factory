
from sqlmodel import Field, SQLModel, create_engine, select

class Package(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    length: int = Field(gt=0)
    weight: int = Field(gt=0)
    classification: str | None = Field(default=None, nullable=True)




