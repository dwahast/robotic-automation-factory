from fastapi import Depends, APIRouter

from src.domain.Entities.package import Package
from src.domain.package_request import PackageSortRequest
from src.domain.batch_package_sort_request import BatchPackageSortRequest
from src.services.robotic_arm_service import RoboticArmService
from src.services.report_service import ReportService
from src.database import get_session

router = APIRouter(prefix="/package", tags=["Package"])

csv_file_name = "packages.csv"


def get_robotic_arm_service(session=Depends(get_session)):
    return RoboticArmService(session=session)


def get_report_service():
    return ReportService()


@router.post("/process/file")
def process_file(
        report_service: ReportService = Depends(get_report_service),
        robotic_arm: RoboticArmService = Depends(get_robotic_arm_service)
):
    reports = report_service.process_report_from_file(robotic_arm, csv_file_name)
    return {"reports_created": reports}

@router.post("/sort")
def sort_packages(
        request: PackageSortRequest,
        robotic_arm: RoboticArmService = Depends(get_robotic_arm_service),
):
    package = Package.from_dict(request.model_dump())
    return robotic_arm.sort(package)

@router.post("/sort/batch")
def sort_packages(
        request: BatchPackageSortRequest,
        robotic_arm: RoboticArmService = Depends(get_robotic_arm_service),
):
    # TODO: Register Batch
    for package in request.packages:
        package = Package.from_dict(request.model_dump())
        # TODO: Save on database

    return "Success batch registering: {}"
    # return robotic_arm.sort(package)
