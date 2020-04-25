from sympy import *
from print_colors import col


def print_res(message, res):
    """ Prints the result with color """
    print(f'{col.OKBLUE}{message}: {res}{col.ENDC}')


# region <!--- PART 1 : Current compensation value  ---!>
def calculate_current_compensation_value(worker, param):
    """
    Calculating the current compensation value based on long equation.
    To build the final equation the function uses 3 part equation.
    After the calculation finished the results is set to worker object - worker.CCV
    """
    LS, SEN, SGR, RET, DISR, t, p, q, ART14_1 = symbols('LastSalary Seniority1 Salary_Growth_Rate retirement_age Discount_Rate t p q Article14_1')
    part1 = LS * SEN * ART14_1 * ((((1 + SGR) ** (t + 0.5)) * p**t * q) / ((1 + DISR) ** (t + 0.5)))
    # print(part1)

    POS, RES = symbols('Property Resignation')
    part2 = POS * p * RES
    # print(part2)

    d, SEN2, ART14_2 = symbols('death Seniority2 Article14_1')
    part3 = LS * SEN2 * ART14_2 * (((1 + SGR) ** (t + 0.5) * p ** t * d) / ((1 + DISR) ** (t + 0.5)))
    # print(part3)

    # region Load values
    LS_VAL = worker.wage  # LastSalary
    SEN_VAL = worker.seniority  # Seniority
    RET_VAL = worker.retirementAge  # retirement_age
    SGR_VAL = param.pay_rise_rate  # Salary_Growth_Rate
    p_VAL = 1 - (param.dismissal + param.resignation + param.prob_death)  # p -  stay on the job probability
    q_VAL = param.dismissal  # q - fired from the job probability
    POS_VAL = worker.property  # Property
    d_VAL = param.prob_death  # death probability
    RES_VAL = param.resignation  # Resignation probability
    ART14_VAL = worker.article14  # article 14 percentage

    sub_dict = dict()  # declaration
    if worker.complex_a_14 is False:
        sub_dict = {
            LS: LS_VAL,
            SEN: SEN_VAL,
            SEN2: SEN_VAL,
            RET: RET_VAL,
            SGR: SGR_VAL,
            p: p_VAL,
            q: q_VAL,
            POS: POS_VAL,
            d: d_VAL,
            RES: RES_VAL,
            ART14_1: ART14_VAL,
            ART14_2: ART14_VAL
        }
    # endregion

    formula = part1 + part2 + part3
    # print(formula)
    est = 0
    for c_t in range(worker.retirementAge):
        sub_dict[t] = c_t  # Update t value
        sub_dict[DISR] = param.discount_rates[c_t + 1]  # Update discount rate value by params values
        res = float(formula.subs(sub_dict))  # Calculate value
        # print(res)
        est += res  # sum all values

    print_res('Calculated CCV - Current Compensation Value', est)
    worker.CCV = est
    return est
# endregion


# region <!--- PART 2 : Current service cost ---!>
def current_service_cost(worker, partOfYear):
    """
    Calculates the service cost.
    :param worker: Worker object with all the specific worker data [Worker obj]
    :param partOfYear: What part of the year the worker worked [float]
    After the calculation finished the results is set to worker object - worker.CSC
    """
    if worker.article14 == 1:
        print(f'{col.OKGREEN}For worker with ARTICLE 14  = 100% cannot compute Current Service Cost {col.ENDC}')
        return

    if worker.CCV == -1:
        raise ValueError('Current compensation value Needed - use calculate_current_compensation_value function')

    # Actuarial factor - AF
    CCV, LS, SEN, ART14 = symbols('Current_Compensation_Value Last_Salary Seniority Article14')
    AF_RES = (CCV) / (LS * SEN * (1 - ART14))

    # Current Service Cost - CSC
    POY, AF = symbols('Part_Of_Year Actuarial_Factor')
    CSC = LS * POY * (1 - ART14) * AF

    AF_dict = {
        LS: worker.wage,
        SEN: worker.seniority,
        ART14: worker.article14,
        CCV: worker.CCV
    }

    # Calculation results of Actuarial factor
    CALC_AF = AF_RES.subs(AF_dict)

    CSC_dict = {
        LS: worker.wage,
        POY: partOfYear,
        ART14: worker.article14,
        AF: CALC_AF
    }

    # Calculate the total cost
    COST = CSC.subs(CSC_dict)
    print_res('Calculated CSC - Current Service Cost', COST)
    worker.CSC = COST
    return COST
# endregion


# region <!--- PART 3 : Interest (Capitalization) ---!>
def calculate_interest(worker, param, benefits_paid, discount_rate):
    # TODO change worker to workers => supposed to be calculation on number of workers just add a loop afterwards
    """
    # TODO check how the E(t) needed in the equation calc
    Calculates the E(t) of the worker
    worker.calc_service_expectancy(param.prob_death, param.resignation, param.dismissal, currentAge=20)
    """

    CCV, DR, CSC, BP = symbols('Current_Compensation_Value Discount_Rate Current_Service_Cost Benefits_Paid')
    eq = (CCV * DR) + ((CSC - BP) * (DR / 2))

    ci_dict = {
        CCV: worker.CCV,
        DR: discount_rate,
        CSC: worker.CSC,
        BP: benefits_paid
    }

    # For one worker
    interest = eq.subs(ci_dict)
    print_res('Current interest: ', interest)

    return interest
# endregion


# region <!--- PART4 : Benefits paid ---!>
# TODO write function that sums all the benefits paid to all workers
# endregion


# region <!--- PART5 : Actuarial losses ---!>
def calculate_actuarial_losses(CCCB, CCV, CSC, INTEREST, BP):
    """
    :param CCCB: Current Compensation Closing Balance
    :param CCV: Current Compensation Values
    :param CSC: Current Service Cost
    :param INTEREST: Interest (Part3)
    :param BP: Benefits Paid
    :return: Actuarial Losses float value
    """
    return CCCB - CCV - CSC - INTEREST + BP
# endregion


# region <!--- PART6 : Present value Commitment to closing balance ---!>
def calculate_closing_balance(workers):
    CB = 0  # Closing Balance
    for worker in workers:
        if worker.CCV != -1:
            CB += worker.CCV
    print_res('Closing Balance: ', CB)
    return CB
# endregion
