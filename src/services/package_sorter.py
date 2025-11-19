import pandas as pd

class PackageSorterService:
    def __init__(self, max_volume=1_000_000, max_dimension=150, max_mass=20):
        self.MAX_VOLUME = max_volume
        self.MAX_DIMENSION = max_dimension
        self.MAX_MASS = max_mass

    def _calculate_volume(self, width, height, length):
        return width * height * length

    def _package_is_bulky(self, width, height, length):
        package_volume = self._calculate_volume(width, height, length)
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

    def get_df(self, filename: str):
        df = pd.read_csv(filename, on_bad_lines='skip')
        # Convert everything to numeric (integers), coercing errors to NaN
        df = df.apply(pd.to_numeric, errors='coerce')

        # Drop rows or columns with NaN
        df = df.dropna()  # drops rows with any NaN
        df = df.astype(int)  # finally convert to int
        df = df[(df > 0).all(axis=1)]
        return df


    def get_volume(self, row):
        width = row["Width"]
        height = row["Height"]
        length = row["Length"]
        return self._calculate_volume(width, height, length)

    def sort_by_row(self, row):
        width = row["Width"]
        height = row["Height"]
        length = row["Length"]
        mass = row["Mass"]

        return self.sort(int(width), int(height), int(length), int(mass))

    def sort(self, width, height, length, mass):
        bulky = self._package_is_bulky(width, height, length)
        heavy = self._package_is_heavy(mass)
        print(f"Bulky: {bulky} | Heavy: {heavy}")
        if bulky and heavy:
            return "REJECTED"
        elif bulky or heavy:
            return "SPECIAL"
        else:
            return "STANDARD"
