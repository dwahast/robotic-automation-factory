import pytest

from unittest.mock import MagicMock

from src.domain.Entities.package import Package
from src.services.robotic_arm_service import RoboticArmService

@pytest.fixture
def mock_session():
    session = MagicMock()
    # Optional: mock methods like add, commit, query, refresh
    session.add = MagicMock()
    session.commit = MagicMock()
    session.refresh = MagicMock()
    return session

@pytest.fixture
def robotic_arm(mock_session):
    return RoboticArmService(session=mock_session)


# -----------------------------
# Tests for utility functions
# -----------------------------
def test_package_is_bulky_by_volume(robotic_arm):
    # volume = 100 * 100 * 100 = 1_000_000 -> bulky
    package = Package(width=100, length=100, height=100, mass=5)
    assert robotic_arm._package_is_bulky(package) is True


def test_package_is_bulky_by_dimension(robotic_arm):
    # max dimension >= 150
    package = Package(width=10, length=200, height=10, mass=5)
    assert robotic_arm._package_is_bulky(package) is True


def test_package_is_not_bulky(robotic_arm):
    package = Package(width=10, length=10, height=10, mass=5)
    assert robotic_arm._package_is_bulky(package) is False


def test_package_is_heavy(robotic_arm):
    package = Package(width=10, length=10, height=10, mass=25)
    assert robotic_arm._package_is_heavy(package) is True


def test_package_is_not_heavy(robotic_arm):
    package = Package(width=10, length=10, height=10, mass=5)
    assert robotic_arm._package_is_heavy(package) is False


# -----------------------------
# Tests for robotic_arm logic
# -----------------------------
def test_sort_standard(robotic_arm):
    package = Package(width=10, height=10, length=10, mass=5)
    assert robotic_arm.sort(package).classification == "STANDARD"


def test_sort_special_bulky_only(robotic_arm):
    package = Package(width=200, height=10, length=10, mass=5)
    assert robotic_arm.sort(package).classification == "SPECIAL"


def test_sort_special_heavy_only(robotic_arm):
    package = Package(width=10, height=10, length=10, mass=25)
    assert robotic_arm.sort(package).classification == "SPECIAL"


def test_sort_rejected(robotic_arm):
    # bulky (dimension 200) AND heavy (mass 25)
    package = Package(width=200, height=10, length=10, mass=25)
    assert robotic_arm.sort(package).classification == "REJECTED"
