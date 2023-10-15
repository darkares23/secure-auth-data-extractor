import re
from datetime import datetime
from typing import Dict, Optional

from dateutil.relativedelta import relativedelta

from auth_data_extractor.data_extractor.base_extractor import DataExtractorStrategy
from auth_data_extractor.data_extractor.extractor_validator import ExtractorValidator


class InitialContributionPeriodExtractor(DataExtractorStrategy):
    CONTRACT_PERIOD_PATTERN = re.compile(r"shall commence on (\w+ \d+, \d+), and shall end on (\w+ \d+, \d+)")
    CONTRIBUTION_PATTERN = re.compile(r"not less than (?P<min_percent>\d+)% and not more than (?P<max_percent>\d+)%")

    @staticmethod
    def format_date(date: str) -> str:
        dt = datetime.strptime(date, "%B %d, %Y")
        return dt.strftime("%d/%m/%Y")

    def extract_data(self, text: str) -> Dict[str, Optional[str]]:
        try:
            contract_period_match = self.CONTRACT_PERIOD_PATTERN.search(text)
            contribution_match = self.CONTRIBUTION_PATTERN.search(text)

            start_date_str = self.format_date(contract_period_match.group(1)) if contract_period_match else None
            end_date_str = self.format_date(contract_period_match.group(2)) if contract_period_match else None

            if not ExtractorValidator.validate_dates(start_date_str, end_date_str):
                raise ValueError("Invalid date range")

            extracted_data = {
                "start_date": start_date_str,
                "end_date": end_date_str,
                "min_percent": f"{contribution_match.group('min_percent')}%" if contribution_match else None,
                "max_percent": f"{contribution_match.group('max_percent')}%" if contribution_match else None,
            }

            if not ExtractorValidator.validate_percentages(
                extracted_data["min_percent"], extracted_data["max_percent"]
            ):
                raise ValueError("Invalid percentage range")

            return extracted_data
        except Exception as e:
            return {"error": str(e)}


class OfferingPeriodExtractor(DataExtractorStrategy):
    """Strategy for extracting data from Input 2 type texts."""

    OFFERING_START_PATTERN = re.compile(r"commence as of (\w+ \d+, \d+)")
    CONTRIBUTION_PATTERN = re.compile(
        r"not exceed \$(?P<max_amount>[\d,]+) per Offering Period|percent \((?P<max_percent>\d{1,2}|100)%\) of Participant’s Compensation"
    )

    @staticmethod
    def format_date(date: str) -> str:
        """Convert a date from 'Month Day, Year' or 'Month Day' to 'Day/Month/Year'."""
        if "," in date:  # Check if year is provided
            dt = datetime.strptime(date, "%B %d, %Y")
        else:
            dt = datetime.strptime(date + f", {datetime.now().year}", "%B %d, %Y")  # Assuming the current year
        return dt.strftime("%d/%m/%Y")

    def extract_data(self, text: str) -> Dict[str, Optional[str]]:
        try:
            offering_start_match = self.OFFERING_START_PATTERN.search(text)
            contribution_matches = list(self.CONTRIBUTION_PATTERN.finditer(text))

            if offering_start_match:
                start_date_str = self.format_date(offering_start_match.group(1))
                start_date_obj = datetime.strptime(start_date_str, "%d/%m/%Y")
                end_date_obj = start_date_obj + relativedelta(months=3)  # Adding 3 months
                end_date_str = end_date_obj.strftime("%d/%m/%Y")
            else:
                start_date_str = None
                end_date_str = None

            max_percent = None
            max_amount = None
            for match in contribution_matches:
                if not max_amount and match.group("max_amount"):
                    max_amount = match.group("max_amount").replace(",", "")
                if not max_percent and match.group("max_percent"):
                    max_percent = f"{match.group('max_percent')}%"

            extracted_data = {
                "start_date": start_date_str,
                "end_date": end_date_str,
                "min_percent": "1%",
                "max_percent": max_percent,
                "max_amount": max_amount,
            }

            if not ExtractorValidator.validate_dates(extracted_data["start_date"], extracted_data["end_date"]):
                raise ValueError("Invalid date range")
            if not ExtractorValidator.validate_percentages(
                extracted_data["min_percent"], extracted_data["max_percent"]
            ):
                raise ValueError("Invalid percentage range")
            if extracted_data["max_amount"] and not ExtractorValidator.validate_amount(extracted_data["max_amount"]):
                raise ValueError("Invalid amount")

            return extracted_data
        except Exception as e:
            return {"error": str(e)}


class SuccessiveOfferingPeriodExtractor(DataExtractorStrategy):
    """Strategy for extracting data from Input 3 type texts."""

    INITIAL_OFFERING_END_PATTERN = re.compile(
        r"end on the last Trading Day on or immediately preceding (\w+ \d+)(, \d+)?"
    )
    CONTRIBUTION_PATTERN = re.compile(r"\((\d{1,2}|100)%\)")

    @staticmethod
    def format_date(date: str, year: int = None) -> str:
        """Convert a date from 'Month Day, Year' or 'Month Day' to 'Day/Month/Year'."""
        if not year:
            year = datetime.now().year
        try:
            dt = datetime.strptime(date, "%B %d, %Y")
        except ValueError:
            dt = datetime.strptime(f"{date} {year}", "%B %d %Y")
        return dt.strftime("%d/%m/%Y")

    def extract_data(self, text: str) -> Dict[str, Optional[str]]:
        try:
            initial_end_match = self.INITIAL_OFFERING_END_PATTERN.search(text)

            if initial_end_match.group(2):
                end_date_str = self.format_date(initial_end_match.group(1) + initial_end_match.group(2))
            else:
                end_date_str = self.format_date(initial_end_match.group(1)) if initial_end_match else None

            # If there's an end date, we calculate the start date as the 14th of the month, six months prior.
            if end_date_str:
                end_date_dt = datetime.strptime(end_date_str, "%d/%m/%Y")
                start_month = (end_date_dt.month - 6) % 12 or 12
                start_year = end_date_dt.year if end_date_dt.month > 6 else end_date_dt.year - 1
                start_date_str = datetime(start_year, start_month, 14).strftime("%d/%m/%Y")
            else:
                start_date_str = None

            # Extracting max percent directly using the pattern
            contribution_match = self.CONTRIBUTION_PATTERN.search(text)
            max_percent = contribution_match.group(1) + "%" if contribution_match else None

            extracted_data = {
                "start_date": start_date_str,
                "end_date": end_date_str,
                "min_percent": "1%",
                "max_percent": max_percent,
            }

            if not ExtractorValidator.validate_dates(extracted_data["start_date"], extracted_data["end_date"]):
                raise ValueError("Invalid date range")
            if not ExtractorValidator.validate_percentages(
                extracted_data["min_percent"], extracted_data["max_percent"]
            ):
                raise ValueError("Invalid percentage range")
            if not ExtractorValidator.validate_dates(start_date_str, end_date_str):
                raise ValueError("Invalid date range")

            return extracted_data
        except Exception as e:
            return {"error": str(e)}
