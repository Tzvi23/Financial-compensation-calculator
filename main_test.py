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
import pandas as pd


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
        eq.calculate_complex_current_compensation_value(worker_test, param)
        eq.current_service_cost(worker_test, float(datetime.now().strftime('%j')) / 366)
        eq.calculate_interest_for_one_worker(worker_test, param)


# param.create_discount_rates_external(0.001, 0.15, 0.002)
def run_dataSet(employee_list_loop):
    global skip_ids
    for workerId in employee_list_loop:
        # if workerId.id in skip_ids:
        #     continue
        if check_art14(workerId):
            # try:
            # [Hackaton] Dont do calculations for workers that left the organization
            if workerId.retirementReason is not None and workerId.resignation_date.year < datetime.now().year:
                continue
            eq.calculate_complex_current_compensation_value(workerId, param)
            eq.current_service_cost(workerId, float(datetime.now().strftime('%j')) / 366)
            eq.calculate_interest_for_one_worker(workerId, param)
            eq.calculate_expected_return(workerId, FVP_OB_VAR=0)  # TODO: update the FVP variable שווי הוגן של נכסי התוכנית יתרת פתיחה
            # except Exception as e:
            #     print(f'{col.FAIL}{e}{col.ENDC}')
            #     print(f'{col.FAIL}WorkerID: {workerId.id}{col.ENDC}')
            #     x = input(f'{col.OKGREEN}Press SPACE+ENTER to continue{col.ENDC}')


# endregion

# test_worker(employee_list[3])
skip_ids = [49, 64, 117, 118, 122]
run_dataSet(employee_list)
print(employee_list)


def output_results(employees, filename):
    def create_col_list(employee):
        cols = list(vars(employee).keys())
        col_remove = ['CSC', 'eT', 'complex_a_14', 'retirementReason', 'service_expectancy', 'epoch2_date']
        for index_name in col_remove:
            cols.remove(index_name)
        return cols

    employees_df = pd.DataFrame([vars(s) for s in employee_list], columns=create_col_list(employees[0]))

    # region Employee list
    # Change format for the dates : remove 00:00:00
    date_cols = ['birthday', 'start_work', 'start_article14', 'resignation_date']
    for col in date_cols:
        employees_df[col] = [time.date() for time in employees_df[col]]
    # Change female male
    employees_df['gender'] = employees_df['gender'].map({0: 'M', 1: 'F'})
    # Remove -1
    employees_df = employees_df.replace(-1, 0)
    # endregion

    # ערך נוכחי התחייבות - יתרת פתיחה
    CCV_open = 0
    # region info summary
    # Summary info
    total_ccv = float(sum([w.CCV for w in employees]))
    total_csc = float(sum([w.CSC for w in employees]))
    total_cost_of_capitalization = float(sum([w.cost_of_capitalization for w in employees]))
    total_benefits_paid = float(eq.calculate_benefits_paid(employees))
    # part 2
    # שווי הוגן של נכסי התוכנית - יתרת פתיחה
    FVP_CB = 1
    total_expected_return = float(sum([w.expected_return for w in employees]))
    total_deposit = float(sum([w.deposit for w in employees]))
    total_benefits_from_dep = float(sum([w.paymentFromProperty for w in employees]))
    total_fair_value = float(sum([w.property for w in employees]))
    summary_dict = {'Field':
                        ['ערך נוכחי התחייבות - יתרת פתיחה',
                         'עלות שירות שוטף',
                         'עלות ההיוון (interest cost)',
                         'הטבות ששולמו',
                         'הפסדים (רווחים) אקטואריים (P.N)',
                         'ערך נוכחי התחייבות - יתרת סגירה',
                         ' ',
                         'שווי הוגן של נכסי התוכנית - יתרת פתיחה',
                         'תשואה צפויה על נכסי התוכנית',
                         'הפקדות לנכסי התוכנית',
                         'הטבות ששולמו מנכסי התוכנית',
                         'רווחים (הפסדים) אקטואריים (P.N)',
                         'שווי הוגן של נכסי התוכנית - יתרת סגירה'],
                    'Value':
                        [CCV_open,
                         total_csc,
                         total_cost_of_capitalization,
                         total_benefits_paid,
                         float(eq.calculate_actuarial_losses(total_ccv, CCV_open, total_csc, total_cost_of_capitalization,
                                                       total_benefits_paid)),
                         total_ccv,
                         0,
                         FVP_CB,
                         total_expected_return,
                         total_deposit,
                         total_benefits_from_dep,
                         float(eq.calculate_actuarial_gains(total_fair_value, FVP_CB, total_expected_return,
                                                            total_deposit, total_benefits_from_dep)),
                         total_fair_value
                         ]}
    summary_df = pd.DataFrame(summary_dict)
    # endregion

    # Write to df to excel file
    with pd.ExcelWriter(filename) as writer:
        employees_df.to_excel(writer, sheet_name='Employee list', index=False)
        summary_df.to_excel(writer, sheet_name='Total info', index=False)


output_results(employee_list, 'output_second_stage4.xlsx')

"""
eq.calculate_current_compensation_value(workers['a'], param)
eq.current_service_cost(workers['a'], 0.5)

eq.calculate_current_compensation_value(workers['b'], param)
eq.current_service_cost(workers['b'], 0.5)
print()
"""
