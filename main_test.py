from worker_class import worker
from stats_parameters import parameters
from equations import calculate_current_compensation_value

# region load Example data
# Create some workers based on the examples
a = worker(w_id=1, prop=30000, a_14=1, seniority=5, wage=10000, retirementAge=3)
b = worker(w_id=2, prop=0, a_14=0.72, seniority=10, wage=15000, retirementAge=3)

workers = dict()
workers['a'] = a
workers['b'] = b
print(workers)

# Create example parameters
param = parameters(0.001, 0.15, 0.002,
                   death=0.0001, resignation=0.1, dismissal=0.05,
                   pay_rise=0.04)
# param.create_discount_rates_external(0.001, 0.15, 0.002)
print(param)
# endregion

print('Total: ' + str(calculate_current_compensation_value(workers['a'], param)))
print('Total: ' + str(calculate_current_compensation_value(workers['b'], param)))
print()
