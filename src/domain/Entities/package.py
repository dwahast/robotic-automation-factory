import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy.sql import func

from src.domain.package import Package
from src.domain.package_enums import PackageStatus


class TimestampMixin(SQLModel):
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC))
    updated_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC))

class PackageEntity(TimestampMixin, table=True):
    __tablename__ = "package"

    id: int | None = Field(default=None, primary_key=True)
    batch_id: int | None = Field(default=None)
    batch_name: str | None = Field(default=None)
    status: str | None = Field(default=PackageStatus.PENDING)
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    length: int = Field(gt=0)
    mass: int = Field(gt=0)
    max_dimension: int | None = Field(gt=0)
    volume: int | None = Field(gt=0)
    classification: str | None = Field(default=None, nullable=True)
    finished_at: datetime.datetime | None = None

    @classmethod
    def from_package(cls, package: Package):
        return cls(
            batch_id=package.batch_id,
            batch_name=package.batch_name,
            status=package.status,
            width=package.width,
            height=package.height,
            length=package.length,
            mass=package.mass,
            max_dimension=package.max_dimension,
            volume=package.volume,
            classification=package.classification,
            finished_at=package.finished_at,
        )






