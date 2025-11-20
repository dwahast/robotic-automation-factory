import datetime
from sqlmodel import Field, SQLModel

from src.domain.batch_enums import BatchStatus

class PackageEntity(SQLModel, table=True):
    __tablename__ = "batch_package"

    batch_id: int | None = Field(default=None, primary_key=True)
    batch_name: str | None = Field(default=None)
    status: str | None = Field(default=BatchStatus.PENDING)
    number_of_packages: int = Field(default=0)
    process_time: datetime.timedelta | None = Field(default=None)
    received_at: datetime.datetime | None = Field(default=None)
    finished_at: datetime.datetime | None = Field(default=None)
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC))


    def from_dict(self, data: dict):
        pass

