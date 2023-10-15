from django.test import TestCase

from auth_data_extractor.data_extractor.imput_extractor import (
    InitialContributionPeriodExtractor,
    OfferingPeriodExtractor,
    SuccessiveOfferingPeriodExtractor,
)


class TestInitialContributionPeriodExtractor(TestCase):
    def setUp(self):
        self.extractor = InitialContributionPeriodExtractor()

    def test_valid_extraction(self):
        text = """
            - Initial Contribution Periods. Subject to the following paragraph (b),
            the Plan shall be implemented by a series of consecutive Contribution Periods
            commencing on January 1 and July 1 each year and ending on the following June 30
            and December 31, respectively. The first Contribution Period under this Plan
            shall commence on July 1, 2010, and shall end on December 31, 2010. The Plan
            shall continue until terminated in accordance with Section 13 or Section 19.
            - Changes. The Committee shall have the power to change the duration and/or
            frequency of Contribution Periods with respect to future purchases of Shares,
            without shareholder approval, if such change is announced to all Employees who
            are eligible under Section 3 at least five Business Days before the Commencement
            Date of the first Contribution Period to be affected by the change; provided,
            however, that no Contribution Period shall exceed 27 months.
            - Contribution Amounts. Subject to the limitations of Sections 3(b) and 11, a
            Participant shall elect to have Contributions made as payroll deductions on each
            payday during the Contribution Period in any percentage of his or her
            Compensation that is not less than 1% and not more than 15% (or such other
            maximum percentage as the Committee may establish from time to time before any
            Commencement Date) of such Participant’s Compensation on each payday during
            the Contribution Period. Contribution amounts shall be withheld in whole percentages only.
        """
        expected_output = {
            "start_date": "01/07/2010",
            "end_date": "31/12/2010",
            "min_percent": "1%",
            "max_percent": "15%",
        }
        result = self.extractor.extract_data(text)
        self.assertEqual(result, expected_output)


class TestOfferingPeriodExtractor(TestCase):
    def setUp(self):
        self.extractor = OfferingPeriodExtractor()

    def test_not_valid_max_amount_extraction(self):
        text = """
        “Offering Period” means a period of time specified by the Administrator, consistent with Section
        423 of the Code, beginning on the Offer Date and ending on the Acquisition Date. Unless otherwise
        determined by the Administrator, each Offering Period shall be a period of three (3) calendar months
        commencing on January 1, April 1, July 1 and October 1 of each calendar year during the Term of
        the Plan. The first Offering Period under the Plan shall commence as of July 1, 2021.
        Enrollment. An eligible Employee may become a Participant in the Plan by completing an enrollment
        election form and any other required enrollment documents provided by the Administrator or its designee
        and submitting them to the Administrator or its designee prior to the commencement of an Offering Period
        in accordance with the rules established by the Administrator. The enrollment documents,
        which may, in the discretion of the Administrator, be in electronic form, shall set forth
        he amount of the Participant’s Compensation in whole dollars, which may not exceed $ per
        Offering Period (or such other amount as may be prescribed by the Administrator from time to
        time) or forty percent (20%) of Participant’s Compensation per Offering Period (or such other
        percentage as may be prescribed by the Administrator from time to time), to be paid as Contributions
        pursuant to the Plan. An Employee’s payroll enrollment election shall become effective on an Offer
        Date in accordance with the rules established by the Administrator. Amounts deducted from a
        Participant’s Compensation pursuant to this Article V shall be credited to the Participant’s Plan percent
        (25%) account. No interest shall be payable on the amounts credited to the Participant’s Plan account.
        After an eligible Employee has become a Participant in the Plan for an Offering Period, the Participant’s
        payroll authorization for that Offering Period shall continue in force and effect for that
        Offering Period, unless the Participant withdraws from the Plan or the Administrator
        permits any such change during the Offering Period and the Participant changes such election in
        accordance with the procedures established by the Administrator.
        """

        expected_output = {
            "start_date": "01/07/2021",
            "end_date": "01/10/2021",
            "min_percent": "1%",
            "max_percent": "20%",
            "max_amount": None,
        }
        result = self.extractor.extract_data(text)
        self.assertEqual(result, expected_output)


class TestSuccessiveOfferingPeriodExtractor(TestCase):
    def setUp(self):
        self.extractor = SuccessiveOfferingPeriodExtractor()

    def test_valid_extraction(self):
        text = """
            - Frequency and Duration. The Administrator may establish Offering Periods
            of such frequency and duration as it may from time to time determine as appropriate.
            - First Offering Period. The first Offering Period under the Plan shall commence on
            the IPO Date and shall end on the last Trading Day on or immediately preceding May 14, 2020.
            - Successive Offering Periods. Unless the Administrator determines otherwise, following
            the completion of the first Offering Period, a new Offering Period shall commence on
            the first Trading Day on or following May 15 and November 15 of each calendar year
            and end on or following the last Trading Day on or immediately preceding November
            14 and May 14, respectively, approximately six (6) months later.
            - At the time a Participant enrolls in the Plan pursuant to Section 5 of the Plan,
            he or she will elect to have Contributions (in the form of payroll deductions
            or otherwise, to the extent permitted by the Administrator) made on each pay day
            during the Offering Period in an amount not exceeding fifteen percent (15%) of the
            Compensation, which he or she receives on each pay day during the Offering Period
            (for illustrative purposes, should a pay day occur on an Exercise Date, a Participant
            will have any payroll deductions made on such day applied to his or her account under
            the then-current Purchase Period or Offering Period). The Administrator, in its sole discretion,
            may permit all Participants in a specified Offering to contribute amounts to the Plan
            through payment by cash, check or other means set forth in the subscription agreement
            prior to each Exercise Date of each Purchase Period. A Participant’s subscription agreement
            will remain in effect for successive Offering Periods unless terminated as provided in Section 10 hereof.
        """
        expected_output = {
            "start_date": "14/11/2019",  # Six months prior to May 14, 2020
            "end_date": "14/05/2020",
            "min_percent": "1%",
            "max_percent": "15%",
        }
        result = self.extractor.extract_data(text)
        self.assertEqual(result, expected_output)

    def test_invalid_extraction(self):
        text = """
            -  Unless the Administrator determines otherwise, following
            the completion of the first Offering Period, a new Offering Period shall commence on
            the first Trading Day on or following May 15 and November 15 of each calendar year
            and end on or following the last Trading Day on or immediately preceding November
            14 and May 14, respectively, approximately six (6) months later.
            - At the time a Participant enrolls in the Plan pursuant to Section 5 of the Plan,
            he or she will elect to have Contributions (in the form of payroll deductions
            or otherwise, to the extent permitted by the Administrator) made on each pay day
            during the Offering Period in an amount not exceeding fifteen percent (15%) of the
            Compensation, which he or she receives on each pay day during the Offering Period
            (for illustrative purposes, should a pay day occur on an Exercise Date, a Participant
            will have any payroll deductions made on such day applied to his or her account under
            the then-current Purchase Period or Offering Period). The Administrator, in its sole discretion,
            may permit all Participants in a specified Offering to contribute amounts to the Plan
            through payment by cash, check or other means set forth in the subscription agreement
            prior to each Exercise Date of each Purchase Period. A Participant’s subscription agreement
            will remain in effect for successive Offering Periods unless terminated as provided in Section 10 hereof.
        """
        expected_output = {"error": "'NoneType' object has no attribute 'group'"}
        result = self.extractor.extract_data(text)
        self.assertEqual(result, expected_output)
