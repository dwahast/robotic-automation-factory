from src.domain.Entities.package import Package

# -----------------------------
# Tests for utility functions
# -----------------------------
def test_calculate_volume():
    package = Package(width=200, height=10, length=10, mass=5)
    assert package.volume == 20000
