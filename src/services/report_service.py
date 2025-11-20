import datetime

import pandas as pd

from src.services.package_sorter import PackageSorterService


class ReportService:
    def __init__(self):
        pass

    def _get_df(self, filename: str):
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
            {'description': f'Number of {name} packages', 'value': len(df)},
            {'description': f'Percentage {name} of total', 'value': len(df) / number_of_artifacts * 100},
            {'description': f'{name} Volume Mean', 'value': df['Volume'].mean()},
            {'description': f'{name} Volume Min', 'value': df['Volume'].min()},
            {'description': f'{name} Volume Max', 'value': df['Volume'].max()},
            {'description': f'{name} Mass Mean', 'value': df['Mass'].mean()},
            {'description': f'{name} Mass Min', 'value': df['Mass'].min()},
            {'description': f'{name} Mass Max', 'value': df['Mass'].max()},
        ]

        stats_df = pd.DataFrame(data)
        file_name = f"package_report_{name}_{datetime.datetime.now()}.csv"
        stats_df.to_csv(file_name, index=False)
        print(f"Report created: {file_name}")
        return stats_df

    def process_report(self, package_service: PackageSorterService, filename: str):
        df = self._get_df(filename)
        df["Classification"] = df.apply(package_service.sort_by_row, axis=1)
        df["Volume"] = df.apply(package_service.get_volume, axis=1)
        total_artifact = len(df)

        for cls, subset in df.groupby("Classification"):
            self.generate_reports(subset, cls, total_artifact)
