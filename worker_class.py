"""
Worker class
Contains the basic data regarding each worker
"""
from datetime import datetime


class worker:
    def __init__(self, w_id=None,
                 name=None,
                 l_name=None,
                 gender=None,
                 birthDate=None,
                 start_work=None,
                 wage=None,
                 start_art14=None,
                 a_14=1,
                 prop=None,
                 deposit=None,
                 res_date=None,
                 payment_from_prop=None,
                 check=None,
                 ret_reason=None,
                 complex_a_14=False,
                 seniority=None,
                 retirementAge=67):

        self.id = w_id
        self.name = name
        self.last_name = l_name
        self.gender = gender
        self.birthday = birthDate
        self.start_work = start_work
        self.start_article14 = start_art14
        self.deposit = deposit
        self.resignation_date = res_date
        if payment_from_prop is None:
            self.paymentFromProperty = 0
        else:
            self.paymentFromProperty = payment_from_prop
        if check is None:
            self.check = 0
        else:
            self.check = check
        self.retirementReason = ret_reason
        self.property = prop  # Int
        self.complex_a_14 = complex_a_14
        if self.complex_a_14 is False:
            if a_14 is None:
                self.article14 = float(0)
            elif a_14 != 1:
                a_14 = float(a_14) / 100
                self.article14 = 1 - a_14  # Percentage (float)
            else:
                self.article14 = a_14
        else:
            self.article14 = a_14  # Except tuples ((years, 1 - percentage), (years, 1 - percentage) ,.. )
        self.seniority = seniority  # Int - number of years on the job
        self.wage = wage  # Int/Float
        self.retirementAge = 67 if self.gender == 0 else 64
        self.service_expectancy = 0
        self.yearsToWork = 0
        self.age = 0
        self.age_startWork = 0
        self.benefits_paid = 0
        self.epoch2_date = None
        # Calculations Results
        self.CCV = -1  # Current Compensation Value
        self.CSC = -1  # Current Service Cost
        self.eT = -1
        self.cost_of_capitalization = -1

        # Run Calc functions
        self.calc_seniority()
        self.calc_yearsToWork()
        self.calc_age()
        self.calc_benefits()
        self.calc_age_startWork()

    # Calculate function
    def calc_service_expectancy(self, prob_death, resignation, dismissal, currentAge):
        base = 1 - (dismissal + resignation) - prob_death
        for year in range(self.retirementAge - currentAge):
            self.service_expectancy += base ** year

    def calc_yearsToWork(self):
        retirement_year = self.birthday.year + self.retirementAge
        self.yearsToWork = retirement_year - self.start_work.year

    def calc_seniority(self):
        today = datetime.now().year
        self.seniority = today - self.start_work.year

    def calc_age(self):
        self.age = datetime.now().year - self.birthday.year

    def calc_benefits(self):
        self.benefits_paid = self.paymentFromProperty + self.check

    def calc_age_startWork(self):
        self.age_startWork = self.start_work.year - self.birthday.year

    # region Setters
    def set_id(self, w_id):
        self.id = w_id

    def set_name(self, name):
        self.name = name

    def set_property(self, prop):
        self.property = prop

    def set_article14(self, a_14):
        self.article14 = a_14

    def set_seniority(self, sen):
        self.seniority = sen

    def set_wage(self, wage):
        self.wage = wage

    # endregion

    def __str__(self):
        return '~~~~~~~~~~~~~~~~~~~~~~~~ \n' + \
               f'Worker Id: {self.id} | Worker Name: {self.name}\n' + \
               f'Properties: {self.property}\n' + \
               f'Article 14: {self.article14}\n' + \
               f'Seniority: {self.seniority}\n' + \
               f'Wage: {self.wage}\n' + \
               '#########################\n'

    def __repr__(self):
        return f'<Worker Class id {self.id}>'
