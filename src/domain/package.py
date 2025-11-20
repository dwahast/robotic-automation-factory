import datetime
from pydantic import BaseModel, Field
from src.domain.package_enums import PackageStatus


class Package(BaseModel):
    id: int | None = None
    batch_id: int | None = None
    batch_name: str | None = None

    status: str | None = Field(default=PackageStatus.PENDING)

    width: int = Field(gt=0)
    height: int = Field(gt=0)
    length: int = Field(gt=0)
    mass: int = Field(gt=0)

    max_dimension: int | None = None
    volume: int | None = None

    classification: str | None = None
    finished_at: datetime.datetime | None = None

    def model_post_init(self, __context):
        self.max_dimension = max(self.width, self.height, self.length)
        self.volume = self.width * self.height * self.length

    def finish(self, classification: str):
        self.status = PackageStatus.FINISHED
        self.classification = classification
        self.finished_at = datetime.datetime.now(datetime.UTC)

    @classmethod
    def from_dict(cls, request: dict):
        lower_request = {k.lower(): v for k, v in request.items()}
        return cls(
            width=int(lower_request["width"]),
            height=int(lower_request["height"]),
            length=int(lower_request["length"]),
            mass=int(lower_request["mass"]),
        )