from fastapi import Depends, APIRouter
from src.services.package_sorter import PackageSorterService
from src.domain.package_request import PackageRequest

router = APIRouter(prefix="/package", tags=["Package"])

csv_file_name = "packages.csv"

def get_package_sorter_service():
    return PackageSorterService()

def get_statistics(df, name=None, number_of_artifacts=None):
    print(f"Number of {name} packages: {len(df)}")
    print(f"Percentage {name} of total: {len(df) / number_of_artifacts * 100:.2f}%")
    print(f"{name} Volume Mean:{df['Volume'].mean()}")
    print(f"{name} Volume Min: {df['Volume'].min()}")
    print(f"{name} Volume Max: {df['Volume'].max()}")
    print(f"{name} Mass Mean: {df['Mass'].mean()}")
    print(f"{name} Mass Min: {df['Mass'].min()}")
    print(f"{name} Mass Max: {df['Mass'].max()}")

@router.post("/process/file")
def process_file(service: PackageSorterService = Depends(get_package_sorter_service)):
    # Apply the read logic and proccessment
    df = service.get_df(csv_file_name)
    df["Classification"] = df.apply(service.sort_by_row, axis=1)
    df["Volume"] = df.apply(service.get_volume, axis=1)
    total_artifact = len(df)
    standard_df = df[df["Classification"] == "STANDARD"]
    special_df = df[df["Classification"] == "SPECIAL"]
    rejected_df = df[df["Classification"] == "REJECTED"]

    get_statistics(standard_df, "STANDARD", total_artifact)
    get_statistics(special_df, "SPECIAL", total_artifact)
    get_statistics(rejected_df, "REJECTED", total_artifact)


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
