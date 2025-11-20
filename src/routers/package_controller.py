from fastapi import Depends, APIRouter
from src.services.package_sorter import PackageSorterService
from src.domain.package_request import PackageRequest
from src.services.report_service import ReportService

router = APIRouter(prefix="/package", tags=["Package"])

csv_file_name = "packages.csv"


def get_package_sorter_service():
    return PackageSorterService()


def get_report_service():
    return ReportService()


@router.post("/process/file")
def process_file(report_service: ReportService = Depends(get_report_service),
                 service: PackageSorterService = Depends(get_package_sorter_service)):
    reports = report_service.process_report_from_file(service, csv_file_name)
    # TODO: save reports on database. Apply cache to save processing time.
    #  Receive data from REST API, and increment the packages by batches
    return {"reports_created": reports}

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
