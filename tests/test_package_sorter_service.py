import pytest
from src.services.package_sorter import PackageSorterService


@pytest.fixture
def sorter():
    return PackageSorterService()


# -----------------------------
# Tests for utility functions
# -----------------------------
def test_calculate_volume(sorter):
    assert sorter._calculate_volume(10, 10, 10) == 1000
    assert sorter._calculate_volume(1, 1, 1) == 1


def test_package_is_bulky_by_volume(sorter):
    # volume = 100 * 100 * 100 = 1_000_000 -> bulky
    assert sorter._package_is_bulky(100, 100, 100) is True


def test_package_is_bulky_by_dimension(sorter):
    # max dimension >= 150
    assert sorter._package_is_bulky(10, 200, 10) is True


def test_package_is_not_bulky(sorter):
    assert sorter._package_is_bulky(10, 10, 10) is False


def test_package_is_heavy(sorter):
    assert sorter._package_is_heavy(25) is True


def test_package_is_not_heavy(sorter):
    assert sorter._package_is_heavy(5) is False


# -----------------------------
# Tests for sorter logic
# -----------------------------
def test_sort_standard(sorter):
    assert sorter.sort(10, 10, 10, 5) == "STANDARD"


def test_sort_special_bulky_only(sorter):
    assert sorter.sort(200, 10, 10, 5) == "SPECIAL"


def test_sort_special_heavy_only(sorter):
    assert sorter.sort(10, 10, 10, 25) == "SPECIAL"


def test_sort_rejected(sorter):
    # bulky (dimension 200) AND heavy (mass 25)
    assert sorter.sort(200, 10, 10, 25) == "REJECTED"
