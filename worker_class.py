"""
Worker class
Contains the basic data regarding each worker
"""


class worker:
    def __init__(self, w_id=None, name=None, prop=None, a_14=None, seniority=None, wage=None):
        self.id = w_id
        self.name = name
        self.property = prop  # Int
        self.article14 = a_14  # Percentage (float)
        self.seniority = seniority  # Int - number of years on the job
        self.wage = wage  # Int/Float

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
