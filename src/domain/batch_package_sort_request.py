from typing import List

from pydantic import BaseModel, Field
from src.domain.package_request import PackageSortRequest

class BatchPackageSortRequest(BaseModel):
    batch_id: int
    batch_name: str
    packages: List[PackageSortRequest] = Field(default_factory=list)
