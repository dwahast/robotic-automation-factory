import datetime

import pandas as pd

from src.domain.Entities.package import Package
from src.services.robotic_arm_service import RoboticArmService


class ReportService:
    def __init__(self):
        pass

    @staticmethod
    def get_df_from_file(filename: str):
        df = pd.read_csv(filename, on_bad_lines='skip')
        # Convert everything to numeric (integers), coercing errors to NaN
        df = df.apply(pd.to_numeric, errors='coerce')

        # Drop rows or columns with NaN
        df = df.dropna()  # drops rows with any NaN
        df = df.astype(int)  # finally convert to int
        df = df[(df > 0).all(axis=1)]
        return df

    @staticmethod
    def generate_reports(df, name=None, number_of_artifacts=None):
        data = [
            {'description': f'classification', 'value': name},
            {'description': f'number_of_packages', 'value': len(df)},
            {'description': f'percentage_of_total', 'value': len(df) / number_of_artifacts * 100},
            {'description': f'volume_mean', 'value': df['Volume'].mean()},
            {'description': f'volume_min', 'value': df['Volume'].min()},
            {'description': f'volume_max', 'value': df['Volume'].max()},
            {'description': f'mass_mean', 'value': df['Mass'].mean()},
            {'description': f'mass_min', 'value': df['Mass'].min()},
            {'description': f'mass_max', 'value': df['Mass'].max()},
        ]

        stats_df = pd.DataFrame(data)
        file_name = f"package_report_{name}_{datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}.csv"
        stats_df.to_csv(file_name, index=False, header=True)
        print(f"Report created: {file_name}")
        return file_name

    @staticmethod
    def classifier(row: pd.Series, robotic_arm: RoboticArmService):
        package = Package.from_dict(row)
        sorted_package = robotic_arm.sort(package)

        return pd.Series({
            "Classification": sorted_package.classification,
            "Volume": sorted_package.volume
        })

    def process_report_from_file(self, robotic_arm: RoboticArmService, filename: str):
        df = ReportService.get_df_from_file(filename)

        # 1. Classify Packages
        df[["Classification", "Volume"]] = df.apply(
            lambda row: ReportService.classifier(row, robotic_arm), axis=1)

        # 3. Generate Reports on Classification subsets
        reports_created = []
        for cls, subset in df.groupby("Classification"):
            reports_created.append(self.generate_reports(subset, cls, len(df)))

        return reports_created
