from datetime import datetime


class ExtractorValidator:
    @staticmethod
    def validate_dates(start_date: str, end_date: str) -> bool:
        if not start_date or not end_date:
            return False
        start_dt = datetime.strptime(start_date, "%d/%m/%Y")
        end_dt = datetime.strptime(end_date, "%d/%m/%Y")
        return start_dt < end_dt

    @staticmethod
    def validate_percentages(min_percent: str, max_percent: str) -> bool:
        if not min_percent or not max_percent:
            return False
        min_val = int(min_percent.rstrip("%"))
        max_val = int(max_percent.rstrip("%"))
        return 0 <= min_val <= max_val <= 100

    @staticmethod
    def validate_amount(amount: str) -> bool:
        if not amount:
            return False
        return int(amount) > 0

    @staticmethod
    def validate_dates(start_date: str, end_date: str) -> bool:
        if not start_date or not end_date:
            return False
        start = datetime.strptime(start_date, "%d/%m/%Y")
        end = datetime.strptime(end_date, "%d/%m/%Y")
        return start <= end
