from sqlmodel import Session
from src.domain.Entities.package import Package, PackageEntity
from src.domain.package_enums import PackageClassification


class RoboticArmService:
    def __init__(self, session: Session, max_volume=1_000_000, max_dimension=150, max_mass=20):
        self.db_session: Session = session
        self.MAX_VOLUME = max_volume
        self.MAX_DIMENSION = max_dimension
        self.MAX_MASS = max_mass

    def _package_is_bulky(self, package: Package) -> bool:
        if (
            package.volume >= self.MAX_VOLUME
            or package.max_dimension >= self.MAX_DIMENSION
        ):
            return True

        return False

    def _package_is_heavy(self, package: Package) -> bool:
        if package.mass >= self.MAX_MASS:
            return True

        return False

    def sort(self, package: Package):

        bulky = self._package_is_bulky(package)
        heavy = self._package_is_heavy(package)

        if bulky and heavy:
            classification = PackageClassification.REJECTED
        elif bulky or heavy:
            classification = PackageClassification.SPECIAL
        else:
            classification = PackageClassification.STANDARD

        package.finish(classification)
        package_entity = PackageEntity.from_package(package)

        self.db_session.add(package_entity)
        self.db_session.commit()
        self.db_session.refresh(package_entity)

        return package
