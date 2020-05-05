"""
Author: Tzvi Puchinsky
"""
from worker_class import worker
from general_parameters import parameters
import equations as eq
from definitions import none_value as nv
import definitions as de
import data_input as di
from datetime import datetime
from print_colors import col


def check_art14(worker_test):
    """
    Check if the specific worker needs actuarial calculation. If he has 100% article 14 no calculation needed.
    """
    if worker_test.start_work == worker_test.start_article14 and worker_test.article14 == 0:
        return False
    else:
        return True


def convert_data_to_obj(data):
    def create_worker_obj(emp_data):
        return worker(w_id=int(emp_data[0]),
                      name=emp_data[1].strip(),
                      l_name=emp_data[2].strip(),
                      gender=de.gender[emp_data[3]],
                      birthDate=emp_data[4],
                      start_work=emp_data[5],
                      wage=emp_data[6],
                      start_art14=nv(emp_data[7]),
                      a_14=nv(emp_data[8]),
                      prop=nv(emp_data[9]),
                      deposit=nv(emp_data[10]),
                      res_date=nv(emp_data[11]),
                      payment_from_prop=nv(emp_data[12]),
                      check=nv(emp_data[13]),
                      ret_reason=de.retirement_reason[emp_data[14]])

    employees = list()
    for emp in data:
        employees.append(create_worker_obj(emp))
    return employees


employee_list = convert_data_to_obj(di.data)
print(employee_list)
"""
# region load Example data
# Create some workers based on the examples
a = worker(w_id=1, prop=30000, a_14=1, seniority=5, wage=10000, retirementAge=3)
b = worker(w_id=2, prop=0, a_14=0.72, seniority=10, wage=15000, retirementAge=3)

workers = dict()
workers['a'] = a
workers['b'] = b
print(workers)
"""

# Create example parameters
# param = parameters(0.001, 0.15, 0.002,
#                    death=0.0001, resignation=0.1, dismissal=0.05,
#                    pay_rise=0.04)
param = parameters()
eq.calculate_benefits_paid(employee_list)


# Specific worker testing
def test_worker(worker_test):
    if check_art14(worker_test):
        eq.calculate_current_compensation_value(worker_test, param)
        eq.current_service_cost(worker_test, float(datetime.now().strftime('%j')) / 366)
        eq.calculate_interest_for_one_worker(worker_test, param)


# param.create_discount_rates_external(0.001, 0.15, 0.002)
def run_dataSet(employee_list_loop):
    for workerId in employee_list_loop:
        if check_art14(workerId):
            try:
                eq.calculate_current_compensation_value(workerId, param)
                eq.current_service_cost(workerId, float(datetime.now().strftime('%j')) / 366)
                eq.calculate_interest_for_one_worker(workerId, param)
            except Exception as e:
                print(f'{col.FAIL}{e}{col.ENDC}')
                print(f'{col.FAIL}WorkerID: {workerId.id}{col.ENDC}')
                x = input(f'{col.OKGREEN}Press SPACE+ENTER to continue{col.ENDC}')


# endregion

# test_worker(employee_list[1])
run_dataSet(employee_list)

"""
eq.calculate_current_compensation_value(workers['a'], param)
eq.current_service_cost(workers['a'], 0.5)

eq.calculate_current_compensation_value(workers['b'], param)
eq.current_service_cost(workers['b'], 0.5)
print()
"""
