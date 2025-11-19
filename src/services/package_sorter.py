from sqlmodel import Session
from src.domain.Entities.package import Package

class PackageSorterService:
    MAX_VOLUME = 1_000_000
    MAX_DIMENSION = 150
    MAX_MASS = 20

    def __init__(self):
        pass

    @staticmethod
    def calculate_volume(width, height, length):
        return width * height * length

    def _package_is_bulky(self, width, height, length):
        package_volume = PackageSorterService.calculate_volume(width, height, length)
        package_max_dimension = max(width, height, length)
        if (
            package_volume >= self.MAX_VOLUME
            or package_max_dimension >= self.MAX_DIMENSION
        ):
            return True

        return False

    def _package_is_heavy(self, mass):
        if mass >= self.MAX_MASS:
            return True

        return False

    def sort(self, session: Session, width, height, length, mass):
        bulky = self._package_is_bulky(width, height, length)
        heavy = self._package_is_heavy(mass)

        if bulky and heavy:
            classification = "REJECTED"
        elif bulky or heavy:
            classification = "SPECIAL"
        else:
            classification = "STANDARD"

        new_package = Package(
             width=width, height=height, length=length, weight=mass, classification=classification)

        session.add(new_package)
        session.commit()
        session.refresh(new_package)

        return classification
