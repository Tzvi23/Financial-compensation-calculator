import data_input


class parameters:
    def __init__(self):
        self.interest_rate = data_input.interest_rate
        self.departure_probabilities = data_input.get_prob
        self.pay_rise = data_input.pay_rise
        self.payroll_dateRise = data_input.payroll_date_rise
        # Death tables
        self.male_deathTable = data_input.male_death
        self.female_deathTable = data_input.female_death
