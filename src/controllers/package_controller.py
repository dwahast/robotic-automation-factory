from fastapi import Depends, APIRouter
from src.services.package_sorter import PackageSorterService
from src.domain.package_request import PackageRequest


router = APIRouter(prefix="/package", tags=["Package"])


def get_package_sorter_service():
    return PackageSorterService()


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
