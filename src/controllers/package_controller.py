from sqlmodel import Session
from fastapi import Depends, APIRouter

from src.database import get_session
from src.services.package_sorter import PackageSorterService
from src.domain.package_request import PackageRequest


router = APIRouter(prefix="/package", tags=["Package"])


def get_package_sorter_service(session: Session = Depends(get_session)) -> PackageSorterService:
    return PackageSorterService(db_session=session)


@router.post("/sort")
def sort_packages(
    request: PackageRequest,
    service: PackageSorterService = Depends(get_package_sorter_service),
):
    return service.sort(
        request.width,
        request.height,
        request.length,
        request.weight,
    )
