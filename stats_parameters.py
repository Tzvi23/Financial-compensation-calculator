class parameters:
    def __init__(self, *args, death=0, resignation=0, dismissal=0, pay_rise=0):
        self.prob_death = death
        self.resignation = resignation
        self.dismissal = dismissal

        self.discount_rates = dict()

        self.pay_rise_rate = pay_rise

        if args is not None:
            self.create_discount_rates_init(args)

    def create_discount_rates_init(self, args):
        if args is not None:
            for year in range(1, len(args) + 1):
                self.discount_rates[year] = args[year - 1]

    def create_discount_rates_external(self, *args):
        if args is not None:
            for year in range(1, len(args) + 1):
                self.discount_rates[year] = args[year - 1]

    def __str__(self):
        return 'Parameters: \n' + \
                f'  Death probability: {self.prob_death}\n' + \
                f'  Resignation probability: {self.resignation}\n' + \
                f'  Dismissal probability: {self.dismissal} \n' + \
                f'  Discount Rates: {self.discount_rates} \n' + \
                f'  Pay rise rate: {self.pay_rise_rate}'
